import { Link } from "react-router-dom"

function Login() {
  return (
    <div>
      <h1>IUBLink Login</h1>
      <p>Welcome back to IUBLink!</p>

      <p>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>

      <Link to="/">Back to Home</Link>
    </div>
  )
}

export default Login