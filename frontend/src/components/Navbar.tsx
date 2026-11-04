
type Role = "student" | "alumni" | "faculty" | "admin"

interface NavbarProps {
  role: Role
  onRoleChange: (role: Role) => void
}

function Navbar({ role, onRoleChange }: NavbarProps) {
  const roleLabels: Record<Role, string> = {
    student: "Student",
    alumni: "Alumni",
    faculty: "Faculty",
    admin: "Admin",
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
        <select
          className="navbar-role-select"
          value={role}
          onChange={(event) => onRoleChange(event.target.value as Role)}
          aria-label="Select demo role"
        >
          {Object.entries(roleLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>

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
          <div className="profile-avatar">U</div>
          <div className="profile-info">
            <strong>IUBLink User</strong>
            <span>{roleLabels[role]}</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Navbar
