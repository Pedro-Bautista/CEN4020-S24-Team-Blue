import { AuthData } from "../auth/AuthWrapper";
import React, { useEffect, useState } from "react";
import api from "../api/api";


export const Profile = () => {
  const { user } = AuthData();
  const [userData, setUserData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  return (
      <div className="page">

        <div className="centered-content">
          <h1>Your Profile</h1>
          {loading && <p>Loading user data...</p>}
          {error && <p>{error}</p>}
          <div>
            {userData.map((data, index) => (
                <div key={index} className="profile-summary">
                  <div className={"page h1"}>
                    <h1>{`${data.first_name} ${data.last_name}`}</h1>
                    <h2>{data.university}</h2>
                    <h2>{data.major}</h2>
                    <div className={"profile Data"}>
                      <h1>About ME</h1>
                      <h3>{data.bio}</h3>
                    </div>

                    <div className={"profile Data"}>
                      <h1>Experience</h1>
                      <h3>{data.experience}</h3>
                    </div>
                    <div className={"profile Data"}>
                      <h1>Education</h1>
                      <h3>{data.education}</h3><br/>
                    </div>
                  </div>
                </div>
            ))}
          </div>
        </div>
      </div>
  );
};
