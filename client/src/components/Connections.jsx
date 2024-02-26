import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from '../api/api';
import { AuthData } from "../auth/AuthWrapper"

export const Connections = () => {

    const [isOpen, setIsOpen] = useState(false);
    const [requests, setRequests] = useState([]);

    const { user } = AuthData();

    const toggleTab = () => {
        setIsOpen(!isOpen);
    };

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

    return (
        <div className="page">
            <button onClick={toggleTab}>Open Connection Requests</button>

            {isOpen && (
                <div>
                    <h2>Requests</h2>
                    {requests.length > 0 ? (
                        <ul>
                            {requests.map((request, index) => (
                                <li key={index}>{/* Render each request here */}
                                    <strong>Sender:</strong> {request.sender_user_id}<br />
                                    <strong>Receiver:</strong> {request.receiver_user_id}<br />
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No connection requests available.</p>
                    )}
                </div>
            )}
        </div>
    );

}