#!/bin/bash

echo "========================================"
echo "Blue Carbon Registry Setup Script (Mac)"
echo "========================================"
echo

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew is already installed"
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    brew install node
else
    echo "✓ Node.js is already installed ($(node --version))"
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    brew install python
else
    echo "✓ Python3 is already installed ($(python3 --version))"
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Installing Git..."
    brew install git
else
    echo "✓ Git is already installed ($(git --version))"
fi

echo
echo "Step 1: Installing backend dependencies..."
cd blue-carbon-backend
if pip3 install -r requirements.txt; then
    echo "✓ Backend dependencies installed successfully"
else
    echo "✗ Failed to install Python dependencies"
    exit 1
fi

echo
echo "Step 2: Installing frontend dependencies..."
cd ../bluecarbon-frontend
if npm install; then
    echo "✓ Frontend dependencies installed successfully"
else
    echo "✗ Failed to install frontend dependencies"
    exit 1
fi

echo
echo "Step 3: Installing blockchain dependencies..."
cd ../blue-carbon-contracts
if npm install; then
    echo "✓ Blockchain dependencies installed successfully"
else
    echo "✗ Failed to install blockchain dependencies"
    exit 1
fi

echo
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "NEXT STEPS:"
echo "1. Copy blue-carbon-backend/.env.example to .env"
echo "2. Update .env with your MetaMask private key"
echo "3. Start Hardhat local blockchain:"
echo "   cd blue-carbon-contracts && npx hardhat node"
echo "4. Deploy contracts (in new terminal):"
echo "   npx hardhat run scripts/deploy.js --network localhost"
echo "5. Update contract addresses in config files"
echo "6. Initialize database:"
echo "   cd blue-carbon-backend && python3 init_db.py"
echo "7. Start backend:"
echo "   python3 main.py"
echo "8. Start frontend (in new terminal):"
echo "   cd bluecarbon-frontend && npm run dev"
echo
echo "See README.md for detailed instructions."
echo