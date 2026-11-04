
type Role = "student" | "alumni" | "faculty" | "admin"

interface Post {
  id: number
  title: string
  description: string
  post_type: "job_seeking" | "job" | "internship"
  status: string
}

interface DashboardStatsProps {
  role: Role
  posts: Post[]
  myPosts: Post[]
  adminPosts: Post[]
}

function DashboardStats({
  role,
  posts,
  myPosts,
  adminPosts,
}: DashboardStatsProps) {
  const stats = [
    ...(role === "admin"
      ? [
          {
            label: "Approved Posts",
            value: posts.length,
            icon: "✓",
            color: "purple",
          },
          {
            label: "Pending Reviews",
            value: adminPosts.length,
            icon: "◷",
            color: "orange",
          },
          {
            label: "Total Visible Posts",
            value: posts.length + adminPosts.length,
            icon: "▤",
            color: "teal",
          },
        ]
      : role === "faculty"
        ? [
            {
              label: "Total Opportunities",
              value: posts.length,
              icon: "▣",
              color: "purple",
            },
            {
              label: "Job Posts",
              value: posts.filter((p) => p.post_type === "job").length,
              icon: "💼",
              color: "teal",
            },
            {
              label: "Internship Posts",
              value: posts.filter((p) => p.post_type === "internship").length,
              icon: "🎓",
              color: "orange",
            },
            {
              label: "Job Seeking Posts",
              value: posts.filter((p) => p.post_type === "job_seeking").length,
              icon: "👥",
              color: "pink",
            },
          ]
        : [
            {
              label: "Career Opportunities",
              value: posts.length,
              icon: "▣",
              color: "purple",
            },
            {
              label: "My Posts",
              value: myPosts.length,
              icon: "▤",
              color: "teal",
            },
            {
              label: "Pending Posts",
              value: myPosts.filter((p) => p.status === "pending").length,
              icon: "◷",
              color: "orange",
            },
            {
              label: "Rejected Posts",
              value: myPosts.filter((p) => p.status === "rejected").length,
              icon: "✕",
              color: "pink",
            },
          ]),
  ]

  return (
    <section className="stats-grid">
      {stats.map((stat) => (
        <article className={`stat-card ${stat.color}`} key={stat.label}>
          <div className="stat-card-top">
            <span className="stat-icon">{stat.icon}</span>
            <span className="stat-label">{stat.label}</span>
          </div>

          <h2>{stat.value}</h2>
          <p>Updated from career posts</p>
        </article>
      ))}
    </section>
  )
}

export default DashboardStats
