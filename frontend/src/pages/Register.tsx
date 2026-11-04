import { Link } from "react-router-dom"

function Register() {
  return (
    <div>
      <h1>Create an Account</h1>
      <p>Join the IUBLink community!</p>

      <p>
        Already have an account? <Link to="/login">Login here</Link>
      </p>

      <Link to="/">Back to Home</Link>
    </div>
  )
}

export default Register