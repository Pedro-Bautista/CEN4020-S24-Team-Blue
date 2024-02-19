import React, { useState } from "react";
import { AuthData } from "../../auth/AuthWrapper";
import api from "../../api/api"; 

export const Languages = () => {
	const { user } = AuthData();
	const [language, setSpanish] = useState(false);


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
            
			setSpanish(enabled)
            // call update to db
            updateDatabase(option, enabled ? 1 : 0);
        }
    };

	return (
		<div className="page">
			<h2>Languages</h2>
			{user.token ? (
                <div>
                    <ToggleOption label="Spanish" enabled={language} toggle={() => handleToggle("spanish", !language)} />
                </div>
            ) : (
                <p> Under Construction </p>
            )}
		</div>
	)
}

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