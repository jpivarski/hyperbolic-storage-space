/*
 * Copyright (c) 2008 - 2011, Jan Stender, Bjoern Kolbeck, Mikael Hoegqvist,
 *                     Felix Hupfeld, Zuse Institute Berlin
 * 
 * Licensed under the BSD License, see LICENSE file for details.
 * 
 */

package org.xtreemfs.babudb.lsmdb;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.channels.ClosedByInterruptException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.xtreemfs.babudb.api.dev.BabuDBInternal;
import org.xtreemfs.babudb.api.dev.CheckpointerInternal;
import org.xtreemfs.babudb.api.dev.DatabaseInternal;
import org.xtreemfs.babudb.api.dev.SnapshotManagerInternal;
import org.xtreemfs.babudb.api.exception.BabuDBException;
import org.xtreemfs.babudb.api.exception.BabuDBException.ErrorCode;
import org.xtreemfs.babudb.log.DiskLogger;
import org.xtreemfs.babudb.snapshots.SnapshotConfig;
import org.xtreemfs.foundation.logging.Logging;
import org.xtreemfs.foundation.util.OutputUtils;

/**
 * This thread regularly checks the size of the database operations log and
 * initiates a checkpoint of all databases if necessary.
 * 
 * @author bjko
 */
public class CheckpointerImpl extends CheckpointerInternal {
    
    private final static class MaterializationRequest {
        
        MaterializationRequest(String dbName, int[] snapIDs, SnapshotConfig snap) {
            
            this.dbName = dbName;
            this.snapIDs = snapIDs;
            this.snap = snap;
        }
        
        String         dbName;
        
        int[]          snapIDs;
        
        SnapshotConfig snap;
        
    }
    
    private static final String                RUNTIME_STATE_CPCOUNT        = "checkpointer.cpCount";
    private static final String                RUNTIME_STATE_LASTCP         = "checkpointer.lastCpTimestampMillis";
    private static final String                RUNTIME_STATE_LASTCPDURATION = "checkpointer.lastCpDurationMillis";
    
    private volatile boolean                   quit;
    
    private final AtomicBoolean                suspended                    = new AtomicBoolean(false);
    private final Object                       suspensionLock               = new Object();
    
    private DiskLogger                         logger;
    
    private long                               checkInterval;
    
    /**
     * Maximum file size of operations log in bytes.
     */
    private long                               maxLogLength;
    
    private final BabuDBInternal               dbs;
    
    /**
     * a queue containing all snapshot materialization requests that should be
     * executed before the next checkpoint is made
     */
    private final List<MaterializationRequest> requests                     = new LinkedList<MaterializationRequest>();
    
    /**
     * indicates whether the next checkpoint has been triggered manually or
     * automatically
     */
    private boolean                            forceCheckpoint;
    
    /**
     * indicates when the current checkpoint is complete and is also a lock
     */
    private AtomicBoolean                      checkpointComplete           = new AtomicBoolean(true);
    
    /**
     * Flag to notify the disk-logger about a viewId incrementation.
     */
    private boolean                            incrementViewId              = false;
    private volatile LSN                       lastWrittenLSN;
    
    private AtomicInteger                      _checkpointCount             = new AtomicInteger();
    
    private AtomicLong                         _lastCheckpoint              = new AtomicLong();
    
    private AtomicLong                         _lastCheckpointDuration      = new AtomicLong();
    
    /**
     * Creates a new database checkpointer
     * 
     * @param master
     *            the database
     */
    public CheckpointerImpl(BabuDBInternal master) {
        setLifeCycleListener(master);
        this.dbs = master;
    }
    
    @Override
    public void init(DiskLogger logger, int checkInterval, long maxLogLength) throws BabuDBException {
        
        this.logger = logger;
        this.checkInterval = 1000L * checkInterval;
        this.maxLogLength = maxLogLength;
        
        if (!suspended.compareAndSet(true, false) && !quit) {
            start();
            try {
                waitForStartup();
            } catch (Exception e) {
                throw new BabuDBException(ErrorCode.INTERNAL_ERROR, e.getMessage(), e);
            }
        } else {
            synchronized (suspensionLock) {
                suspensionLock.notify();
            }
        }
    }
    
    /*
     * (non-Javadoc)
     * 
     * @see
     * org.xtreemfs.babudb.api.dev.CheckpointerInternal#suspendCheckpointing()
     */
    @Override
    public void suspendCheckpointing() throws InterruptedException {
        
        synchronized (suspended) {
            if (!suspended.compareAndSet(false, true)) {
                synchronized (this) {
                    notify();
                }
                suspended.wait();
            }
        }
    }
    
    /*
     * (non-Javadoc)
     * 
     * @see org.xtreemfs.babudb.api.dev.CheckpointerInternal#checkpoint(boolean)
     */
    @Override
    public LSN checkpoint(boolean incViewId) throws BabuDBException {
        
        synchronized (checkpointComplete) {
            checkpointComplete.set(false);
        }
        
        // notify the checkpointing thread to immediately process all requests
        // in the processing queue
        synchronized (this) {
            incrementViewId = incViewId;
            forceCheckpoint = true;
            notify();
        }
        
        // wait for the checkpoint to complete
        try {
            waitForCheckpoint();
            return lastWrittenLSN;
        } catch (InterruptedException e) {
            throw new BabuDBException(ErrorCode.INTERNAL_ERROR, "interrupted", e);
        }
    }
    
