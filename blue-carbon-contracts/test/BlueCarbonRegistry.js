const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BlueCarbonRegistry", function () {
  let owner, verifier, projectOwner, other;
  let CarbonToken, BlueCarbonRegistry;
  let carbonToken, registry;

  beforeEach(async function () {
    [owner, verifier, projectOwner, other] = await ethers.getSigners();

    // Deploy ERC20 CarbonToken
    CarbonToken = await ethers.getContractFactory("CarbonToken");
    carbonToken = await CarbonToken.deploy("CarbonToken", "CT");
    await carbonToken.waitForDeployment();

    // Deploy Registry with `owner` as admin
    BlueCarbonRegistry = await ethers.getContractFactory("BlueCarbonRegistry");
    registry = await BlueCarbonRegistry.deploy(owner.address);
    await registry.waitForDeployment();

    // Link CarbonToken to Registry
    await registry.setCarbonToken(await carbonToken.getAddress());

    // Give registry ISSUER_ROLE on CarbonToken so it can mint
    const ISSUER_ROLE = await carbonToken.ISSUER_ROLE();
    await carbonToken.connect(owner).grantRole(ISSUER_ROLE, await registry.getAddress());
  });

  it("Should register a project", async function () {
    const tx = await registry.registerProject(
      "Mangrove Project",
      "Kerala Coastline",
      100,
      projectOwner.address,
      "ipfs://projectMetadata"
    );

    const receipt = await tx.wait();
    const projectId = receipt.logs[0].args.projectId;

    const project = await registry.getProject(projectId);
    expect(project[0]).to.equal("Mangrove Project");
    expect(project[3]).to.equal(projectOwner.address);
  });

  it("Should upload and verify evidence with NFT + ERC20 credits", async function () {
    // Register project first
    await registry.registerProject(
      "Seagrass Project",
      "Tamil Nadu",
      200,
      projectOwner.address,
      "ipfs://seagrass"
    );

    // Upload evidence
    const evidenceHash = ethers.keccak256(ethers.toUtf8Bytes("dummyEvidence"));
    await registry.connect(projectOwner).uploadEvidence(1, evidenceHash, "ipfs://evidence");

    // Verify & issue NFT + tokens
    await registry.verifyEvidenceAndIssue(
      1,
      true,
      "ipfs://receipt",
      ethers.parseUnits("1000", 18)
    );

    // Check balances
    const bal = await carbonToken.balanceOf(projectOwner.address);
    expect(bal).to.equal(ethers.parseUnits("1000", 18));

    const evidence = await registry.getEvidence(1);
    expect(evidence.verified).to.equal(true);
    expect(evidence.receiptTokenId).to.not.equal(0);
  });
});
