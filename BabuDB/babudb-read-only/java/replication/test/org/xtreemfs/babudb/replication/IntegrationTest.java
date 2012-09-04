/*
 * Copyright (c) 2011, Jan Stender, Bjoern Kolbeck, Mikael Hoegqvist,
 *                     Felix Hupfeld, Felix Langner, Zuse Institute Berlin
 * 
 * Licensed under the BSD License, see LICENSE file for details.
 * 
 */
package org.xtreemfs.babudb.replication;

import static org.xtreemfs.babudb.replication.TestParameters.*;

import java.io.File;
import java.util.Map.Entry;
import java.util.concurrent.atomic.AtomicInteger;

import junit.framework.TestCase;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.xtreemfs.babudb.BabuDBFactory;
import org.xtreemfs.babudb.api.BabuDB;
import org.xtreemfs.babudb.api.database.Database;
import org.xtreemfs.babudb.api.database.DatabaseInsertGroup;
import org.xtreemfs.babudb.api.database.DatabaseRequestListener;
import org.xtreemfs.babudb.api.database.ResultSet;
import org.xtreemfs.babudb.api.exception.BabuDBException;
import org.xtreemfs.babudb.config.ReplicationConfig;
import org.xtreemfs.foundation.logging.Logging;
import org.xtreemfs.foundation.logging.Logging.Category;
import org.xtreemfs.foundation.util.FSUtils;

/**
 * Test basic BabuDB IO for a fully synchronous setup of BabuDB instances using replication.
 * 
 * @author flangner
 * @since 03/31/2011
 */
public class IntegrationTest extends TestCase {

    private BabuDB babu0;
    private BabuDB babu1;
    private BabuDB babu2;
    
    public IntegrationTest() throws Exception {
        Logging.start(Logging.LEVEL_ERROR, Category.all);
        
        FSUtils.delTree(new File(conf0.getBaseDir()));
        FSUtils.delTree(new File(conf1.getBaseDir()));
        FSUtils.delTree(new File(conf2.getBaseDir()));
        FSUtils.delTree(new File(conf0.getDbLogDir()));
        FSUtils.delTree(new File(conf1.getDbLogDir()));
        FSUtils.delTree(new File(conf2.getDbLogDir()));
        
        FSUtils.delTree(new File(
                new ReplicationConfig("config/replication_server0.test", conf0).getTempDir()));
        FSUtils.delTree(new File(
                new ReplicationConfig("config/replication_server1.test", conf1).getTempDir()));
        FSUtils.delTree(new File(
                new ReplicationConfig("config/replication_server2.test", conf2).getTempDir()));
    }
    
    /**
     * @throws java.lang.Exception
     */
    @Before
    public void setUp() throws Exception {
        System.out.println("=== " + getName() + " ===");
        
        // starting three local BabuDB services supporting replication; based on mock databases
        Thread t0 = new Thread(new Runnable() {
            
            @Override
            public void run() {
                try {
                    babu0 = BabuDBFactory.createBabuDB(conf0);
                } catch (BabuDBException e) {
                    fail(e.getMessage());
                }
            }
        });
        Thread t1 = new Thread(new Runnable() {
            
            @Override
            public void run() {
                try {
                    babu1 = BabuDBFactory.createBabuDB(conf1);
                } catch (BabuDBException e) {
                    fail();
                }
            }
        });
        Thread t2 = new Thread(new Runnable() {
            
            @Override
            public void run() {
                try {
                    babu2 = BabuDBFactory.createBabuDB(conf2);
                } catch (BabuDBException e) {
                    fail();
                }
            }
        });
        
        t0.start();
        t1.start();
        t2.start();
        t0.join();
        t1.join();
        t2.join();
    }

    /**
     * @throws java.lang.Exception
     */
    @After
    public void tearDown() throws Exception {
        babu0.shutdown();
        babu1.shutdown();
        babu2.shutdown();
    }

