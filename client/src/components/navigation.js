import { Profile } from "./Profile"
import { Home } from "./Home"
import { Login } from "./Login"
import { Signup } from "./Signup"
import { Jobs } from "./Jobs"
import { People } from "./People"
import { Learn } from "./Learn"
import { Connections } from "./Connections"

// Epic 3 added links ///////////////////////
// IMPORTANT LINKS
import { Accessibility } from "./important_links/Accessibility"
import { BrandPolicy } from "./important_links/BrandPolicy"
import { CookiePolicy } from "./important_links/CookiePolicy"
import { CopyrightNotice } from "./important_links/CopyrightNotice"
import { CopyrightPolicy } from "./important_links/CopyrightPolicy"
import { GuestControls } from "./important_links/GuestControls"
import { Languages } from "./important_links/Languages"
import { PrivacyPolicy } from "./important_links/PrivacyPolicy"
import { UserAgreement } from "./important_links/UserAgreement"


// USEFUL LINKS
import { About } from "./useful_links/About"
import { Blogs } from "./useful_links/Blogs"
import { Browse } from "./useful_links/Browse"
import { BusinessSolutions } from "./useful_links/BusinessSolutions"
import { Careers } from "./useful_links/Careers"
import { Developers } from "./useful_links/Developers"
import { Directories } from "./useful_links/Directories"
import { HelpCenter } from "./useful_links/HelpCenter"
import { Press } from "./useful_links/Press"



export const nav = [
	{ path:     "/",         name: "Home",        element: <Home />,       isMenu: true,     isPrivate: false  },
	{ path:     "/login",    name: "Login",       element: <Login />,      isMenu: false,    isPrivate: false  },
	{ path:     "/signup",   name: "Sign Up",     element: <Signup />,     isMenu: false,    isPrivate: false  },
	{ path:     "/jobs",     name: "Jobs",        element: <Jobs />,       isMenu: true,     isPrivate: true   },
	{ path:     "/people",   name: "People",      element: <People />,     isMenu: true,     isPrivate: false  },
	{ path:     "/learn",    name: "Learn",       element: <Learn />,      isMenu: true,     isPrivate: true   },
	{ path:     "/profile",  name: "Profile",     element: <Profile />,    isMenu: true,     isPrivate: true   },
	{ path:     "/connections",  name: "Connections",     element: <Connections />,    isMenu: true,     isPrivate: true   },
	{ path: 	"/important_links/Accessibility",	name: "Accessibility", 		element: <Accessibility />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/BrandPolicy",	name: "Brand Policy", 		element: <BrandPolicy />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/CookiePolicy",	name: "Cookie Policy", 		element: <CookiePolicy />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/CopyrightNotice",	name: "Copyright Notice", 		element: <CopyrightNotice />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/CopyrightPolicy",	name: "Copyright Policy", 		element: <CopyrightPolicy />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/GuestControls",	name: "Guest Controls", 		element: <GuestControls />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/Languages",	name: "Languages", 		element: <Languages />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/PrivacyPolicy",	name: "Privacy Policy", 		element: <PrivacyPolicy />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/important_links/UserAgreement",	name: "User Agreement", 		element: <UserAgreement />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/About",	name: "About", 		element: <About />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/Blogs",	name: "Blogs", 		element: <Blogs />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/Browse",	name: "Browse", 		element: <Browse />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/BusinessSolutions",	name: "Business Solutions", 		element: <BusinessSolutions />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/Careers",	name: "Careers", 		element: <Careers />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/Developers",	name: "Developers", 		element: <Developers />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/Directories",	name: "Directories", 		element: <Directories />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/HelpCenter",	name: "Help Center", 		element: <HelpCenter />,		isMenu: false, 	isPrivate: false},
	{ path: 	"/useful_links/Press",	name: "Press", 		element: <Press />,		isMenu: false, 	isPrivate: false},
]

