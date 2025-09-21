const API_BASE = "http://127.0.0.1:8000"

// Get auth token from localStorage
function getAuthHeaders() {
  const token = localStorage.getItem('access_token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

// --- Projects ---
export async function getProjects() {
  const res = await fetch(`${API_BASE}/projects?ts=${Date.now()}`, {
    cache: "no-store",
  })
  if (!res.ok) throw new Error("Failed to fetch projects")
  return res.json()
}

// Get user's own projects with full details
export async function getMyProjects() {
  const res = await fetch(`${API_BASE}/projects/my?ts=${Date.now()}`, {
    cache: "no-store",
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error("Failed to fetch my projects")
  return res.json()
}

// Get all projects with limited info for other users' projects
export async function getAllProjectsLimited() {
  const res = await fetch(`${API_BASE}/projects/all?ts=${Date.now()}`, {
    cache: "no-store",
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error("Failed to fetch all projects")
  return res.json()
}

export async function getProjectById(id) {
  // ✅ now directly fetch from backend instead of filtering dummy
  const res = await fetch(`${API_BASE}/projects/${id}?ts=${Date.now()}`, {
    cache: "no-store",
  })
  if (!res.ok) throw new Error("Failed to fetch project")
  return res.json()
}

export async function getEvidences(projectId) {
  const res = await fetch(`${API_BASE}/evidences/${projectId}?ts=${Date.now()}`, {
    cache: "no-store",
  })
  if (!res.ok) throw new Error("Failed to fetch evidences")
  return res.json()
}

// --- Register a new project ---
export async function registerProject(project) {
  const payload = {
    ...project,
    hectares: parseInt(project.hectares, 10), // ✅ ensure integer
  }

  const res = await fetch(`${API_BASE}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error?.detail || "Failed to register project")
  }
  return res.json()
}

// --- Delete Project ---
export async function deleteProject(projectId) {
  const res = await fetch(`${API_BASE}/projects/${projectId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders()
    }
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error?.detail || "Failed to delete project")
  }
  return res.json()
}

// --- Verify Evidence ---
export async function verifyProject(
  evidenceId,
  { mint_receipt = false, receipt_token_uri = "", mint_amount = 0 } = {}
) {
  const payload = {
    evidence_id: Number(evidenceId),
    mint_receipt: Boolean(mint_receipt),
    receipt_token_uri: String(receipt_token_uri),
    mint_amount: Number(mint_amount),
  }

  const res = await fetch(`${API_BASE}/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error?.detail || "Failed to verify evidence")
  }
  return res.json()
}

// --- Mint Credits (via verify with amount > 0) ---
export async function mintCredits(evidenceId, amount, receiptUri = "") {
  const payload = {
    evidence_id: Number(evidenceId),
    mint_receipt: true,
    receipt_token_uri: String(receiptUri),
    mint_amount: Number(amount),
  }

  const res = await fetch(`${API_BASE}/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error?.detail || "Failed to mint credits")
  }
  return res.json()
}

// --- Token Balance ---
export async function getCredits(address) {
  const res = await fetch(`${API_BASE}/credits/${address}?ts=${Date.now()}`, {
    cache: "no-store",
  })
  if (!res.ok) throw new Error("Failed to fetch credits")
  return res.json()
}

// --- Auth Functions ---
export async function updateWalletAddress(walletAddress) {
  const res = await fetch(`${API_BASE}/auth/wallet`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders()
    },
    body: JSON.stringify({ wallet_address: walletAddress }),
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error?.detail || "Failed to update wallet address")
  }
  return res.json()
}
