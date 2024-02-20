import React, { useState } from "react";
import { AuthData } from "../../auth/AuthWrapper";
import api from "../../api/api"; 

export const Languages = () => {
	const { user } = AuthData();
	const [language, setSpanish] = useState(false);


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
        setSpanish(enabled)
        // call update to db
        updatePreference(option, enabled ? "spanish" : "english");
    };

	return (
		<div className="page">
			<h2>Languages</h2>
			{user.token ? (
                <div>
                    <ToggleOption label="Spanish" enabled={language} toggle={() => handleToggle("language_pref", !language)} />
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