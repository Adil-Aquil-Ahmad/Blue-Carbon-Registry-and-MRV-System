# Blue Carbon Registry and MRV System

A blockchain-based Blue Carbon Registry and Monitoring, Reporting, and Verification (MRV) System for carbon credit management and verification.

## Project Setup for New Environment

### Prerequisites

1. **Node.js** (v16 or higher)
2. **Python** (v3.8 or higher)
3. **MetaMask** browser extension
4. **Git**

### Configuration Changes Required for Different Computer/MetaMask Account

When transferring this project to a different computer or using a different MetaMask account, you need to update the following configurations:

#### 1. Backend Configuration (`blue-carbon-backend/config.py`)

```python
# Blockchain config
RPC_URL = "http://127.0.0.1:8545"  # Keep same for local development
PRIVATE_KEY = "YOUR_METAMASK_PRIVATE_KEY_HERE"  #  CHANGE THIS

# Contract address - will be different after redeployment
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  #  UPDATE AFTER DEPLOY

# Database config (can keep same)
DB_URL = f"sqlite:///{os.path.abspath('bluecarbon.db')}"

# IPFS config (keep same for local)
IPFS_HOST = "/ip4/127.0.0.1/tcp/5001/http"
```

#### 2. Frontend Configuration (`bluecarbon-frontend/app/upload/page.js`)

```javascript
// Line 13 - Update contract address after deployment
const REGISTRY_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"  //  CHANGE THIS
```

#### 3. Hardhat Configuration (`blue-carbon-contracts/hardhat.config.js`)

```javascript
// The mnemonic can stay the same for local development
// This is the standard Hardhat test mnemonic
accounts: {
  mnemonic: "test test test test test test test test test test test junk",
  // ... rest of config
}
```

### Setup Instructions

#### For Windows Users

##### Step 1: Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Adil-Aquil-Ahmad/Blue-Carbon-Registry-and-MRV-System.git
cd Blue-Carbon-Registry-and-MRV-System

# Install backend dependencies
cd blue-carbon-backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../bluecarbon-frontend
npm install

# Install blockchain dependencies
cd ../blue-carbon-contracts
npm install
```

##### Step 2: Get Your MetaMask Private Key

 **SECURITY WARNING**: Never share your private key or commit it to version control!

1. Open MetaMask
2. Click on account menu → Account details
3. Export Private Key
4. Copy the private key (starts with 0x...)

##### Step 3: Update Configuration Files

1. **Update Backend Config**:
   ```bash
   # Edit blue-carbon-backend/config.py
   # Replace PRIVATE_KEY with your MetaMask private key
   PRIVATE_KEY = "0xYOUR_PRIVATE_KEY_HERE"
   ```

2. **Set Environment Variable** (Recommended):
   ```bash
   # Create .env file in blue-carbon-backend/
   echo "PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE" > blue-carbon-backend/.env
   ```

##### Step 4: Start Local Blockchain

```bash
cd blue-carbon-contracts
npx hardhat node
```

Keep this terminal open. Note the first account address and private key displayed.

##### Step 5: Deploy Smart Contracts

In a new terminal:
```bash
cd blue-carbon-contracts
npx hardhat run scripts/deploy.js --network localhost
```

**IMPORTANT**: Copy the deployed contract address from the output!

##### Step 6: Update Contract Addresses

1. **Backend**: Update `CONTRACT_ADDRESS` in `blue-carbon-backend/config.py`
2. **Frontend**: Update `REGISTRY_ADDRESS` in `bluecarbon-frontend/app/upload/page.js`

##### Step 7: Setup MetaMask for Local Network

1. Open MetaMask
2. Add network:
   - Network Name: `Hardhat Local`
   - RPC URL: `http://127.0.0.1:8545`
   - Chain ID: `31337`
   - Currency Symbol: `ETH`

3. Import test account:
   - Use the private key from Step 4 (first account from hardhat node)

##### Step 8: Initialize Database

```bash
cd blue-carbon-backend
python init_db.py
```

##### Step 9: Start Applications

1. **Backend** (Terminal 1):
   ```bash
   cd blue-carbon-backend
   python main.py
   ```

2. **Frontend** (Terminal 2):
   ```bash
   cd bluecarbon-frontend
   npm run dev
   ```

