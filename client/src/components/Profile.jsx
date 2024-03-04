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
        const user=responseData.user
        setUserData([user]);
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

  const handleUpdate = async () => {
  try {
    // Assuming userData[0] is an object with multiple preferences
    const preferencesToUpdate = {
      university: userData[0].university,
      major: userData[0].major,
      bio: userData[0].bio,
      experience: userData[0].experience,
      education: userData[0].education,
    };

    // Iterate through each preference and make individual API calls
    for (const preferenceName in preferencesToUpdate) {
      const preferenceValue = preferencesToUpdate[preferenceName];

      try {
        // Send the updated user data to the server
        const response = await api.updatePref({
          preference_name: preferenceName,
          preference_value: preferenceValue,
        });

      }  catch (error) {
        if (error.response && error.response.status === 503) {
          // Handle 503 error (Service Unavailable) as a successful update
          console.log(`No changes detected for ${preferenceName}. Update considered successful.`);
        } else {
          // Re-throw other errors
          throw error;
        }
      }}
    // Disable editing mode after attempting updates
    setIsEditing(false);

  } catch (error) {
    console.error("Error updating user data:", error);
    // Handle the error, e.g., display an error message to the user
  }
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
                      onChange={(e) => handleFieldChange('major', e.target.value)}
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
                {isEditing ? (
                    <button onClick={()=>{setIsEditing(false);handleUpdate();}}>Save</button>
                  ) : (
                    <button onClick={()=>{setIsEditing(true);handleEdit();}}>Edit</button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
