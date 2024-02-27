import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from '../api/api';
import { AuthData } from "../auth/AuthWrapper"

export const Connections = () => {

    const [isOpen, setIsOpen] = useState(false);
    const [requests, setRequests] = useState([]);
    const [Connections, setConnections] = useState([]);

    const { user } = AuthData();

    const toggleTab = () => {
        setIsOpen(!isOpen);
    };

    useEffect(()=> {
        const fetchAccepted = async () => {
            try {
                const responseData = await api.getAccepted({});
                console.log("Accepted List", responseData);
                setConnections(responseData.message)
            } catch (error) {
                console.log(error);
            }
        };
        if (!isOpen) {
            fetchAccepted();
        }
    },[isOpen]);


    useEffect(() => {
        const fetchData = async () => {
    
            try {
                const responseData = await api.getRequests({});
                console.log("RESPONSE DATA: ", responseData);
                setRequests(responseData.message); 
            } catch (error) {
                console.log(error);
            }
        };

        if (isOpen) {
            fetchData(); 
        }
    }, [isOpen]);

    const handleAccept = async (requestId) => {
        // Function to handle accept request
        try {
            const status = 'accepted';
            await api.changeConnStatus({ request_id: requestId, status: status });
            console.log("Accept request with ID:", requestId);
        } catch (error) {
            console.error("Status change request error (acceptance):", error);
        }
    };

    const handleReject = async (requestId) => {
        // Function to handle reject request
        try {
            const status = 'rejected';
            await api.changeConnStatus({ request_id: requestId, status: status });
            console.log("Rejected request with ID:", requestId);
        } catch (error) {
            console.error("Status change request error (rejected):", error);
        }
    };


    return (
        <div className="page">

            <div className="Connections_List">
                {!isOpen && (
                    <div>
                        <h2>My Network</h2>
                        {Connections.length > 0 ? (
                            <div>
                                {Connections.map((Connection, index) => (
                                    <div key={index} className="request-box">
                                        <div className="request-text">
                                            <strong>Receiver:</strong> {Connection.receiver_user_id}<br/>
                                        </div>
                                        <div className="button-container">
                                            <button onClick={() => handleReject(Connection.request_id)}>Remove</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <h3>No Connections Made</h3>
                        )}
                    </div>
                )}
            </div>

            <div className="Request_List">
                <button onClick={toggleTab}>Open Connection Requests</button>
                {isOpen && (
                    <div>
                        <h2>Requests</h2>
                        {requests.length > 0 ? (
                            <div>
                                {requests.map((request, index) => (
                                    <div key={index} className="request-box">
                                        <div className="request-text">
                                            <strong>Sender:</strong> {request.sender_user_id}<br/>
                                            <strong>Receiver:</strong> {request.receiver_user_id}<br/>
                                        </div>
                                        <div className="button-container">
                                            <button onClick={() => handleAccept(request.request_id)}>Accept</button>
                                            <button onClick={() => handleReject(request.request_id)}>Reject</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p>No connection requests available.</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}


