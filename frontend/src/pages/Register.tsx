import { useState, type FormEvent } from "react"
import { Link, useNavigate } from "react-router-dom"
import { apiData, apiFetch } from "../services/api"

function Register() {
  const navigate = useNavigate()

  const [fullName, setFullName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [department, setDepartment] = useState("")
  const [batchOrGraduation, setBatchOrGraduation] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleRegister(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()

    setError("")
    setLoading(true)

    try {
      const response = await apiFetch("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({
          full_name: fullName.trim(),
          email: email.trim(),
          password,
        }),
      })

      await apiData<{ message: string }>(response)

      if (department.trim() || batchOrGraduation.trim()) {
        const loginRes = await apiFetch("/api/auth/login", {
          method: "POST",
          body: JSON.stringify({
            email: email.trim(),
            password,
          }),
        })
        if (loginRes.ok) {
          await apiFetch("/api/users/me", {
            method: "PATCH",
            body: JSON.stringify({
              department: department.trim() || null,
              batch_or_graduation: batchOrGraduation.trim() || null,
            }),
          })
          await apiFetch("/api/auth/logout", { method: "POST" })
        }
      }

      alert("Account created successfully! Please log in.")
      navigate("/login")
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong. Please try again."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Create an Account</h1>
        <p>Join the IUBLink community!</p>

        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label htmlFor="fullName">Full Name</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Enter your full name"
              minLength={2}
              maxLength={100}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password (min 8 characters)"
              minLength={8}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="department">Department (Optional)</label>
            <input
              id="department"
              type="text"
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              placeholder="e.g., CSE"
            />
          </div>

          <div className="form-group">
            <label htmlFor="batch">Batch / Graduation Year (Optional)</label>
            <input
              id="batch"
              type="text"
              value={batchOrGraduation}
              onChange={(e) => setBatchOrGraduation(e.target.value)}
              placeholder="e.g., 2026"
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Creating Account..." : "Register"}
          </button>
        </form>

        <p>
          Already have an account?{" "}
          <Link to="/login">Login here</Link>
        </p>

        <Link to="/">Back to Home</Link>
      </div>
    </div>
  )
}

export default Register
