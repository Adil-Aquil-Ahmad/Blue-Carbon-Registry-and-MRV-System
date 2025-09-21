// scripts/deploy.mjs
import hardhat from "hardhat";
const { ethers } = hardhat;

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  // Deploy CarbonToken
  const CarbonToken = await ethers.getContractFactory("CarbonToken");
  const carbonToken = await CarbonToken.deploy("CarbonToken", "CT");
  await carbonToken.waitForDeployment();
  console.log("CarbonToken deployed at:", await carbonToken.getAddress());

  // Deploy Registry
  const Registry = await ethers.getContractFactory("BlueCarbonRegistry");
  const registry = await Registry.deploy(deployer.address);
  await registry.waitForDeployment();
  console.log("Registry deployed at:", await registry.getAddress());

  // Link registry <-> token
  await registry.setCarbonToken(await carbonToken.getAddress());
  const ISSUER_ROLE = await carbonToken.ISSUER_ROLE();
  await carbonToken.grantRole(ISSUER_ROLE, await registry.getAddress());

  console.log("✅ Deployment complete");
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
