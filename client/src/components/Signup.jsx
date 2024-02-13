import { useReducer, useState } from "react"
import { useNavigate } from "react-router-dom"
import { AuthData } from "../auth/AuthWrapper"

export const Signup = () => {
	const navigate = useNavigate()
	const { signup } = AuthData()
	const [formData, setFormData] = useReducer(
		(state, newState) => ({ ...state, ...newState }),
		{ username: "", password: "", first_name: "", last_name: "" }
	)

	const [errorMessage, setErrorMessage] = useState(null)

	const handleSignup = async () => {
		try {
			await signup(formData)
			navigate("/profile")
		} catch (error) {
			setErrorMessage(error.response.data.error.description)
		}
	}

	return (
		<div className="page">
			<h2>Sign Up</h2>
			<div className="inputs">
				<div className="input">
					<input
						value={formData.username}
						onChange={(e) => setFormData({ username: e.target.value })}
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
				<div className="input">
					<input
						value={formData.first_name}
						onChange={(e) => setFormData({ first_name: e.target.value })}
						type="text"
						placeholder="First Name"
					/>
				</div>
				<div className="input">
					<input
						value={formData.last_name}
						onChange={(e) => setFormData({ last_name: e.target.value })}
						type="text"
						placeholder="Last Name"
					/>
				</div>
				<div className="button">
					<button onClick={handleSignup}>Sign Up</button>
				</div>
				{errorMessage && <div className="error">{errorMessage}</div>}
			</div>
		</div>
	)
}
