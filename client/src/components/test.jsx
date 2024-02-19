export const RenderMenu = () => {
    const { user, logout } = AuthData();

    const MenuItem = ({ r }) => {
        return (
            <div className="menuItem"><Link to={r.path}>{r.name}</Link></div>
        );
    };

    const DropdownMenuItem = ({ r }) => {
        return (
            <div className="menuItem dropdown">
                <button className="dropbtn">{r.name}</button>
                <div className="dropdown-content">
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
                    return <MenuItem key={i} r={r} />;
                } else if (user.token && r.isMenu) {
                    return <MenuItem key={i} r={r} />;
                } else return false;
            })}
            {user.token ? (
                <div className="menuItem">
                    <Link to={'/'} onClick={logout}>Log out</Link>
                </div>
            ) : (
                <>
                    <div className="menuItem"><Link to={'/login'}>Log in</Link></div>
                    <div className="menuItem"><Link to={'/signup'}>Sign up</Link></div>
                    <DropdownMenuItem r={{
                        name: 'More Pages',
                        submenu: [
                            { name: 'Accessibility', path: '/important_links/accessibility' },
                            // Add more submenu items here as needed
                        ]
                    }} />
                </>
            )}
        </div>
    );
};
