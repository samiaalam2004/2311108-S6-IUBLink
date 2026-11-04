
import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

interface LoginResponse {
  access_token: string
  token_type: string
  user: {
    id: number
    full_name: string
    email: string
    role: string
  }
}

function Login() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    setError("")
    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      })

      const data: LoginResponse | { detail: string } =
        await response.json()

      if (!response.ok) {
        throw new Error(
          "detail" in data ? data.detail : "Login failed"
        )
      }

      const loginData = data as LoginResponse

      localStorage.setItem("access_token", loginData.access_token)
      localStorage.setItem("user", JSON.stringify(loginData.user))

      navigate("/dashboard")
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
        <h1>IUBLink Login</h1>

        <p>Welcome back to IUBLink!</p>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>

            <input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>

            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p>
          Don't have an account?{" "}
          <Link to="/register">Register here</Link>
        </p>

        <Link to="/">Back to Home</Link>
      </div>
    </div>
  )
}

export default Login
