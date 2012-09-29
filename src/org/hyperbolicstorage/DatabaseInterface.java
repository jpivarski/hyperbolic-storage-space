package org.hyperbolicstorage;

import java.io.IOException;

import org.xtreemfs.babudb.api.BabuDB;
import org.xtreemfs.babudb.api.DatabaseManager;
import org.xtreemfs.babudb.api.database.Database;
import org.xtreemfs.babudb.api.database.DatabaseRequestResult;
import org.xtreemfs.babudb.BabuDBFactory;
import org.xtreemfs.babudb.config.BabuDBConfig;
import org.xtreemfs.babudb.log.DiskLogger.SyncMode;
import org.xtreemfs.babudb.api.exception.BabuDBException;

public class DatabaseInterface {
    private BabuDB babuDB = null;
    private DatabaseManager databaseManager = null;
    private Database geographicalTiles = null;
    private Database drawingCommands = null;

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
            geographicalTiles = databaseManager.getDatabase("geographicalTiles");
            drawingCommands = databaseManager.getDatabase("drawingCommands");
        }
        catch (BabuDBException ignoreException) {
            try {
                geographicalTiles = databaseManager.createDatabase("geographicalTiles", 1);
                drawingCommands = databaseManager.createDatabase("drawingCommands", 1);
            }
            catch (BabuDBException exception) {
                throw new IOException("BabuDBException while creating databases: " + exception.getMessage());
            }
        }
    }

    public void close() throws IOException {
        try {
            babuDB.shutdown();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while closing: " + exception.getMessage());
        }
    }

    public void insertGeographical(byte[] key, byte[] value) throws IOException {
        DatabaseRequestResult<Object> result = geographicalTiles.singleInsert(0, key, value, null);
        try {
            result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while inserting to geographicalTiles: " + exception.getMessage());
        }
    }

    public void deleteGeographical(byte[] key) throws IOException {
        DatabaseRequestResult<Object> result = geographicalTiles.singleInsert(0, key, null, null);
        try {
            result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while deleting from geographicalTiles: " + exception.getMessage());
        }
    }

    public byte[] getGeographical(byte[] key) throws IOException {
        DatabaseRequestResult<byte[]> result = geographicalTiles.lookup(0, key, null);
        try {
            return result.get();
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException while lookup up a value in geographicalTiles: " + exception.getMessage());
        }
    }


}
