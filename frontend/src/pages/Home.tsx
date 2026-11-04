import { Link } from "react-router-dom"

function Home() {
  return (
    <div>
      <h1>Welcome to IUBLink</h1>

      <p>
        Connect with IUB students, alumni, and faculty.
      </p>

      <nav>
        <Link to="/login">Login</Link>
        {" | "}
        <Link to="/register">Register</Link>
        {" | "}
        <Link to="/dashboard">Dashboard</Link>
      </nav>
    </div>
  )
}

export default Home