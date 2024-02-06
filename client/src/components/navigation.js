import { Profile } from "./Profile"
import { Home } from "./Home"
import { Login } from "./Login"
import { Signup } from "./Signup"
import { Jobs } from "./Jobs"
import { People } from "./People"
import { Learn } from "./Learn"


export const nav = [
	{ path:     "/",         name: "Home",        element: <Home />,       isMenu: true,     isPrivate: false  },
	{ path:     "/login",    name: "Login",       element: <Login />,      isMenu: false,    isPrivate: false  },
	{ path:     "/signup",   name: "Sign Up",     element: <Signup />,     isMenu: false,    isPrivate: false  },
	{ path:     "/jobs",     name: "Jobs",        element: <Jobs />,       isMenu: true,     isPrivate: true   },
	{ path:     "/people",   name: "People",      element: <People />,     isMenu: true,     isPrivate: true   },
	{ path:     "/learn",    name: "Learn",       element: <Learn />,      isMenu: true,     isPrivate: true   },
	{ path:     "/profile",  name: "Profile",     element: <Profile />,    isMenu: true,     isPrivate: true   },
]