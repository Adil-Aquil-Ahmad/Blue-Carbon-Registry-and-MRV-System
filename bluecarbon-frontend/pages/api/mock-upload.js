// Simple mock endpoint to accept FormData and return a fake id.
// Create 'pages' folder in root of the frontend project and add this file.

export const config = {
  api: {
    bodyParser: false
  }
}

import formidable from 'formidable'
import fs from 'fs'

export default async function handler(req, res){
  if(req.method !== 'POST') return res.status(405).json({error:'method'})
  const form = formidable({ multiples: true, keepExtensions:true })
  form.parse(req, (err, fields, files) => {
    if(err) return res.status(500).json({ error: err.message })
    // Here you would upload files to IPFS and store metadata in backend.
    // For demo we return fake CID and record id.
    res.json({ id: 'mock-evidence-' + Date.now(), cid: 'QmDemoCID'+Date.now(), fields })
  })
}
