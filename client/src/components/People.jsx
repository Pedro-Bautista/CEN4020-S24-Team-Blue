import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from '../api/api';
import { AuthData } from "../auth/AuthWrapper"

export const People = () => {
    const [searchParams, setSearchParams] = useState({ first_name: "", last_name: "" ,university:"", major:""});
    const [userFound, setUserFound] = useState(false);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [data, setData] = useState([]);   // store return array

	const { user } = AuthData();


    const handleSearch = async () => {
        setLoading(true);
        setUserFound(false);
        setErrorMessage("");
        try {
            const responseData = await api.searchForPeople(searchParams);
            console.log("ALL THE PEOPLE: ", responseData);
            setData(responseData.message);
            if (responseData.message) {
                setUserFound(true);
            }
			console.log(user);
        } catch (error) {
            console.error("Search error:", error);
            setErrorMessage(error.response ? error.response.data.error.description : "An error occurred");
        } finally {
            setLoading(false);
        }
    };

    const handleConnectRequest = async (userId) => {

        try {
            await api.requestConnection({ sender_userID: user, receiver_userID: userId });
            console.log("Request sent to ", userId);
        } catch (error) {
            console.error("Connection request error:", error);
            setErrorMessage(error.response ? error.response.data.error.description : "An error occurred");
        }
    };

    return (
        <div className="page">
            <h2>Search People</h2>
            <div className="search">
                <input
                    type="text"
                    placeholder="First Name"
                    value={searchParams.first_name}
                    onChange={(e) => setSearchParams({...searchParams, first_name: e.target.value})}
                />
                <input
                    type="text"
                    placeholder="Last Name"
                    value={searchParams.last_name}
                    onChange={(e) => setSearchParams({...searchParams, last_name: e.target.value})}
                />
                <input
                    type="text"
                    placeholder="University"
                    value={searchParams.university}
                    onChange={(e) => setSearchParams({...searchParams, university: e.target.value})}
                />
                <input
                    type="text"
                    placeholder="Major"
                    value={searchParams.major}
                    onChange={(e) => setSearchParams({...searchParams, major: e.target.value})}
                />
                <button style={{marginLeft: '10px'}} onClick={handleSearch} disabled={loading}>
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </div>
            {errorMessage && <div className="error">{errorMessage}</div>}
            {userFound && (
                <div className="login-signup-prompt">
                    <p>They are a part of the InCollege system.</p>
                    {!user.token && (
                        <>
							<p>If you haven't signed in yet, please do so.</p>
							<Link to="/login"><button>Login</button></Link>
							<Link to="/signup"><button>Sign Up</button></Link>
						</>
					)}
                
                    {user.token && (
                        
                        <> 
                            {console.log(data)}
                            <h3>Search Results</h3>
                            <ul style={{ listStyleType: 'none' }}>
                                {data.map((user) => (
                                    <li key={user.user_id} style={{ marginBottom: '10px' }}>
                                        <span>{user.first_name} {user.last_name} {user.university} {user.major}</span>
                                        <button style={{ marginLeft: '10px' }} onClick={() => handleConnectRequest(user.user_id)}>Connect</button> 
                                    </li> 
                                ))}
                            </ul>
                        </>
                        
                    )}
                </div>
            )}
            {!userFound && (
                <div className="login-signup-prompt">
                    <p>They are not part of the InCollege system.</p>
					{!user.token && (
						<>
							<p>If you haven't signed in yet, please do so.</p>
							<Link to="/login"><button>Login</button></Link>
							<Link to="/signup"><button>Sign Up</button></Link>
						</>
					)}
                </div>
            )}
        </div>
    );
};

