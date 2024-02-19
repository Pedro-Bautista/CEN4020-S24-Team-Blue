import { Link, Route, Routes } from "react-router-dom"
import { AuthData } from "../auth/AuthWrapper"
import { nav } from "./navigation"


export const RenderRoutes = () => {

	const { user } = AuthData()

	return (
		<Routes>
			{nav.map((r, i) => {

				if (r.isPrivate && user.token) {
					return <Route key={i} path={r.path} element={r.element} />
				} else if (!r.isPrivate) {
					return <Route key={i} path={r.path} element={r.element} />
				} else return false
			})}

		</Routes>
	)
}

export const RenderMenu = () => {

	const { user, logout } = AuthData()

	const MenuItem = ({ r }) => {
		return (
			<div className="menuItem"><Link to={r.path}>{r.name}</Link></div>
		)
	};

	const DropdownMenuItem = ({ r }) => {
		const handleMouseEnter = () => {
			const dropdownContent = document.getElementById(`${r.name.replace(/\s/g, '-')}-dropdown-content`);
			if (dropdownContent) {
				dropdownContent.style.display = 'block';
			}
		};
	
		const handleMouseLeave = () => {
			const dropdownContent = document.getElementById(`${r.name.replace(/\s/g, '-')}-dropdown-content`);
			if (dropdownContent) {
				dropdownContent.style.display = 'none';
			}
		};
	
		return (
			<div className="menuItem dropdown" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
				<button className="dropbtn">{r.name}</button>
				<div className="dropdown-content" id={`${r.name.replace(/\s/g, '-')}-dropdown-content`}>
					{r.submenu.map((subItem, index) => (
						<Link key={index} to={subItem.path}>{subItem.name}</Link>
					))}
				</div>
			</div>
		);
	};



	return (
		<div className="menu">
			{nav.map((r, i) => {

				if (!r.isPrivate && r.isMenu) {
					return (
						<MenuItem key={i} r={r} />
					)
				} else if (user.token && r.isMenu) {
					return (
						<MenuItem key={i} r={r} />
					)
				} else return false
			})}

			{user.token ?
				<div className="menuItem"><Link to={'/'} onClick={logout}>Log out</Link></div>
				:
				<>
					<div className="menuItem"><Link to={'/login'}>Log in</Link></div>
					<div className="menuItem"><Link to={'/signup'}>Sign up</Link></div>
					
					<DropdownMenuItem r={{
                        name: 'Important Links',
                        submenu: [
                            { name: 'Accessibility', path: '/important_links/Accessibility' },
                            { name: 'Brand Policy', path: '/important_links/BrandPolicy' },
                            { name: 'Cookie Policy', path: '/important_links/CookiePolicy' },
                            { name: 'Copyright Notice', path: '/important_links/CopyrightNotice' },
                            { name: 'Copyright Policy', path: '/important_links/CopyrightPolicy' },
                            { name: 'Guest Controls', path: '/important_links/GuestControls' },
                            { name: 'Languages', path: '/important_links/Languages' },
                            { name: 'Privacy Policy', path: '/important_links/PrivacyPolicy' },
                            { name: 'User Agreement', path: '/important_links/UserAgreement' },
                        ]
                    }} />

					<DropdownMenuItem r={{
                        name: 'Useful Links',
                        submenu: [
                            { name: 'About', path: '/useful_links/About' },
                            { name: 'Blogs', path: '/useful_links/Blogs' },
                            { name: 'Browse', path: '/useful_links/Browse' },
                            { name: 'BusinessSolutions', path: '/useful_links/BusinessSolutions' },
                            { name: 'Careers', path: '/useful_links/Careers' },
                            { name: 'Developers', path: '/useful_links/Developers' },
                            { name: 'Directories', path: '/useful_links/Directories' },
                            { name: 'HelpCenter', path: '/useful_links/HelpCenter' },
                            { name: 'Press', path: '/useful_links/Press' },
                        ]
                    }} />
				</>
			}
		</div>
	)
}