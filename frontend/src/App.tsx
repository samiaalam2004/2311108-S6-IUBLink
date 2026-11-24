import { useCallback, useEffect, useState, type FormEvent } from "react"
import { Routes, Route, Link, useNavigate } from "react-router-dom"

import Home from "./pages/Home"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Navbar from "./components/Navbar"
import Sidebar from "./components/Sidebar"
import DashboardStats from "./components/DashboardStats"
import {
  apiData,
  apiFetch,
  getStoredToken,
  refreshAccessToken,
  setStoredToken,
} from "./api/client"
import "./App.css"

type PostType = "job_seeking" | "job" | "internship"

interface User {
  id: number
  full_name: string
  email: string
  role: string
  department?: string | null
  batch_or_graduation?: string | null
  headline?: string | null
  bio?: string | null
  linkedin_url?: string | null
  is_banned?: boolean
  ban_reason?: string | null
}

interface AdminUserRow {
  id: number
  full_name: string
  email: string
  role: string
  department?: string | null
  batch_or_graduation?: string | null
  is_banned: boolean
  ban_reason?: string | null
}

interface Post {
  id: number
  title: string
  description: string
  post_type: PostType
  company: string | null
  owner_id: number | string
  owner_name: string
  status: string
  review_note: string | null
  created_at: string
}

