import React, { useState } from "react";
import { AuthData } from "../../auth/AuthWrapper";
import api from "../../api/api"; 

export const GuestControls = () => {
    const { user } = AuthData();

    const [emailEnabled, setEmailEnabled] = useState(false);
    const [smsEnabled, setSmsEnabled] = useState(false);
    const [targetedAdEnabled, setTargetedAdEnabled] = useState(false);

    const updateDatabase = async (option, value) => {
        try {
            if (user.token) {
                // using username for now (assuming all unique usernames)
                const prefData = {
                    user_id: user.user_id,
                    preference: option,
                    toggle: value
                };

                await api.updatePref(prefData);

                console.log(`Updated ${option} to ${value} in the database`);
            }
        } catch (error) {
            console.log(error);
        }
    };

	const handleToggle = (option, enabled) => {
        if (user.token) {
            
            switch (option) {
                case "email":
                    setEmailEnabled(enabled);
                    break;
                case "sms":
                    setSmsEnabled(enabled);
                    break;
                case "targetedAd":
                    setTargetedAdEnabled(enabled);
                    break;
                default:
                    break;
            }

            // call update to db
            updateDatabase(option, enabled ? 1 : 0);
        }
    };


    return (
        <div className="page">
            <h2>InCollege Guest Controls</h2>
            
            {user.token ? (
                <div>
                    <ToggleOption label="Email" enabled={emailEnabled} toggle={() => handleToggle("email", !emailEnabled)} />
                    <ToggleOption label="SMS" enabled={smsEnabled} toggle={() => handleToggle("sms", !smsEnabled)} />
                    <ToggleOption label="Targeted Ad" enabled={targetedAdEnabled} toggle={() => handleToggle("targetedAd", !targetedAdEnabled)} />
                </div>
            ) : (
                <p> Under Construction </p>
            )}
        </div>
    );
};


const ToggleOption = ({ label, enabled, toggle }) => {
    return (
        <div className="toggle-option">
            <label>
                <input type="checkbox" checked={enabled} onChange={toggle} />
                {label}
            </label>
        </div>
    );
};
