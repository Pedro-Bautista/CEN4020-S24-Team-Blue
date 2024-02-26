import { createContext, useContext, useState, useEffect } from "react"
import { RenderHeader } from "../components/Header"
import { RenderMenu, RenderRoutes } from "../components/RenderNavigation"
import api from "../api/api"

const AuthContext = createContext()
export const AuthData = () => useContext(AuthContext)

export const AuthWrapper = () => {

	const [user, setUser] = useState({ token: null, username: null})

	useEffect(() => {
		const token = localStorage.getItem("token")
		if (token) {
			setUser({ token })
		}
	}, []);

	const signup = async (formData) => {
		try {
			const response = await api.signup(formData)

			const token = response.data.token
			const username = formData.username
			localStorage.setItem("token", token)
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
			setUser({ token, username })

			return response

		} catch (error) {
			console.log(error)
			throw error
		}

	}

	const logout = () => {
		localStorage.removeItem("token")
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