function CareerDashboard() {
  const navigate = useNavigate()

  const [user, setUser] = useState<User | null>(null)
  const [authChecked, setAuthChecked] = useState(false)

  const [posts, setPosts] = useState<Post[]>([])
  const [myPosts, setMyPosts] = useState<Post[]>([])
  const [adminPosts, setAdminPosts] = useState<Post[]>([])
  const [adminUsers, setAdminUsers] = useState<AdminUserRow[]>([])
  const [banReasons, setBanReasons] = useState<Record<number, string>>({})
  const [detail, setDetail] = useState<Post | null>(null)

  // Post form state
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [company, setCompany] = useState("")
  const [postType, setPostType] = useState<PostType>("job_seeking")
  const [editingId, setEditingId] = useState<number | null>(null)

  // Profile form state
  const [profileFullName, setProfileFullName] = useState("")
  const [department, setDepartment] = useState("")
  const [batchOrGraduation, setBatchOrGraduation] = useState("")
  const [headline, setHeadline] = useState("")
  const [bio, setBio] = useState("")
  const [linkedinUrl, setLinkedinUrl] = useState("")
  const [savingProfile, setSavingProfile] = useState(false)

  // Password change state
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [changingPassword, setChangingPassword] = useState(false)

  const [message, setMessage] = useState("")
  const [error, setError] = useState("")

  function syncProfileForm(u: User) {
    setProfileFullName(u.full_name || "")
    setDepartment(u.department || "")
    setBatchOrGraduation(u.batch_or_graduation || "")
    setHeadline(u.headline || "")
    setBio(u.bio || "")
    setLinkedinUrl(u.linkedin_url || "")
  }

  // Restore session on load or refresh
  useEffect(() => {
    let active = true

    async function loadUser() {
      if (!getStoredToken()) {
        await refreshAccessToken()
      }

      if (!getStoredToken()) {
        if (active) {
          setAuthChecked(true)
          setError("Please log in first.")
        }
        return
      }

      try {
        const res = await apiFetch("/api/auth/me")
        const currentUser = await apiData<User>(res)
        if (!active) return

        setUser(currentUser)
        syncProfileForm(currentUser)
        localStorage.setItem("user", JSON.stringify(currentUser))
        setError("")
      } catch (err) {
        if (!active) return
        setStoredToken(null)
        localStorage.removeItem("user")
        setError(
          err instanceof Error ? err.message : "Session expired. Please log in."
        )
      } finally {
        if (active) {
          setAuthChecked(true)
        }
      }
    }

    void loadUser()
    return () => {
      active = false
    }
  }, [])

  const refreshData = useCallback(async () => {
    if (!user) return

    try {
      setError("")

      const publicRes = await apiFetch("/api/posts")
      setPosts(await apiData<Post[]>(publicRes))

      if (user.role === "admin") {
        const [pendingRes, usersRes] = await Promise.all([
          apiFetch("/api/admin/posts?status=pending"),
          apiFetch("/api/admin/users"),
        ])
        setAdminPosts(await apiData<Post[]>(pendingRes))
        setAdminUsers(await apiData<AdminUserRow[]>(usersRes))
        setMyPosts([])
      } else {
        const myRes = await apiFetch("/api/my-posts")
        setMyPosts(await apiData<Post[]>(myRes))
        setAdminPosts([])
        setAdminUsers([])
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not load dashboard data"
      )
    }
  }, [user])

  useEffect(() => {
    if (user) {
      void refreshData()
    }
  }, [user, refreshData])

  function resetPostForm() {
    setTitle("")
    setDescription("")
    setCompany("")
    setEditingId(null)
    setPostType("job_seeking")
  }

  async function handlePostSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setMessage("")
    setError("")

    if (!user) {
      setError("Please log in first.")
      return
    }

    const commonData = {
      title,
      description,
      company: company.trim() || null,
    }

    try {
      const response =
        editingId !== null
          ? await apiFetch(`/api/posts/${editingId}`, {
              method: "PATCH",
              body: JSON.stringify(commonData),
            })
          : await apiFetch("/api/posts", {
              method: "POST",
              body: JSON.stringify({
                ...commonData,
                post_type: postType,
              }),
            })

      await apiData<Post>(response)
      setMessage(
        editingId !== null ? "Post updated!" : "Post submitted for approval!"
      )
      resetPostForm()
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
    if (!window.confirm("Are you sure you want to delete this post?")) {
      return
    }

    try {
      const response = await apiFetch(`/api/posts/${id}`, {
        method: "DELETE",
      })
      await apiData<{ message: string }>(response)
      setMessage("Post deleted successfully!")
      await refreshData()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed")
    }
  }

  async function reviewPost(id: number, status: "approved" | "rejected") {
    try {
      const response = await apiFetch(`/api/admin/posts/${id}/review`, {
        method: "PATCH",
        body: JSON.stringify({
          status,
          review_note:
            status === "approved"
              ? "Approved by admin."
              : "Rejected by admin.",
        }),
      })
      await apiData<Post>(response)
      setMessage(`Post ${status}!`)
      await refreshData()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Review failed")
    }
  }

  async function handleToggleBan(targetUser: AdminUserRow, nextBanned: boolean) {
    setMessage("")
    setError("")

    try {
      const reasonText = (banReasons[targetUser.id] || "").trim()
      const response = await apiFetch(`/api/admin/users/${targetUser.id}/ban`, {
        method: "PATCH",
        body: JSON.stringify({
          is_banned: nextBanned,
          ban_reason: nextBanned ? reasonText || "Banned by admin" : null,
        }),
      })

      await apiData<AdminUserRow>(response)
      setMessage(
        nextBanned
          ? `${targetUser.full_name} has been banned.`
          : `${targetUser.full_name} has been unbanned.`
      )
      await refreshData()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to update ban status"
      )
    }
  }

  async function handleProfileSave(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setMessage("")
    setError("")
    setSavingProfile(true)

    try {
      const response = await apiFetch("/api/users/me", {
        method: "PATCH",
        body: JSON.stringify({
          full_name: profileFullName.trim(),
          department: department.trim() || null,
          batch_or_graduation: batchOrGraduation.trim() || null,
          headline: headline.trim() || null,
          bio: bio.trim() || null,
          linkedin_url: linkedinUrl.trim() || null,
        }),
      })

      const updatedUser = await apiData<User>(response)
      setUser(updatedUser)
      syncProfileForm(updatedUser)
      localStorage.setItem("user", JSON.stringify(updatedUser))
      setMessage("Profile updated successfully!")
      await refreshData()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to update profile"
      )
    } finally {
      setSavingProfile(false)
    }
  }

  async function handlePasswordChange(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setMessage("")
    setError("")
    setChangingPassword(true)

    try {
      const response = await apiFetch("/api/users/me/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      })

      const resData = await apiData<{ message: string }>(response)
      setCurrentPassword("")
      setNewPassword("")
      setStoredToken(null)
      localStorage.removeItem("user")
      alert(resData.message)
      navigate("/login")
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to change password"
      )
    } finally {
      setChangingPassword(false)
    }
  }

  async function showDetails(id: number) {
    try {
      const response = await apiFetch(`/api/posts/${id}`)
      setDetail(await apiData<Post>(response))
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Could not load details"
      )
    }
  }

  function postTypeLabel(type: PostType) {
    if (type === "job_seeking") return "Job Seeking"
    if (type === "internship") return "Internship"
    return "Job Opportunity"
  }

  if (!authChecked) {
    return <div className="auth-page">Loading your dashboard...</div>
  }

  if (!user) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <h1>Session Required</h1>
          <p>{error || "Please log in to view the dashboard."}</p>
          <Link to="/login">Go to Login</Link>
        </div>
      </div>
    )
  }

  const currentRole = (user.role || "user") as "user" | "student" | "alumni" | "faculty" | "admin"

  return (
    <div className="dashboard-layout">
      <Sidebar role={currentRole} />

      <div className="dashboard-main">
        <Navbar user={user} />

        <main className="dashboard-content">
          <div className="dashboard-toolbar">
            <div>
              <h1>Welcome to IUBLink!</h1>
              <p>Welcome back, {user.full_name}!</p>
              <p>Connect. Explore. Grow.</p>
            </div>

            <button
              type="button"
              className="refresh-btn"
              onClick={() => void refreshData()}
            >
              &#8635; Refresh
            </button>
          </div>

          <DashboardStats
            role={currentRole}
            posts={posts}
            myPosts={myPosts}
            adminPosts={adminPosts}
          />

          {message && <p className="success">{message}</p>}
          {error && <p className="error">{error}</p>}

          {currentRole !== "admin" && (
            <section className="panel">
              <h2>
                {editingId !== null
                  ? "Edit Your Post"
                  : "Create a Career Post"}
              </h2>

              <form onSubmit={handlePostSubmit}>
                {editingId === null && (
                  <label>
                    Post Type
                    <select
                      value={postType}
                      onChange={(e) =>
                        setPostType(e.target.value as PostType)
                      }
                    >
                      <option value="job_seeking">Job Seeking</option>
                      <option value="job">Job Opportunity</option>
                      <option value="internship">Internship</option>
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
                    <button
                      type="button"
                      className="cancel-btn"
                      onClick={resetPostForm}
                    >
                      Cancel
                    </button>
                  )}
                </div>
              </form>
            </section>
          )}

          {currentRole === "admin" ? (
            <>
              <section className="panel" id="review">
                <h2>Admin Review Panel</h2>
                <p>Review submitted posts before publishing.</p>

                {adminPosts.length === 0 && (
                  <p>No pending posts right now.</p>
                )}

                {adminPosts.map((post) => (
                  <article className="post-card" key={post.id}>
                    <span className="status pending">Pending</span>

                    <h3>{post.title}</h3>
                    <p>{post.description}</p>

                    <small>
                      {post.owner_name} &middot; {postTypeLabel(post.post_type)}
                    </small>

                    <div className="form-actions">
                      <button
                        type="button"
                        onClick={() => void reviewPost(post.id, "approved")}
                      >
                        Approve
                      </button>

                      <button
                        type="button"
                        className="delete-btn"
                        onClick={() => void reviewPost(post.id, "rejected")}
                      >
                        Reject
                      </button>
                    </div>
                  </article>
                ))}
              </section>

              <section className="panel" id="users">
                <h2>User Moderation (Ban / Unban)</h2>
                <p>Manage user access and ban status.</p>

                {adminUsers.length === 0 && <p>No users found.</p>}

                {adminUsers.map((u) => (
                  <article className="post-card" key={u.id}>
                    <span
                      className={`status ${u.is_banned ? "rejected" : "approved"}`}
                    >
                      {u.is_banned ? "Banned" : "Active"}
                    </span>

                    <h3>
                      {u.full_name} ({u.role})
                    </h3>
                    <p>{u.email}</p>
                    {u.is_banned && u.ban_reason && (
                      <p>Reason: {u.ban_reason}</p>
                    )}

                    {u.role !== "admin" && u.id !== user.id && (
                      <div className="form-actions">
                        {!u.is_banned ? (
                          <>
                            <input
                              type="text"
                              placeholder="Ban reason (optional)"
                              value={banReasons[u.id] || ""}
                              onChange={(e) =>
                                setBanReasons((prev) => ({
                                  ...prev,
                                  [u.id]: e.target.value,
                                }))
                              }
                            />
                            <button
                              type="button"
                              className="delete-btn"
                              onClick={() => void handleToggleBan(u, true)}
                            >
                              Ban User
                            </button>
                          </>
                        ) : (
                          <button
                            type="button"
                            onClick={() => void handleToggleBan(u, false)}
                          >
                            Unban User
                          </button>
                        )}
                      </div>
                    )}
                  </article>
                ))}
              </section>
            </>
          ) : (
            <section className="panel" id="my-posts">
              <h2>My Posts</h2>

              {myPosts.length === 0 && (
                <p>You have not created any posts yet.</p>
              )}

              {myPosts.map((post) => (
                <article className="post-card" key={post.id}>
                  <span className={`status ${post.status}`}>
                    {post.status}
                  </span>

                  <h3>{post.title}</h3>
                  <p>{post.description}</p>

                  <small>
                    {postTypeLabel(post.post_type)} &middot; {post.created_at}
                  </small>

                  <div className="form-actions">
                    <button
                      type="button"
                      className="edit-btn"
                      onClick={() => startEdit(post)}
                    >
                      Edit
                    </button>

                    <button
                      type="button"
                      className="delete-btn"
                      onClick={() => void deletePost(post.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </section>
          )}

          <section className="panel" id="profile">
            <h2>Profile &amp; Account Security</h2>

            <form onSubmit={handleProfileSave}>
              <label>
                Full Name
                <input
                  required
                  minLength={2}
                  maxLength={100}
                  value={profileFullName}
                  onChange={(e) => setProfileFullName(e.target.value)}
                />
              </label>

              <label>
                Department
                <input
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  placeholder="e.g., CSE"
                />
              </label>

              <label>
                Batch / Graduation
                <input
                  value={batchOrGraduation}
                  onChange={(e) => setBatchOrGraduation(e.target.value)}
                  placeholder="e.g., 2026"
                />
              </label>

              <label>
                Headline
                <input
                  value={headline}
                  onChange={(e) => setHeadline(e.target.value)}
                  placeholder="e.g., Aspiring Software Engineer"
                />
              </label>

              <label>
                LinkedIn URL
                <input
                  value={linkedinUrl}
                  onChange={(e) => setLinkedinUrl(e.target.value)}
                  placeholder="https://linkedin.com/in/..."
                />
              </label>

              <label>
                Bio
                <textarea
                  rows={3}
                  value={bio}
                  onChange={(e) => setBio(e.target.value)}
                  placeholder="Short bio..."
                />
              </label>

              <button type="submit" disabled={savingProfile}>
                {savingProfile ? "Saving..." : "Save Profile"}
              </button>
            </form>

            <hr />

            <h3>Change Password</h3>
            <form onSubmit={handlePasswordChange}>
              <label>
                Current Password
                <input
                  type="password"
                  required
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                />
              </label>

              <label>
                New Password
                <input
                  type="password"
                  required
                  minLength={8}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </label>

              <button type="submit" disabled={changingPassword}>
                {changingPassword ? "Updating..." : "Change Password"}
              </button>
            </form>
          </section>

          <section className="panel" id="opportunities">
            <h2>Approved Career Posts</h2>

            {posts.length === 0 && (
              <p>No approved posts available.</p>
            )}

            {posts.map((post) => (
              <article className="post-card" key={post.id}>
                <span className="status approved">Approved</span>

                <h3>{post.title}</h3>
                <p>{post.description}</p>

                <small>
                  {postTypeLabel(post.post_type)} &middot; By {post.owner_name}
                </small>

                <button
                  type="button"
                  className="details-btn"
                  onClick={() => void showDetails(post.id)}
                >
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

              <button
                type="button"
                className="cancel-btn"
                onClick={() => setDetail(null)}
              >
                Close Details
              </button>
            </section>
          )}

          <footer>
            IUBLink CareerHub &middot; CSE309 MVP
          </footer>
        </main>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<CareerDashboard />} />
    </Routes>
  )
}

