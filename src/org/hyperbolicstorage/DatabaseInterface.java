package org.hyperbolicstorage;

import java.nio.ByteBuffer;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Arrays;
import java.util.Collections;
import java.io.IOException;
import java.lang.InterruptedException;

import org.xtreemfs.babudb.api.BabuDB;
import org.xtreemfs.babudb.api.DatabaseManager;
import org.xtreemfs.babudb.api.database.Database;
import org.xtreemfs.babudb.api.database.DatabaseRequestResult;
import org.xtreemfs.babudb.api.database.ResultSet;
import org.xtreemfs.babudb.BabuDBFactory;
import org.xtreemfs.babudb.config.BabuDBConfig;
import org.xtreemfs.babudb.log.DiskLogger.SyncMode;
import org.xtreemfs.babudb.api.exception.BabuDBException;

public class DatabaseInterface {
    private BabuDB babuDB = null;
    private DatabaseManager databaseManager = null;
    private Database geoTiles = null;

    public DatabaseInterface(String dbPath) throws IOException {
        final int numThreads = 0;
        BabuDBConfig babuDBConfig = new BabuDBConfig(dbPath + "/databases/", dbPath + "/dblog/", numThreads, 1024*1024*16, 5*60, SyncMode.FSYNC, 50, 0, false, 16, 1024*1024*512);

        try {
            babuDB = BabuDBFactory.createBabuDB(babuDBConfig);
            databaseManager = babuDB.getDatabaseManager();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while making connection: " + exception.getMessage());
        }

        try {
            geoTiles = databaseManager.getDatabase("geoTiles");
        }
        catch (BabuDBException ignoreException) {
            try {
                geoTiles = databaseManager.createDatabase("geoTiles", 1);
            }
            catch (BabuDBException exception) {
                throw new IOException("BabuDBException while creating database: " + exception.getMessage());
            }
        }
    }

    public void close() throws IOException {
        try {
            babuDB.getCheckpointer().checkpoint();
            babuDB.shutdown();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while closing: " + exception.getMessage());
        }
        catch (InterruptedException exception) {
            throw new IOException("InterruptedException while closing: " + exception.getMessage());
        }
    }

    protected byte[] getKey(int latitude, long longitude, long id) {
        ByteBuffer byteBuffer = ByteBuffer.allocate(20);
        byteBuffer.putInt(latitude);
        byteBuffer.putLong(longitude);
        byteBuffer.putLong(id);
        return byteBuffer.array();
    }

    public void insert(int latitude, long longitude, long id, double depth, String drawable) throws IOException {
        byte[] drawableBytes = drawable.getBytes();
        ByteBuffer byteBuffer = ByteBuffer.allocate(8 + drawableBytes.length);
        byteBuffer.putDouble(depth);
        byteBuffer.put(drawableBytes);

        DatabaseRequestResult<Object> result;
        result = geoTiles.singleInsert(0, getKey(latitude, longitude, id), byteBuffer.array(), null);
        try {
            result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while inserting: " + exception.getMessage());
        }
    }

    public void delete(int latitude, long longitude, long id) throws IOException {
        DatabaseRequestResult<Object> result;
        result = geoTiles.singleInsert(0, getKey(latitude, longitude, id), null, null);
        try {
            result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while deleting: " + exception.getMessage());
        }
    }

    public void clearAll() throws IOException {
        // FIXME
    }

    public String getOne(int latitude, long longitude, long id) throws IOException {
        DatabaseRequestResult<byte[]> result = geoTiles.lookup(0, getKey(latitude, longitude, id), null);
        try {
            byte[] byteResult = result.get();
            if (byteResult == null) {
                return null;
            } else {
                return new String(Arrays.copyOfRange(byteResult, 8, byteResult.length));
            }
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException during lookup: " + exception.getMessage());
        }
    }

    class DepthDrawable implements Comparable {
        public double depth;
        public String drawable;

        public DepthDrawable(double depth_, String drawable_) {
            depth = depth_;
            drawable = drawable_;
        }

        public int compareTo(Object o) {
            DepthDrawable other = (DepthDrawable)o;
            double comparison = this.depth - other.depth;
            if (comparison > 0.0) { return 1; }
            else if (comparison < 0.0) { return -1; }
            else { return 0; }
        }
    }

    public int getRange(int latitude, long minLongitude, long maxLongitude, List<String> output) throws IOException {
        byte[] emptyId = {-128, -128, -128, -128, -128, -128, -128, -128};

        // inclusive
        ByteBuffer from = ByteBuffer.allocate(22);
        from.putInt(latitude);
        from.putLong(minLongitude);
        from.put(emptyId);

        // exclusive
        ByteBuffer to = ByteBuffer.allocate(22);
        to.putInt(latitude);
        to.putLong(maxLongitude);
        to.put(emptyId);

        DatabaseRequestResult<ResultSet<byte[], byte[]>> result;
        result = geoTiles.rangeLookup(0, from.array(), to.array(), null);

        List<DepthDrawable> depthDrawables = new ArrayList<DepthDrawable>();

        try {
            Iterator<Entry<byte[], byte[]>> iterator = result.get();
            while (iterator.hasNext()) {
                Entry<byte[], byte[]> keyValuePair = iterator.next();
                
                byte[] value = keyValuePair.getValue();
                double depth = ByteBuffer.wrap(value).getDouble();
                String drawable = new String(Arrays.copyOfRange(value, 8, value.length));

                depthDrawables.add(new DepthDrawable(depth, drawable));
            }
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException during lookup: " + exception.getMessage());
        }

        Collections.sort(depthDrawables);
        for (DepthDrawable depthDrawable : depthDrawables) {
            output.add(depthDrawable.drawable);
        }
        return depthDrawables.size();
    }

}
