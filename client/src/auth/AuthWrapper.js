import { createContext, useContext, useState, useEffect } from "react"
import { RenderHeader } from "../components/Header"
import { RenderMenu, RenderRoutes } from "../components/RenderNavigation"
import api from "../api/api"

const AuthContext = createContext()
export const AuthData = () => useContext(AuthContext)

export const AuthWrapper = () => {

	const [user, setUser] = useState({ token: null, username: null })

	useEffect(() => {
		const token = localStorage.getItem("token")
		const username = localStorage.getItem("username")
		if (token && username) {
			setUser({ token, username })
		}
	}, []);

	const signup = async (username, password) => {
		try {
			const response = await api.signup({ username, password })

			const token = response.data.token
			localStorage.setItem("token", token)
			localStorage.setItem("username", username)
			setUser({ token, username })

			return response
		
		} catch (error) {
			console.log(error)
			throw error
		}
	}

	const login = async (username, password) => {
		try {
			const response = await api.login({ username, password });

			const token = response.data.token
			localStorage.setItem("token", token)
			localStorage.setItem("username", username)
			setUser({ token, username })

			return response

		} catch (error) {
			console.log(error)
			throw error
		}

	}

	const logout = () => {
		localStorage.removeItem("token")
		localStorage.removeItem("username")
		setUser({ token: null, username: null })
	}

	return (

		<AuthContext.Provider value={{ user, signup, login, logout }}>
			<>
				<RenderHeader />
				<RenderMenu />
				<RenderRoutes />
			</>

		</AuthContext.Provider>

	)

}