#### For Mac Users

##### Quick Setup (Automated)

For a quick automated setup, you can use the provided script:

```bash
# Make the script executable and run it
chmod +x setup-mac.sh
./setup-mac.sh
```

##### Manual Setup

##### Prerequisites for Mac

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Node.js**:
   ```bash
   brew install node
   # Verify installation
   node --version
   npm --version
   ```

3. **Install Python** (if not already installed):
   ```bash
   brew install python
   # Verify installation
   python3 --version
   pip3 --version
   ```

4. **Install Git** (if not already installed):
   ```bash
   brew install git
   ```

5. **Install MetaMask** browser extension from the Chrome Web Store or Firefox Add-ons

##### Step 1: Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/Adil-Aquil-Ahmad/Blue-Carbon-Registry-and-MRV-System.git
cd Blue-Carbon-Registry-and-MRV-System

# Install backend dependencies
cd blue-carbon-backend
pip3 install -r requirements.txt

# Install frontend dependencies
cd ../bluecarbon-frontend
npm install

# Install blockchain dependencies
cd ../blue-carbon-contracts
npm install
```

##### Step 2: Get Your MetaMask Private Key

 **SECURITY WARNING**: Never share your private key or commit it to version control!

1. Open MetaMask
2. Click on account menu → Account details
3. Export Private Key
4. Copy the private key (starts with 0x...)

##### Step 3: Update Configuration Files

1. **Update Backend Config**:
   ```bash
   # Edit blue-carbon-backend/config.py using your preferred editor
   nano blue-carbon-backend/config.py
   # or
   vim blue-carbon-backend/config.py
   # or
   code blue-carbon-backend/config.py  # if using VS Code
   
   # Replace PRIVATE_KEY with your MetaMask private key
   PRIVATE_KEY = "0xYOUR_PRIVATE_KEY_HERE"
   ```

2. **Set Environment Variable** (Recommended):
   ```bash
   # Create .env file in blue-carbon-backend/
   echo "PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE" > blue-carbon-backend/.env
   ```

##### Step 4: Start Local Blockchain

```bash
cd blue-carbon-contracts
npx hardhat node
```

Keep this terminal open. Note the first account address and private key displayed.

##### Step 5: Deploy Smart Contracts

Open a new terminal (Cmd+T):
```bash
cd Blue-Carbon-Registry-and-MRV-System/blue-carbon-contracts
npx hardhat run scripts/deploy.js --network localhost
```

**IMPORTANT**: Copy the deployed contract address from the output!

##### Step 6: Update Contract Addresses

1. **Backend**: Update `CONTRACT_ADDRESS` in `blue-carbon-backend/config.py`
2. **Frontend**: Update `REGISTRY_ADDRESS` in `bluecarbon-frontend/app/upload/page.js`

```bash
# Edit the files using your preferred editor
nano blue-carbon-backend/config.py
nano bluecarbon-frontend/app/upload/page.js
```

##### Step 7: Setup MetaMask for Local Network

1. Open MetaMask
2. Add network:
   - Network Name: `Hardhat Local`
   - RPC URL: `http://127.0.0.1:8545`
   - Chain ID: `31337`
   - Currency Symbol: `ETH`

3. Import test account:
   - Use the private key from Step 4 (first account from hardhat node)

##### Step 8: Initialize Database

```bash
cd blue-carbon-backend
python3 init_db.py
```

##### Step 9: Start Applications

1. **Backend** (Terminal 1):
   ```bash
   cd blue-carbon-backend
   python3 main.py
   ```

2. **Frontend** (Terminal 2 - open new tab with Cmd+T):
   ```bash
   cd Blue-Carbon-Registry-and-MRV-System/bluecarbon-frontend
   npm run dev
   ```

##### Mac-Specific Notes

- Use `python3` and `pip3` instead of `python` and `pip`
- Use `Cmd+T` to open new terminal tabs
- Default terminal editors: `nano` (beginner-friendly) or `vim` (advanced)
- If you have VS Code installed, you can use `code filename` to edit files
- Permission issues: prefix commands with `sudo` if needed
- Use `brew install` for package management

##### Mac Troubleshooting

