import { useLocation } from "react-router-dom"

interface SidebarProps {
  role: string
}

interface MenuItem {
  label: string
  icon: string
  href: string
}

function Sidebar({ role }: SidebarProps) {
  const location = useLocation()

  const commonMenu: MenuItem[] = [
    { label: "Dashboard", icon: "•", href: "/dashboard" },
    { label: "Profile & Security", icon: "•", href: "/dashboard#profile" },
    { label: "Career Opportunities", icon: "•", href: "/dashboard#opportunities" },
  ]

  const adminMenu: MenuItem[] = [
    { label: "Post Moderation", icon: "•", href: "/dashboard#review" },
    { label: "User Moderation", icon: "•", href: "/dashboard#users" },
  ]

  const userMenu: MenuItem[] = [
    { label: "My Posts", icon: "•", href: "/dashboard#my-posts" },
  ]

  const items = [
    ...commonMenu,
    ...(role === "admin" ? adminMenu : userMenu),
  ]

  return (
    <aside className="sidebar" data-path={location.pathname}>
      <div className="sidebar-brand">
        <strong>IUBLink</strong>
        <span>CareerHub</span>
      </div>

      <nav className="sidebar-nav">
        {items.map((item) => (
          <a key={item.href} href={item.href} className="sidebar-link">
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
