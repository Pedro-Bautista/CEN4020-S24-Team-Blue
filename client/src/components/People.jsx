import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from '../api/api';
import { AuthData } from "../auth/AuthWrapper"

export const People = () => {
    const [searchParams, setSearchParams] = useState({ first_name: "", last_name: "" });
    const [userFound, setUserFound] = useState(false);
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

	const { user } = AuthData();

    const handleSearch = async () => {
        setLoading(true);
        setUserFound(false);
        setErrorMessage("");
        try {
            const data = await api.searchForPeople(searchParams);
            setUserFound(true);
			console.log(user);
        } catch (error) {
            console.error("Search error:", error);
            setErrorMessage(error.response ? error.response.data.error.description : "An error occurred");
        } finally {
            setLoading(false);
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
                    onChange={(e) => setSearchParams({ ...searchParams, first_name: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="Last Name"
                    value={searchParams.last_name}
                    onChange={(e) => setSearchParams({ ...searchParams, last_name: e.target.value })}
                />
                <button onClick={handleSearch} disabled={loading}>
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
                </div>
            )}
        </div>
    );
};
