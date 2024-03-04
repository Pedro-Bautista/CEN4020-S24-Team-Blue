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
  const [errorMessage, setErrorMessage] = useState(null)

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
        }
        if (error.response && error.response.status===409){
          setErrorMessage(error.response.data.error.description)
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

                <h1>{`${data.first_name} ${data.last_name}`}</h1>
                <div className="profile-section">
                <h2>University</h2>
                {isEditing ?(
                    <textarea
                        className={"profile-section editing"}
                      value={data.university}
                      onChange={(e) => handleFieldChange('university', e.target.value)}
                      />

                ): (
                    <h3>{data.university}</h3>
                )}
                </div>

                <div className="profile-section">
                <h2>Major</h2>
                {isEditing ?(
                    <textarea
                        className={"profile-section editing"}
                      value={data.major}
                      onChange={(e) => handleFieldChange('major', e.target.value)}
                      />
                ): (
                    <h3>{data.major}</h3>
                )}
                </div>

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
                    <button onClick={()=>{
                      if (userData[0].education.trim() === '') {
                          // Show an alert if education is empty
                          alert('Education cannot be empty. Please fill in the field.');
                        } else {
                          setIsEditing(false);
                          handleUpdate();
                        }
                      }}

                    >
                      Save
                    </button>
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