    /**
     * @throws Exception
     */
    @Test
    public void testBasicIO() throws Exception {
               
        // create some DBs
        Database test0 = babu0.getDatabaseManager().createDatabase("0", 3);    
        Database test1 = babu1.getDatabaseManager().createDatabase("1", 3);
        Database test2 = babu2.getDatabaseManager().createDatabase("2", 3);
                
        // retrieve the databases
        test0 = babu2.getDatabaseManager().getDatabase("0");
        test1 = babu0.getDatabaseManager().getDatabase("1");
        test2 = babu1.getDatabaseManager().getDatabase("2");
        
        // make some inserts
        final AtomicInteger notReady = new AtomicInteger(3);
        final Object context0 = new Object();
        DatabaseInsertGroup ig = test0.createInsertGroup();
        ig.addInsert(0, "bla00".getBytes(), "blub00".getBytes());
        ig.addInsert(1, "bla01".getBytes(), "blub01".getBytes());
        ig.addInsert(2, "bla02".getBytes(), "blub02".getBytes());
        test0.insert(ig, context0).registerListener(new DatabaseRequestListener<Object>() {
            @Override
            public void finished(Object result, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                assertEquals(context0, context);
            }
            
            @Override
            public void failed(BabuDBException error, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                fail("This should not happen.");
            }
        });
        
        final Object context1 = new Object();
        ig = test1.createInsertGroup();
        ig.addInsert(0, "bla10".getBytes(), "blub10".getBytes());
        ig.addInsert(1, "bla11".getBytes(), "blub11".getBytes());
        ig.addInsert(2, "bla12".getBytes(), "blub12".getBytes());
        test1.insert(ig, context1).registerListener(new DatabaseRequestListener<Object>() {
            @Override
            public void finished(Object result, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                assertEquals(context1, context);
            }
            
            @Override
            public void failed(BabuDBException error, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                fail("This should not happen.");
            }
        });
        
        final Object context2 = new Object();
        ig = test2.createInsertGroup();
        ig.addInsert(0, "bla20".getBytes(), "blub20".getBytes());
        ig.addInsert(1, "bla21".getBytes(), "blub21".getBytes());
        ig.addInsert(2, "bla22".getBytes(), "blub22".getBytes());
        test2.insert(ig, context2).registerListener(new DatabaseRequestListener<Object>() {
            @Override
            public void finished(Object result, Object context) {
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                assertEquals(context2, context);
            }
            
            @Override
            public void failed(BabuDBException error, Object context) {
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                fail("This should not happen.");
            }
        });
        
        // wait for the inserts to finish
        synchronized (notReady) {
            if (notReady.get() > 0) {
                notReady.wait();
            }
        }
        
        // retrieve the databases
        test0 = babu1.getDatabaseManager().getDatabase("0");
        test1 = babu2.getDatabaseManager().getDatabase("1");
        test2 = babu0.getDatabaseManager().getDatabase("2");
        
        // make some lookups
        byte[] res = test0.lookup(0, "bla00".getBytes(), test0).get();
        assertNotNull(res);
        assertEquals("blub00", new String(res));
        assertNull(test0.lookup(0, "bla20".getBytes(), test0).get());

        res = test0.lookup(1, "bla01".getBytes(), test0).get();
        assertNotNull(res);
        assertEquals("blub01", new String(res));
        assertNull(test0.lookup(1, "bla20".getBytes(), test0).get());
        
        res = test1.lookup(0, "bla10".getBytes(), test0).get();
        assertNotNull(res);
        assertEquals("blub10", new String(res));
        assertNull(test0.lookup(0, "bla20".getBytes(), test0).get());
        
        res = test2.lookup(0, "bla20".getBytes(), test0).get();
        assertNotNull(res);
        assertEquals("blub20", new String(res));
        assertNull(test0.lookup(0, "bla01".getBytes(), test0).get());
    }
    
