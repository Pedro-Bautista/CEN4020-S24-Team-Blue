// Profile.js

import { AuthData } from "../auth/AuthWrapper";
import React, { useEffect, useState } from "react";
import api from "../api/api";


export const Profile = () => {
  const { user } = AuthData();
  const [userData, setUserData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const handleUserData = async () => {
      try {
        const responseData = await api.getUserData({});
        console.log("User Data", responseData);
        setUserData(responseData.message);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setError("Error fetching user data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    // Call handleUserData when the component mounts
    handleUserData();
  }, []); // Empty dependency array ensures it runs only once when the component mounts

  const handleEdit = () => {
    setIsEditing(!isEditing);
  };

  const handleFieldChange = (field, value) => {
    setUserData([{ ...userData[0], [field]: value }]);
  };

  return (
    <div className="page">
      <div className="centered-content">
        <h1>Your Profile</h1>
        {loading && <p>Loading user data...</p>}
        {error && <p>{error}</p>}
        <div>
          {userData.map((data, index) => (
            <div key={index} className="profile-summary">
              <div className={`page h1 ${isEditing ? 'editing' : ''}`}>
                {isEditing ?(
                    <textarea
                        className={"profile-section editing"}
                      value={`${data.first_name} ${data.last_name}`}
                      onChange={(e) => handleFieldChange('first_name', e.target.value)}
                      />

                ):(
                <h1>{`${data.first_name} ${data.last_name}`}</h1>
                    )}

                {isEditing ?(
                    <textarea
                        className={"profile-section editing"}
                      value={data.university}
                      onChange={(e) => handleFieldChange('university', e.target.value)}
                      />

                ): (
                    <h2>{data.university}</h2>
                )}

                {isEditing ?(
                    <textarea
                        className={"profile-section editing"}
                      value={data.major}
                      onChange={(e) => handleFieldChange('university', e.target.value)}
                      />
                ): (
                    <h2>{data.major}</h2>
                )}

                <div className="profile-section">
                  <h1>About Me</h1>
                  {isEditing ? (
                    <textarea
                        className={"profile-section editing"}
                      value={data.bio}
                      onChange={(e) => handleFieldChange('bio', e.target.value)}
                    />
                  ) : (
                    <h3>{data.bio}</h3>
                  )}
                </div>

                <div className="profile-section">
                  <h1>Experience</h1>
                  {isEditing ? (
                    <textarea
                        className={"profile-section editing"}
                      value={data.experience}
                      onChange={(e) => handleFieldChange('experience', e.target.value)}
                    />
                  ) : (
                    <h3>{data.experience}</h3>
                  )}
                </div>

                <div className="profile-section">
                  <h1>Education</h1>
                  {isEditing ? (
                    <textarea
                        className={"profile-section editing"}
                      value={data.education}
                      onChange={(e) => handleFieldChange('education', e.target.value)}
                    />
                  ) : (
                    <h3>{data.education}</h3>
                  )}
                </div>
                <div className={"button-container"}>
                <button onClick={handleEdit}>{isEditing ? "Save" : "Edit"}</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
