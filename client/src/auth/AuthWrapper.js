import { createContext, useContext, useState, useEffect } from "react"
import { RenderHeader } from "../components/Header"
import { RenderMenu, RenderRoutes } from "../components/RenderNavigation"
import api from "../api/api"

const AuthContext = createContext()
export const AuthData = () => useContext(AuthContext)

export const AuthWrapper = () => {
    const [user, setUser] = useState({ token: null, username: null, user_id: null });

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem("token");
            if (token) {
                try {
                    const userData = await api.getUserData({});
                    setUser({
                        token: token,
                        username: userData.user.username,
                        user_id: userData.user.user_id,
                    });
                } catch (error) {
                    console.error("Error fetching user data:", error);
					localStorage.removeItem("token");
                }
            }
        };

        fetchUserData();
    }, []);

    const signup = async (formData) => {
        try {
            const response = await api.signup(formData);
            const { token, username } = response.data;
            localStorage.setItem("token", token);
            setUser({ token, username });
            return response;
        } catch (error) {
            console.error("Signup error:", error);
            throw error;
        }
    };

    const login = async (username, password) => {
        try {
            const response = await api.login({ username, password });
            const { token } = response.data;
            localStorage.setItem("token", token);
            setUser({ token, username });
            return response;
        } catch (error) {
            console.error("Login error:", error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser({ token: null, username: null, user_id: null });
    };

    return (
        <AuthContext.Provider value={{ user, signup, login, logout }}>
            <>
                <RenderHeader />
                <RenderMenu />
                <RenderRoutes />
            </>
        </AuthContext.Provider>
    );
};