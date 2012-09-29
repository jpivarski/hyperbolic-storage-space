package org.hyperbolicstorage;

import java.nio.ByteBuffer;
import java.util.Set;
import java.util.Iterator;
import java.util.Map.Entry;
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

    protected byte[] getKey(long latitude, long longitude, long id) {
        ByteBuffer byteBuffer = ByteBuffer.allocate(24);
        byteBuffer.putLong(latitude);
        byteBuffer.putLong(longitude);
        byteBuffer.putLong(id);
        return byteBuffer.array();
    }

    public void insert(long latitude, long longitude, long id, String drawable) throws IOException {
        DatabaseRequestResult<Object> result;
        result = geoTiles.singleInsert(0, getKey(latitude, longitude, id), drawable.getBytes(), null);
        try {
            result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while inserting: " + exception.getMessage());
        }
    }

    public void delete(long latitude, long longitude, long id) throws IOException {
        DatabaseRequestResult<Object> result;
        result = geoTiles.singleInsert(0, getKey(latitude, longitude, id), null, null);
        try {
            result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while deleting: " + exception.getMessage());
        }
    }

    public String getOne(long latitude, long longitude, long id) throws IOException {
        DatabaseRequestResult<byte[]> result = geoTiles.lookup(0, getKey(latitude, longitude, id), null);
        try {
            byte[] byteResult = result.get();
            if (byteResult == null) {
                return null;
            } else {
                return new String(byteResult);
            }
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException during lookup: " + exception.getMessage());
        }
    }

    public Set<String> getRange(long latitude, long minLongitude, long maxLongitude) throws IOException {
        byte[] emptyId = {-128, -128, -128, -128, -128, -128, -128, -128};

        // inclusive
        ByteBuffer from = ByteBuffer.allocate(24);
        from.putLong(latitude);
        from.putLong(minLongitude);
        from.put(emptyId);

        // exclusive
        ByteBuffer to = ByteBuffer.allocate(24);
        to.putLong(latitude);
        to.putLong(maxLongitude);
        to.put(emptyId);

        DatabaseRequestResult<ResultSet<byte[], byte[]>> result;
        result = geoTiles.rangeLookup(0, from.array(), to.array(), null);

        try {
            Iterator<Entry<byte[], byte[]>> iterator = result.get();

            Set<String> output = new java.util.HashSet<String>();
            while (iterator.hasNext()) {
                Entry<byte[], byte[]> keyValuePair = iterator.next();
                output.add(new String(keyValuePair.getValue()));
            }
            return output;
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException during lookup: " + exception.getMessage());
        }
    }

}