**Issue**: Permission denied errors
```bash
# Solution: Use sudo or fix npm permissions
sudo chown -R $(whoami) ~/.npm
# or install npm packages globally with correct permissions
```

**Issue**: Python version conflicts
```bash
# Solution: Use python3 explicitly
python3 --version
pip3 install -r requirements.txt
```

**Issue**: Node.js not found
```bash
# Solution: Install via Homebrew
brew install node
# or download from nodejs.org
```

```bash
cd blue-carbon-contracts
npx hardhat node
```

Keep this terminal open. Note the first account address and private key displayed.

#### Step 5: Deploy Smart Contracts

In a new terminal:
```bash
cd blue-carbon-contracts
npx hardhat run scripts/deploy.js --network localhost
```

**IMPORTANT**: Copy the deployed contract address from the output!

#### Step 6: Update Contract Addresses

1. **Backend**: Update `CONTRACT_ADDRESS` in `blue-carbon-backend/config.py`
2. **Frontend**: Update `REGISTRY_ADDRESS` in `bluecarbon-frontend/app/upload/page.js`

#### Step 7: Setup MetaMask for Local Network

1. Open MetaMask
2. Add network:
   - Network Name: `Hardhat Local`
   - RPC URL: `http://127.0.0.1:8545`
   - Chain ID: `31337`
   - Currency Symbol: `ETH`

3. Import test account:
   - Use the private key from Step 4 (first account from hardhat node)

#### Step 8: Initialize Database

```bash
cd blue-carbon-backend
python init_db.py
```

#### Step 9: Start Applications

1. **Backend** (Terminal 1):
   ```bash
   cd blue-carbon-backend
   python main.py
   ```

2. **Frontend** (Terminal 2):
   ```bash
   cd bluecarbon-frontend
   npm run dev
   ```

### Key Configuration Files to Update

| File | What to Change | Why |
|------|----------------|-----|
| `blue-carbon-backend/config.py` | `PRIVATE_KEY`, `CONTRACT_ADDRESS` | Different wallet, new deployment |
| `bluecarbon-frontend/app/upload/page.js` | `REGISTRY_ADDRESS` | Must match deployed contract |
| MetaMask Network Settings | Add local network (127.0.0.1:8545) | Connect to local blockchain |

### Security Best Practices

1. **Never commit private keys to Git**
2. **Use environment variables** for sensitive data
3. **Use different accounts** for development and production
4. **Keep test accounts separate** from real funds

### Common Issues and Solutions

#### Issue: "Contract not found" errors
**Solution**: Ensure contract address in both backend and frontend match the deployed address

#### Issue: "Insufficient funds" errors
**Solution**: Make sure your MetaMask account has ETH from the Hardhat local network

#### Issue: "Network mismatch" errors
**Solution**: Verify MetaMask is connected to the local Hardhat network (Chain ID: 31337)

#### Issue: Database connection errors
**Solution**: Run `python init_db.py` to initialize the database

### Project Structure

```
Blue-Carbon-Registry-and-MRV-System/
├── blue-carbon-backend/          # FastAPI Python backend
│   ├── config.py                 #  Main configuration file
│   ├── main.py                   # API endpoints
│   ├── database.py               # Database connection
│   └── requirements.txt          # Python dependencies
├── bluecarbon-frontend/          # Next.js React frontend
│   ├── app/upload/page.js        #  Contains contract address
│   └── package.json              # Node.js dependencies
├── blue-carbon-contracts/        # Smart contracts
│   ├── hardhat.config.js         # Blockchain configuration
│   ├── contracts/                # Solidity contracts
│   └── scripts/deploy.js         # Deployment script
└── README.md                     # This file
```

### Features

- **AI-powered vegetation analysis** for carbon credit calculation
- **Blockchain verification** of carbon credits
- **Image upload and processing** for evidence validation
- **Project management** with user authentication
- **Credit multiplier system** based on vegetation improvement

### Contributing

1. Fork the repository
2. Create a feature branch
3. Update configurations as needed
4. Test thoroughly
5. Submit a pull request

### Support

If you encounter issues during setup, please check:
1. All configuration files are updated correctly
2. Local blockchain is running
3. MetaMask is connected to the correct network
4. Smart contracts are deployed successfully

---

**Remember**: Always update the contract addresses and private keys when moving to a new environment!