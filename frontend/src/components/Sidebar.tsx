
import { Link, useLocation } from "react-router-dom"

type Role = "student" | "alumni" | "faculty" | "admin"

interface SidebarProps {
  role: Role
}

interface MenuItem {
  label: string
  icon: string
  href: string
}

function Sidebar({ role }: SidebarProps) {
  const location = useLocation()

  const commonMenu: MenuItem[] = [
    { label: "Dashboard", icon: "▦", href: "/dashboard" },
  ]

  const roleMenus: Record<Role, MenuItem[]> = {
    student: [
      { label: "Career Opportunities", icon: "💼", href: "/dashboard#opportunities" },
      { label: "My Posts", icon: "📝", href: "/dashboard#my-posts" },
      { label: "Alumni Directory", icon: "👥", href: "/dashboard#alumni" },
      { label: "Mentorship", icon: "🎓", href: "/dashboard#mentorship" },
      { label: "Events", icon: "📅", href: "/dashboard#events" },
    ],
    alumni: [
      { label: "Career Opportunities", icon: "💼", href: "/dashboard#opportunities" },
      { label: "My Posts", icon: "📝", href: "/dashboard#my-posts" },
      { label: "Students", icon: "👥", href: "/dashboard#students" },
      { label: "Mentorship", icon: "🎓", href: "/dashboard#mentorship" },
      { label: "Events", icon: "📅", href: "/dashboard#events" },
    ],
    faculty: [
      { label: "Career Opportunities", icon: "💼", href: "/dashboard#opportunities" },
      { label: "Students", icon: "👥", href: "/dashboard#students" },
      { label: "Alumni Directory", icon: "🎓", href: "/dashboard#alumni" },
      { label: "Events", icon: "📅", href: "/dashboard#events" },
    ],
    admin: [
      { label: "User Management", icon: "👥", href: "/dashboard#users" },
      { label: "Post Review", icon: "📋", href: "/dashboard#review" },
      { label: "Events Management", icon: "📅", href: "/dashboard#events" },
      { label: "Reports", icon: "📊", href: "/dashboard#reports" },
    ],
  }

  function isActive(href: string) {
    const [path, hash] = href.split("#")

    return (
      location.pathname === path &&
      (hash ? location.hash === `#${hash}` : !location.hash)
    )
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">I</div>
        <div>
          <h2>IUBLink</h2>
          <span>CareerHub</span>
        </div>
      </div>

      <div className="sidebar-menu">
        <p className="sidebar-label">MAIN MENU</p>

        {commonMenu.map((item) => (
          <Link
            key={item.label}
            to={item.href}
            className={`nav-link ${isActive(item.href) ? "active" : ""}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}

        <p className="sidebar-label">WORKSPACE</p>

        {roleMenus[role].map((item) => (
          <Link
            key={item.label}
            to={item.href}
            className={`nav-link ${isActive(item.href) ? "active" : ""}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-help-icon">?</div>
        <div>
          <strong>Need Help?</strong>
          <p>Contact IUBLink Support</p>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
