import { AuthData } from "../auth/AuthWrapper"

export const Profile = () => {

	const { user } = AuthData()

	return (
		<div className="page">
			<h2>Your Profile</h2>
			<p>Username: {user.username}</p>
		</div>
	)
}