    /*
     * (non-Javadoc)
     * 
     * @see org.xtreemfs.babudb.lsmdb.Checkpointer#checkpoint()
     */
    @Override
    public void checkpoint() throws BabuDBException, InterruptedException {
        checkpoint(false);
    }
    
    /**
     * Materialize all snapshots in the queue before taking a checkpoint.
     * 
     * @throws BabuDBException
     *             if materialization failed.
     */
    private void materializeSnapshots() throws BabuDBException {
        
        for (;;) {
            MaterializationRequest rq = null;
            
            synchronized (requests) {
                if (requests.size() > 0)
                    rq = requests.remove(0);
            }
            
            if (rq == null)
                break;
            
            if (Logging.isDebug())
                Logging.logMessage(Logging.LEVEL_DEBUG, this, "snapshot materialization request found for database '"
                        + rq.dbName + "', snapshot: '" + rq.snap.getName() + "'");
            
            SnapshotManagerInternal snapMan = dbs.getSnapshotManager();
            
            // write the snapshot
            dbs.getDatabaseManager().getDatabase(rq.dbName)
                    .proceedWriteSnapshot(rq.snapIDs, snapMan.getSnapshotDir(rq.dbName, rq.snap.getName()), rq.snap);
            
            // notify the snapshot manager about the completion
            // of the snapshot
            snapMan.snapshotComplete(rq.dbName, rq.snap);
            
            Logging.logMessage(Logging.LEVEL_DEBUG, this, "snapshot materialization complete");
        }
    }
    
    /**
     * Internal method for creating a new database checkpoint. This involves the
     * following steps:
     * <ol>
     * <li>snapshot all indices of all databases
     * <li>create new log file for subsequent insertions
     * <li>write index snapshots to new on-disk index files
     * <li>link new on-disk files to index structures
     * <li>delete any obsolete on-disk files
     * <li>delete any obsolete log files
     * </ol>
     * The first two steps need to be sync'ed with new insertions but should be
     * very fast. The following steps are performed in a fully asynchronous
     * manner.
     * 
     * @throws BabuDBException
     * @throws InterruptedException
     */
    private void createCheckpoint() throws BabuDBException, InterruptedException {
        Logging.logMessage(Logging.LEVEL_INFO, this, "initiating database checkpoint...");
        
        Collection<DatabaseInternal> databases = dbs.getDatabaseManager().getDatabaseList();
        
        try {
            int[][] snapIds = new int[databases.size()][];
            int i = 0;
            
            try {
                // critical block...
                logger.lock();
                for (DatabaseInternal db : databases) {
                    snapIds[i++] = db.proceedCreateSnapshot();
                }
                lastWrittenLSN = logger.switchLogFile(incrementViewId);
                incrementViewId = false;
            } finally {
                if (logger.hasLock())
                    logger.unlock();
            }
            
            i = 0;
            for (DatabaseInternal db : databases) {
                db.proceedWriteSnapshot(lastWrittenLSN.getViewId(), lastWrittenLSN.getSequenceNo(), snapIds[i++]);
                db.proceedCleanupSnapshot(lastWrittenLSN.getViewId(), lastWrittenLSN.getSequenceNo());
            }
            
            // delete all logfile with LSN <= lastWrittenLSN
            File f = new File(dbs.getConfig().getDbLogDir());
            String[] logs = f.list(new FilenameFilter() {
                
                public boolean accept(File dir, String name) {
                    return name.endsWith(".dbl");
                }
            });
            if (logs != null) {
                Pattern p = Pattern.compile("(\\d+)\\.(\\d+)\\.dbl");
                for (String log : logs) {
                    Matcher m = p.matcher(log);
                    m.matches();
                    String tmp = m.group(1);
                    int viewId = Integer.valueOf(tmp);
                    tmp = m.group(2);
                    int seqNo = Integer.valueOf(tmp);
                    LSN logLSN = new LSN(viewId, seqNo);
                    if (logLSN.compareTo(lastWrittenLSN) <= 0) {
                        Logging.logMessage(Logging.LEVEL_DEBUG, this, "deleting old db log file: " + log);
                        f = new File(dbs.getConfig().getDbLogDir() + log);
                        if (!f.delete())
                            Logging.logMessage(Logging.LEVEL_WARN, this, "could not delete log file: %s",
                                    f.getAbsolutePath());
                    }
                }
            }
        } catch (IOException ex) {
            throw new BabuDBException(ErrorCode.IO_ERROR, "cannot create checkpoint", ex);
        }
        Logging.logMessage(Logging.LEVEL_INFO, this, "checkpoint complete");
    }
    
