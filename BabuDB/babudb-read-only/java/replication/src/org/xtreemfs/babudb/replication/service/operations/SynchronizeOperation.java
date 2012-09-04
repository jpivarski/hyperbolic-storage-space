/*
 * Copyright (c) 2011, Jan Stender, Bjoern Kolbeck, Mikael Hoegqvist,
 *                     Felix Hupfeld, Felix Langner, Zuse Institute Berlin
 * 
 * Licensed under the BSD License, see LICENSE file for details.
 * 
 */
package org.xtreemfs.babudb.replication.service.operations;

import java.net.InetSocketAddress;

import org.xtreemfs.babudb.lsmdb.LSN;
import org.xtreemfs.babudb.pbrpc.GlobalTypes.ErrorCodeResponse;
import org.xtreemfs.babudb.pbrpc.GlobalTypes.HeartbeatMessage;
import org.xtreemfs.babudb.pbrpc.ReplicationServiceConstants;
import org.xtreemfs.babudb.replication.control.ControlLayerInterface;
import org.xtreemfs.babudb.replication.service.RequestManagement;
import org.xtreemfs.babudb.replication.transmission.ErrorCode;
import org.xtreemfs.babudb.replication.transmission.dispatcher.Operation;
import org.xtreemfs.babudb.replication.transmission.dispatcher.Request;
import org.xtreemfs.foundation.logging.Logging;

import com.google.protobuf.Message;

/**
 * <p>
 * {@link Operation} to send get forced by a potentially master to synchronize with its 
 * database state.
 * </p>
 * 
 * @since 03/29/2011
 * @author flangner
 */

public class SynchronizeOperation extends Operation {
    
    private final RequestManagement     rqMan;
    
    private final ControlLayerInterface control;
    
    public SynchronizeOperation(RequestManagement rqManagement, ControlLayerInterface control) {
        this.rqMan = rqManagement;
        this.control = control;
    }

    /*
     * (non-Javadoc)
     * @see org.xtreemfs.babudb.replication.service.operations.Operation#
     * getProcedureId()
     */
    @Override
    public int getProcedureId() {
        return ReplicationServiceConstants.PROC_ID_SYNCHRONIZE;
    }

    /* (non-Javadoc)
     * @see org.xtreemfs.babudb.replication.transmission.dispatcher.Operation#
     * getDefaultRequest()
     */
    @Override
    public Message getDefaultRequest() {
        return HeartbeatMessage.getDefaultInstance();
    }
    
    /* (non-Javadoc)
     * @see org.xtreemfs.babudb.replication.transmission.dispatcher.Operation#
     *          processRequest(org.xtreemfs.babudb.replication.transmission.dispatcher.Request)
     */
    @Override
    public void processRequest(Request rq) {
        
        HeartbeatMessage message = (HeartbeatMessage) rq.getRequestMessage();
        org.xtreemfs.babudb.pbrpc.GlobalTypes.LSN mLSN = message.getLsn();
        LSN lsn = new LSN(mLSN.getViewId(), mLSN.getSequenceNo());
            
        InetSocketAddress participant = new InetSocketAddress(
                rq.getSenderAddress().getAddress(), message.getPort());
        
        Logging.logMessage(Logging.LEVEL_INFO, this, "SynchronizeOperation:  received %s by %s", 
                lsn.toString(), participant.toString());
        
        try {
            rqMan.createStableState(lsn, participant, control);
            rq.sendSuccess(ErrorCodeResponse.getDefaultInstance());
        } catch (InterruptedException ie) {
            Logging.logMessage(Logging.LEVEL_WARN, this, "Participant was not able to establish " +
            		"stable state @ LSN (%s).", lsn.toString());
            rq.sendSuccess(ErrorCodeResponse.newBuilder().setErrorCode(
                    ErrorCode.SERVICE_UNAVAILABLE).build());
        }
    }
}