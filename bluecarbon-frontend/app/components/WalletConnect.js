'use client'
import { useState } from 'react'
import { ethers } from 'ethers'

export default function WalletConnect(){
  const [addr, setAddr] = useState(null)

  async function connect(){
    if(!window.ethereum) return alert('Install MetaMask')
    const provider = new ethers.BrowserProvider(window.ethereum)
    const accounts = await provider.send('eth_requestAccounts', [])
    setAddr(accounts[0])
  }

  return (
    <div>
      {addr ? <div className="small">Wallet: {addr}</div> : <button onClick={connect} className="btn">Connect Wallet</button>}
    </div>
  )
}