    /*
     * (non-Javadoc)
     * 
     * @see org.xtreemfs.babudb.api.dev.CheckpointerInternal#
     * addSnapshotMaterializationRequest( java.lang.String, int[],
     * org.xtreemfs.babudb.snapshots.SnapshotConfig)
     */
    @Override
    public void addSnapshotMaterializationRequest(String dbName, int[] snapIds, SnapshotConfig snap) {
        synchronized (requests) {
            requests.add(new MaterializationRequest(dbName, snapIds, snap));
        }
    }
    
    /*
     * (non-Javadoc)
     * 
     * @see org.xtreemfs.babudb.api.dev.CheckpointerInternal#
     * removeSnapshotMaterializationRequest( java.lang.String, java.lang.String)
     */
    @Override
    public void removeSnapshotMaterializationRequest(String dbName, String snapshotName) {
        
        synchronized (requests) {
            Iterator<MaterializationRequest> it = requests.iterator();
            while (it.hasNext()) {
                MaterializationRequest rq = it.next();
                if (snapshotName.equals(rq.snap.getName())) {
                    requests.remove(rq);
                    break;
                }
            }
        }
    }
    
    @Override
    public synchronized void shutdown() {
        quit = true;
        interrupt();
    }
    
    public void run() {
        Logging.logMessage(Logging.LEVEL_DEBUG, this, "operational");
        
        boolean manualCheckpoint = false;
        notifyStarted();
        while (!quit) {
            try {
                synchronized (this) {
                    if (!forceCheckpoint) {
                        wait(checkInterval);
                    }
                    manualCheckpoint = forceCheckpoint;
                    forceCheckpoint = false;
                }
                
                // this block allows to suspend the Checkpointer from taking
                // checkpoints until it has been re-init()
                synchronized (suspended) {
                    if (suspended.get()) {
                        
                        // lock
                        suspended.notify();
                        synchronized (suspensionLock) {
                            suspensionLock.wait();
                        }
                        continue;
                    }
                }
                
                final long lfsize = logger.getLogFileSize();
                if (manualCheckpoint || lfsize > maxLogLength) {
                    
                    if (!manualCheckpoint) {
                        Logging.logMessage(Logging.LEVEL_INFO, this, "database operation log has exceeded threshold "
                                + "size of " + maxLogLength + " (" + lfsize + ")");
                    } else {
                        Logging.logMessage(Logging.LEVEL_INFO, this, "triggered manual checkpoint");
                    }
                    
                    synchronized (dbs.getDatabaseManager().getDBModificationLock()) {
                        synchronized (this) {
                            long start = System.currentTimeMillis();
                            materializeSnapshots();
                            createCheckpoint();
                            
                            // update statistics
                            _checkpointCount.incrementAndGet();
                            _lastCheckpoint.set(System.currentTimeMillis());
                            _lastCheckpointDuration.set(System.currentTimeMillis() - start);
                        }
                    }
                }
            } catch (InterruptedException ex) {
                if (quit)
                    break;
                else
                    Logging.logMessage(Logging.LEVEL_DEBUG, this, "CHECKPOINT WAS ABORTED!");
            } catch (Throwable ex) {
                if (ex instanceof BabuDBException
                        && ((BabuDBException) ex).getCause() instanceof ClosedByInterruptException) {
                    Logging.logMessage(Logging.LEVEL_DEBUG, this, "CHECKPOINT WAS ABORTED!");
                } else {
                    Logging.logMessage(Logging.LEVEL_ERROR, this, "DATABASE CHECKPOINT CREATION FAILURE!");
                    Logging.logMessage(Logging.LEVEL_ERROR, this, OutputUtils.stackTraceToString(ex));
                }
            } finally {
                synchronized (checkpointComplete) {
                    checkpointComplete.set(true);
                    checkpointComplete.notify();
                }
            }
        }
        
        Logging.logMessage(Logging.LEVEL_DEBUG, this, "checkpointer shut down " + "successfully");
        notifyStopped();
    }
    
    /*
     * (non-Javadoc)
     * 
     * @see org.xtreemfs.babudb.api.Checkpointer#waitForCheckpoint()
     */
    @Override
    public void waitForCheckpoint() throws InterruptedException {
        
        synchronized (checkpointComplete) {
            while (!checkpointComplete.get()) {
                checkpointComplete.wait();
            }
        }
    }
    
    @Override
    public Object getRuntimeState(String property) {
        
        if (RUNTIME_STATE_CPCOUNT.equals(property))
            return _checkpointCount.get();
        if (RUNTIME_STATE_LASTCP.equals(property))
            return _lastCheckpoint.get();
        if (RUNTIME_STATE_LASTCPDURATION.equals(property))
            return _lastCheckpointDuration.get();
        
        return null;
    }
    
    @Override
    public Map<String, Object> getRuntimeState() {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put(RUNTIME_STATE_CPCOUNT, _checkpointCount.get());
        map.put(RUNTIME_STATE_LASTCP, _lastCheckpoint.get());
        map.put(RUNTIME_STATE_LASTCPDURATION, _lastCheckpointDuration.get());
        return map;
    }
    
}
