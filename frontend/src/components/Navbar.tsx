
import { useNavigate } from "react-router-dom"

type Role = "student" | "alumni" | "faculty" | "admin"

interface User {
  full_name: string
  email: string
  role: Role
}

interface NavbarProps {
  user: User
}

function Navbar({ user }: NavbarProps) {
  const navigate = useNavigate()

  const roleLabels: Record<Role, string> = {
    student: "Student",
    alumni: "Alumni",
    faculty: "Faculty",
    admin: "Admin",
  }

  function handleLogout() {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user")
    navigate("/login")
  }

  return (
    <header className="navbar">
      <div className="navbar-heading">
        <div>
          <h2>Dashboard</h2>
          <p>Welcome back! Here's what's happening.</p>
        </div>
      </div>

      <div className="navbar-actions">
        <button
          type="button"
          className="notification-btn"
          aria-label="Notifications"
          title="Notifications"
        >
          <span>♢</span>
          <i />
        </button>

        <div className="navbar-profile">
          <div className="profile-avatar">
            {user.full_name.charAt(0).toUpperCase()}
          </div>

          <div className="profile-info">
            <strong>{user.full_name}</strong>
            <span>{roleLabels[user.role]}</span>
          </div>
        </div>

        <button
          type="button"
          className="logout-btn"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    </header>
  )
}

export default Navbar
