
import { useEffect, useState, type FormEvent } from "react"
import "./App.css"

const API = "http://127.0.0.1:8000"

type Role = "student" | "alumni" | "admin"
type PostType = "job_seeking" | "job" | "internship"

type Post = {
  id: number
  title: string
  description: string
  post_type: PostType
  company: string | null
  owner_id: string
  owner_name: string
  owner_role: string
  status: string
  review_note: string | null
  created_at: string
}

async function apiData<T>(response: Response): Promise<T> {
  const data = await response.json()
  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : JSON.stringify(data.detail)
    )
  }
  return data as T
}

export default function App() {
  const [role, setRole] = useState<Role>("student")
  const [posts, setPosts] = useState<Post[]>([])
  const [myPosts, setMyPosts] = useState<Post[]>([])
  const [adminPosts, setAdminPosts] = useState<Post[]>([])
  const [detail, setDetail] = useState<Post | null>(null)

  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [company, setCompany] = useState("")
  const [postType, setPostType] = useState<PostType>("job_seeking")
  const [editingId, setEditingId] = useState<number | null>(null)

  const [message, setMessage] = useState("")
  const [error, setError] = useState("")

  const ownerId = role === "student" ? "student-001" : "alumni-001"
  const ownerName = role === "student" ? "Demo Student" : "Demo Alumni"

  async function refreshData() {
    try {
      setError("")

      const publicResponse = await fetch(`${API}/api/posts`)
      setPosts(await apiData<Post[]>(publicResponse))

      if (role === "admin") {
        const response = await fetch(`${API}/api/admin/posts?status=pending`)
        setAdminPosts(await apiData<Post[]>(response))
        setMyPosts([])
      } else {
        const response = await fetch(
          `${API}/api/my-posts?owner_id=${encodeURIComponent(ownerId)}`
        )
        setMyPosts(await apiData<Post[]>(response))
        setAdminPosts([])
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load posts")
    }
  }

  useEffect(() => {
    void refreshData()
  }, [role])

  function resetForm() {
    setTitle("")
    setDescription("")
    setCompany("")
    setEditingId(null)
    setPostType(role === "student" ? "job_seeking" : "job")
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setMessage("")
    setError("")

    const commonData = {
      title,
      description,
      company: company.trim() || null,
    }

    try {
      let response: Response

      if (editingId !== null) {
        response = await fetch(
          `${API}/api/posts/${editingId}?owner_id=${encodeURIComponent(ownerId)}`,
          {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(commonData),
          }
        )
      } else {
        response = await fetch(`${API}/api/posts`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            ...commonData,
            post_type: postType,
            owner_id: ownerId,
            owner_name: ownerName,
            owner_role: role,
          }),
        })
      }

      await apiData<Post>(response)
      setMessage(editingId !== null ? "Post updated!" : "Post submitted for approval!")
      resetForm()
      await refreshData()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong")
    }
  }

  function startEdit(post: Post) {
    setEditingId(post.id)
    setTitle(post.title)
    setDescription(post.description)
    setCompany(post.company || "")
    setMessage("")
    setError("")
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  async function deletePost(id: number) {
    if (!window.confirm("Are you sure you want to delete this post?")) return

    try {
      const response = await fetch(
        `${API}/api/posts/${id}?owner_id=${encodeURIComponent(ownerId)}`,
        { method: "DELETE" }
      )
      await apiData<{ message: string }>(response)
      setMessage("Post deleted successfully!")
      await refreshData()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed")
    }
  }

  async function reviewPost(id: number, status: "approved" | "rejected") {
    try {
      const response = await fetch(`${API}/api/admin/posts/${id}/review`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          status,
          review_note: status === "approved" ? "Approved by admin." : "Rejected by admin.",
        }),
      })
      await apiData<Post>(response)
      setMessage(`Post ${status}!`)
      await refreshData()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Review failed")
    }
  }

  async function showDetails(id: number) {
    try {
      const response = await fetch(`${API}/api/posts/${id}`)
      setDetail(await apiData<Post>(response))
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not load details")
    }
  }

  function postTypeLabel(type: PostType) {
    if (type === "job_seeking") return "Job Seeking"
    if (type === "internship") return "Internship"
    return "Job Opportunity"
  }

  return (
    <main className="app">
      <header className="header">
        <div>
          <h1>IUBLink CareerHub</h1>
          <p>Connect. Explore. Grow.</p>
        </div>
        <span className="brand-tag">IUB CSE</span>
      </header>

      <section className="role-section">
        <label htmlFor="role">Choose demo role:</label>
        <select
          id="role"
          value={role}
          onChange={(e) => {
            setRole(e.target.value as Role)
            resetForm()
            setDetail(null)
            setMessage("")
          }}
        >
          <option value="student">Student</option>
          <option value="alumni">Alumni</option>
          <option value="admin">Admin</option>
        </select>
        <button className="refresh-btn" onClick={() => void refreshData()}>
          Refresh
        </button>
      </section>

      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}

      {role !== "admin" && (
        <section className="panel">
          <h2>{editingId !== null ? "Edit Your Post" : "Create a Career Post"}</h2>
          <form onSubmit={handleSubmit}>
            {editingId === null && (
              <label>
                Post Type
                <select
                  value={postType}
                  onChange={(e) => setPostType(e.target.value as PostType)}
                >
                  {role === "student" ? (
                    <option value="job_seeking">Job Seeking</option>
                  ) : (
                    <>
                      <option value="job">Job Opportunity</option>
                      <option value="internship">Internship</option>
                    </>
                  )}
                </select>
              </label>
            )}

            <label>
              Title
              <input
                required
                minLength={3}
                maxLength={150}
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter post title"
              />
            </label>

            <label>
              Description
              <textarea
                required
                minLength={10}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Write post details..."
                rows={4}
              />
            </label>

            <label>
              Company (Optional)
              <input
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Company name"
              />
            </label>

            <div className="form-actions">
              <button type="submit">
                {editingId !== null ? "Save Changes" : "Submit Post"}
              </button>
              {editingId !== null && (
                <button type="button" className="cancel-btn" onClick={resetForm}>
                  Cancel
                </button>
              )}
            </div>
          </form>
        </section>
      )}

      {role === "admin" ? (
        <section className="panel">
          <h2>Admin Review Panel</h2>
          <p>Review submitted posts before publishing.</p>
          {adminPosts.length === 0 && <p>No pending posts right now.</p>}

          {adminPosts.map((post) => (
            <article className="post-card" key={post.id}>
              <span className="status pending">Pending</span>
              <h3>{post.title}</h3>
              <p>{post.description}</p>
              <small>
                {post.owner_name} · {postTypeLabel(post.post_type)}
              </small>
              <div className="form-actions">
                <button onClick={() => void reviewPost(post.id, "approved")}>
                  Approve
                </button>
                <button
                  className="delete-btn"
                  onClick={() => void reviewPost(post.id, "rejected")}
                >
                  Reject
                </button>
              </div>
            </article>
          ))}
        </section>
      ) : (
        <section className="panel">
          <h2>My Posts</h2>
          {myPosts.length === 0 && <p>You have not created any posts yet.</p>}

          {myPosts.map((post) => (
            <article className="post-card" key={post.id}>
              <span className={`status ${post.status}`}>{post.status}</span>
              <h3>{post.title}</h3>
              <p>{post.description}</p>
              <small>
                {postTypeLabel(post.post_type)} · {post.created_at}
              </small>
              <div className="form-actions">
                <button className="edit-btn" onClick={() => startEdit(post)}>
                  Edit
                </button>
                <button className="delete-btn" onClick={() => void deletePost(post.id)}>
                  Delete
                </button>
              </div>
            </article>
          ))}
        </section>
      )}

      <section className="panel">
        <h2>Approved Career Posts</h2>
        {posts.length === 0 && <p>No approved posts available.</p>}

        {posts.map((post) => (
          <article className="post-card" key={post.id}>
            <span className="status approved">Approved</span>
            <h3>{post.title}</h3>
            <p>{post.description}</p>
            <small>
              {postTypeLabel(post.post_type)} · By {post.owner_name}
            </small>
            <button className="details-btn" onClick={() => void showDetails(post.id)}>
              View Details
            </button>
          </article>
        ))}
      </section>

      {detail && (
        <section className="panel detail-panel">
          <h2>Post Details</h2>
          <h3>{detail.title}</h3>
          <p>{detail.description}</p>
          <p>Company: {detail.company || "Not specified"}</p>
          <p>Posted by: {detail.owner_name}</p>
          <button className="cancel-btn" onClick={() => setDetail(null)}>
            Close Details
          </button>
        </section>
      )}

      <footer>
        IUBLink CareerHub · Mid Project Assessment MVP
      </footer>
    </main>
  )
}
