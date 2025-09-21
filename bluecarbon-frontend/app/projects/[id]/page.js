'use client'
import { use, useEffect, useState } from 'react'
import { getProjectById, getEvidences, getCredits } from '@/lib/api'

export default function ProjectDetail({ params }) {
  // ✅ unwrap params (Next.js 13+ App Router gives params as Promise)
  const { id } = use(params)

  const [project, setProject] = useState(null)
  const [evidences, setEvidences] = useState([])
  const [credits, setCredits] = useState(null)
  const [loading, setLoading] = useState(true)

  async function load() {
    try {
      const proj = await getProjectById(id)
      const ev = await getEvidences(id)
      const creditInfo = await getCredits(proj.owner)

      setProject(proj)
      setEvidences(ev)
      setCredits(creditInfo)
    } catch (err) {
      console.error("Failed to load project:", err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()

    // 🔄 refresh every 10s so uploads/credits show up
    const interval = setInterval(() => load(), 10000)
    return () => clearInterval(interval)
  }, [id])

  if (loading || !project) {
    return <div className="card">Loading project...</div>
  }

  return (
    <div className="card">
      <h2>{project.name}</h2>
      <p>{project.location} • {project.hectares} ha</p>
      <p>Status: {project.totalIssuedCredits > 0 ? "✅ Verified" : "⏳ Pending"}</p>
      <p>Owner: {project.owner}</p>
      {credits && <p>Credits: {credits.balance}</p>}

      <h3 style={{ marginTop: "1em" }}>Evidences</h3>
      {evidences.length > 0 ? (
        <ul>
          {evidences.map(ev => (
            <li key={ev.evidenceId}>
              Evidence #{ev.evidenceId} – Hash: {ev.evidenceHash?.slice(0, 10)}... <br />
              Uploader: {ev.uploader} <br />
              URI: {ev.evidenceURI || "N/A"}
            </li>
          ))}
        </ul>
      ) : (
        <p>No evidences uploaded yet.</p>
      )}
    </div>
  )
}
