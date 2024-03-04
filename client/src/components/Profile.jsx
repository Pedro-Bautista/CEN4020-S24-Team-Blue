import { AuthData } from "../auth/AuthWrapper";
import React, { useEffect, useState } from "react";
import api from "../api/api";

export const Profile = () => {
  const { user } = AuthData();
  const [userData, setUserData] = useState([]);

  useEffect(() => {
    const handleUserData = async () => {
      try {
        const responseData = await api.getUserData({});
        console.log("User Data", responseData);
        setUserData(responseData.message);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    // Call handleUserData when the component mounts
    handleUserData();
  }, []); // Empty dependency array ensures it runs only once when the component mounts

  return (
    <div className="page">
      <h2>Your Profile</h2>
      <div>
        <h2>BYE</h2>
        {userData.map((data, index) => (
          <div key={index} className="profile-summary">
            <h2>HEY</h2>
            <div className={"Basic data"}>
				{`${data.first_name} ${data.last_name}`}<br/>
			</div>
          </div>
        ))}
      </div>
    </div>
  )
}
