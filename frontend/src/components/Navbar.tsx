import { useNavigate } from "react-router-dom"
import { apiFetch, setStoredToken } from "../api/client"

interface User {
  full_name: string
  email: string
  role: string
}

interface NavbarProps {
  user: User
}

function Navbar({ user }: NavbarProps) {
  const navigate = useNavigate()

  const roleLabels: Record<string, string> = {
    user: "Member",
    admin: "Admin",
    student: "Student",
    alumni: "Alumni",
    faculty: "Faculty",
  }

  async function handleLogout() {
    try {
      await apiFetch("/api/auth/logout", {
        method: "POST",
      })
    } catch {
      // Ignore network errors on logout and clear local state anyway
    } finally {
      setStoredToken(null)
      localStorage.removeItem("user")
      navigate("/login")
    }
  }

  const displayName = user.full_name || "User"
  const roleText = roleLabels[user.role] || user.role

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
          <span>&#9826;</span>
          <i />
        </button>

        <div className="navbar-profile">
          <div className="profile-avatar">
            {displayName.charAt(0).toUpperCase()}
          </div>

          <div className="profile-info">
            <strong>{displayName}</strong>
            <span>{roleText}</span>
          </div>
        </div>

        <button
          type="button"
          className="logout-btn"
          onClick={() => void handleLogout()}
        >
          Logout
        </button>
      </div>
    </header>
  )
}

export default Navbar
