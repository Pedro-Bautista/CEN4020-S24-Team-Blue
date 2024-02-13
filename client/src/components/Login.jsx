import { useReducer, useState } from "react"
import { useNavigate } from "react-router-dom"
import { AuthData } from "../auth/AuthWrapper"

export const Login = () => {

	const navigate = useNavigate()
	const { login } = AuthData()
	const [formData, setFormData] = useReducer((formData, newItem) =>{ return ({ ...formData, ...newItem }) }, { userName: "", password: "" })
	const [errorMessage, setErrorMessage] = useState(null)

	const handleLogin = async () => {
		console.log("Login", formData.userName, formData.password)
		try {
			await login(formData.userName, formData.password)
			navigate("/profile")
		} catch (error) {
			setErrorMessage(error.response.data.error.description)
		}

	}

	return (
		<div className="page">
			<h2>Login</h2>
			<div className="inputs">
				<div className="input">
					<input
						value={formData.userName}
						onChange={(e) => setFormData({ userName: e.target.value })}
						type="text"
						placeholder="Username"
					/>
				</div>
				<div className="input">
					<input
						value={formData.password}
						onChange={(e) => setFormData({ password: e.target.value })}
						type="password"
						placeholder="Password"
					/>
				</div>
				<div className="button">
					<button onClick={handleLogin}>Log in</button>
				</div>
				{errorMessage ?
					<div className="error">{errorMessage}</div>
					: null}
			</div>
		</div>
	)
}