    @Test
    public void testPrefixLookups() throws Exception {
        
        // create some DBs
        babu0.getDatabaseManager().createDatabase("prefixLookup", 1);
        Database test0 = babu2.getDatabaseManager().getDatabase("prefixLookup");
        Database test1 = babu0.getDatabaseManager().getDatabase("prefixLookup");
        Database test2 = babu1.getDatabaseManager().getDatabase("prefixLookup");
        
        // make some inserts on database 'test1'
        final AtomicInteger notReady = new AtomicInteger(2);
        final Object context0 = new Object();
        DatabaseInsertGroup ig = test1.createInsertGroup();
        ig.addInsert(0, "bla0".getBytes(), "blub0".getBytes());
        ig.addInsert(0, "bla1".getBytes(), "blub1".getBytes());
        ig.addInsert(0, "bla2".getBytes(), "blub2".getBytes());
        test1.insert(ig, context0).registerListener(new DatabaseRequestListener<Object>() {
            @Override
            public void finished(Object result, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                assertEquals(context0, context);
            }
            
            @Override
            public void failed(BabuDBException error, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                fail("This should not happen.");
            }
        });
        
        final Object context1 = new Object();
        ig = test1.createInsertGroup();
        ig.addInsert(0, "yagga0".getBytes(), "yagga0".getBytes());
        ig.addInsert(0, "yagga1".getBytes(), "yagga1".getBytes());
        ig.addInsert(0, "yagga2".getBytes(), "yagga2".getBytes());
        test1.insert(ig, context1).registerListener(new DatabaseRequestListener<Object>() {
            @Override
            public void finished(Object result, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                assertEquals(context1, context);
            }
            
            @Override
            public void failed(BabuDBException error, Object context) {
                
                if (notReady.decrementAndGet() == 0) {
                    synchronized (notReady) {
                        notReady.notify();
                    }
                }
                fail("This should not happen.");
            }
        });
        
        // wait for the inserts to finish
        synchronized (notReady) {
            if (notReady.get() > 0) {
                notReady.wait();
            }
        }
        
    /*
     * prefix
     */
        
        // perform a prefix lookup on database 'test0'
        ResultSet<byte[], byte[]> result = test0.prefixLookup(0, "bla".getBytes(), null).get();
        assertTrue(result.hasNext());
        Entry<byte[], byte[]> next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        assertFalse(result.hasNext());
        
        // perform a prefix lookup on database 'test1'
        result = test1.prefixLookup(0, "bla".getBytes(), null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        assertFalse(result.hasNext());
        
        // perform a prefix lookup on database 'test2'
        result = test2.prefixLookup(0, "bla".getBytes(), null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        assertFalse(result.hasNext());
        
        // perform an empty prefix lookup on database 'test0'
        result = test0.prefixLookup(0, null, null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        next = result.next();
        assertEquals("yagga0", new String(next.getKey()));
        assertEquals("yagga0", new String(next.getValue()));
        next = result.next();
        assertEquals("yagga1", new String(next.getKey()));
        assertEquals("yagga1", new String(next.getValue()));
        next = result.next();
        assertEquals("yagga2", new String(next.getKey()));
        assertEquals("yagga2", new String(next.getValue()));
        assertFalse(result.hasNext());
        
    /*
     * prefix reverse
     */
        
        // perform a prefix lookup on database 'test0'
        result = test0.reversePrefixLookup(0, "bla".getBytes(), null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertFalse(result.hasNext());
        
        // perform a prefix lookup on database 'test1'
        result = test1.reversePrefixLookup(0, "bla".getBytes(), null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertFalse(result.hasNext());
        
        // perform a prefix lookup on database 'test2'
        result = test2.reversePrefixLookup(0, "bla".getBytes(), null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertFalse(result.hasNext());
        
        // perform an empty prefix lookup on database 'test0'
        result = test0.reversePrefixLookup(0, null, null).get();
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("yagga2", new String(next.getKey()));
        assertEquals("yagga2", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("yagga1", new String(next.getKey()));
        assertEquals("yagga1", new String(next.getValue()));
        assertTrue(result.hasNext());
        next = result.next();
        assertEquals("yagga0", new String(next.getKey()));
        assertEquals("yagga0", new String(next.getValue()));
        next = result.next();
        assertEquals("bla2", new String(next.getKey()));
        assertEquals("blub2", new String(next.getValue()));
        next = result.next();
        assertEquals("bla1", new String(next.getKey()));
        assertEquals("blub1", new String(next.getValue()));
        next = result.next();
        assertEquals("bla0", new String(next.getKey()));
        assertEquals("blub0", new String(next.getValue()));
        assertFalse(result.hasNext());
    }
    
    /**
     * @throws Exception
     */
    @Test
    public void testRestart() throws Exception {
        
        // retrieve the databases
        Database test0 = babu1.getDatabaseManager().getDatabase("0");
        Database test1 = babu2.getDatabaseManager().getDatabase("1");
        Database test2 = babu0.getDatabaseManager().getDatabase("2");
        
        // make some lookups
        byte[] res = test0.lookup(0, "bla00".getBytes(), test0).get();
        assertNotNull(res);
        assertEquals("blub00", new String(res));
        
        assertNull(test0.lookup(0, "bla20".getBytes(), test0).get());
        
        res = test1.lookup(0, "bla10".getBytes(), test1).get();
        assertNotNull(res);
        assertEquals("blub10", new String(res));
        
        assertNull(test1.lookup(0, "bla20".getBytes(), test1).get());
        
        res = test2.lookup(0, "bla20".getBytes(), test2).get();
        assertNotNull(res);
        assertEquals("blub20", new String(res));
        
        assertNull(test2.lookup(0, "bla10".getBytes(), test2).get());
    }
}
