import React, { useState } from "react";
import { AuthData } from "../../auth/AuthWrapper";
import api from "../../api/api"; 

export const GuestControls = () => {
    const { user } = AuthData();

    const [emailEnabled, setEmailEnabled] = useState(false);
    const [smsEnabled, setSmsEnabled] = useState(false);
    const [targetedAdEnabled, setTargetedAdEnabled] = useState(false);

    const updatePreference = async (name, value) => {
        try {
            const prefData = {
                preference_name: name,
                preference_value: value
            };

            await api.updatePref(prefData);
        } catch (error) {
            console.log(error);
        }
    };

	const handleToggle = (option, enabled) => {
        switch (option) {
            case "email_pref":
                setEmailEnabled(enabled);
                break;
            case "sms_pref":
                setSmsEnabled(enabled);
                break;
            case "targeted_adv_pref":
                setTargetedAdEnabled(enabled);
                break;
            default:
                break;
        }

        // call update to db
        updatePreference(option, enabled ? 1 : 0);
    };


    return (
        <div className="page">
            <h2>InCollege Guest Controls</h2>
            
            {user.token ? (
                <div>
                    <ToggleOption label="Email" enabled={emailEnabled} toggle={() => handleToggle("email_pref", !emailEnabled)} />
                    <ToggleOption label="SMS" enabled={smsEnabled} toggle={() => handleToggle("sms_pref", !smsEnabled)} />
                    <ToggleOption label="Targeted Ad" enabled={targetedAdEnabled} toggle={() => handleToggle("targeted_adv_pref", !targetedAdEnabled)} />
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
