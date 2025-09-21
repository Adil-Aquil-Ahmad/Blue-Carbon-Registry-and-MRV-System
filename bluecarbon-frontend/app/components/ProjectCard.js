'use client'
import Link from 'next/link'

export default function ProjectCard({ project }) {
  const owner = project.owner || "Unknown"
  const name = project.name || "Unnamed Project"
  const location = project.location || "N/A"
  const hectares = project.hectares ?? 0

  // if project.owner is an address, shorten safely
  const shortOwner = typeof owner === "string" && owner.length > 10
    ? owner.slice(0, 6) + "..." + owner.slice(-4)
    : owner

  return (
    <Link href={`/projects/${project.id}`} className="card">
      <h3>{name}</h3>
      <div className="kv">{location} • {hectares} ha</div>
      <div className="small">Owner: {shortOwner}</div>
      {project.evidences?.length > 0 && (
        <div className="small">📂 {project.evidences.length} evidences</div>
      )}
      <div className="small">
        Status: {project.verified ? "✅ Verified" : "⏳ Pending"}
      </div>
    </Link>
  )
}
