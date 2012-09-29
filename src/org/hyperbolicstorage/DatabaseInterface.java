package org.hyperbolicstorage;

import java.io.IOException;

import org.xtreemfs.babudb.api.BabuDB;
import org.xtreemfs.babudb.api.DatabaseManager;
import org.xtreemfs.babudb.api.database.Database;
import org.xtreemfs.babudb.BabuDBFactory;
import org.xtreemfs.babudb.config.BabuDBConfig;
import org.xtreemfs.babudb.log.DiskLogger.SyncMode;
import org.xtreemfs.babudb.api.exception.BabuDBException;

public class DatabaseInterface {
    private BabuDB babuDB = null;
    private DatabaseManager databaseManager = null;
    private Database geographicalTiles = null;
    private Database drawingCommands = null;

    public DatabaseInterface() throws IOException {
        BabuDBConfig babuDBConfig = new BabuDBConfig("babudb/databases/", "babudb/dblog/", 1, 1024*1024*16, 5*60, SyncMode.FSYNC, 50, 0, false, 16, 1024*1024*512);

        try {
            babuDB = BabuDBFactory.createBabuDB(babuDBConfig);
            databaseManager = babuDB.getDatabaseManager();
            geographicalTiles = databaseManager.createDatabase("geographicalTiles", 5);
        }
        catch (BabuDBException exception) {
            throw new IOException("BabuDBException: " + exception.getMessage());
        }
    }

}
