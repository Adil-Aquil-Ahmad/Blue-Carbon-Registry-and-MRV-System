// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/*
 BlueCarbonRegistry.sol
 - BlueCarbonRegistry: manages projects, evidence anchoring, verification, and issues NFTs (receipts)
 - CarbonToken: an ERC20 token representing fungible carbon credits
 - AccessControl: role-based verifier/issuer management
*/

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CarbonToken is ERC20, ERC20Burnable, AccessControl {
    bytes32 public constant ISSUER_ROLE = keccak256("ISSUER_ROLE");

    constructor(string memory name_, string memory symbol_) ERC20(name_, symbol_) {
        // grant deployer admin role
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function mint(address to, uint256 amount) external onlyRole(ISSUER_ROLE) {
        _mint(to, amount);
    }
}

/**
 * @title BlueCarbonRegistry
 * @notice Registry for blue carbon restoration projects, MRV evidence anchoring,
 *         verifier/admin roles, NFT receipts, and issuance of fungible carbon tokens.
 */
contract BlueCarbonRegistry is ERC721URIStorage, AccessControl, Ownable {
    bytes32 public constant VERIFIER_ROLE = keccak256("VERIFIER_ROLE");

    CarbonToken public carbonToken; // Address of ERC20 token for credits

    uint256 public totalProjects;
    uint256 private _nextEvidenceId;
    uint256 private _nextReceiptTokenId;
    
    
    struct Project {
        string name;
        string location; // can be human-readable or geojson string
        uint256 area; // in hectares (or m^2 as you prefer)
        address owner; // NGO / community wallet
        string metadataURI; // IPFS metadata for the project
        bool exists;
        uint256 totalIssuedCredits; // total fungible credits issued (in token smallest unit)
    }

    struct Evidence {
        uint256 projectId;
        bytes32 evidenceHash; // SHA-256 hash of evidence file(s)
        string evidenceURI; // IPFS CID or metadata URI
        address uploader;
        bool verified;
        uint256 timestamp;
        uint256 receiptTokenId; // NFT receipt minted after verification (0 if none)
    }

    // storage
    mapping(uint256 => Project) public projects; // projectId => Project
    mapping(uint256 => Evidence) public evidences; // evidenceId => Evidence

    // events
    event ProjectRegistered(uint256 indexed projectId, address indexed owner, string name, string metadataURI);
    event EvidenceUploaded(uint256 indexed evidenceId, uint256 indexed projectId, bytes32 evidenceHash, string evidenceURI, address uploader);
    event EvidenceVerified(uint256 indexed evidenceId, uint256 indexed projectId, address verifier, uint256 receiptTokenId);
    event CreditsMinted(uint256 indexed projectId, address indexed to, uint256 amount);
    event ReceiptMinted(uint256 indexed tokenId, uint256 indexed evidenceId, address indexed to);
    event ReceiptRetired(uint256 indexed tokenId, address indexed owner);

    // constructor
    constructor(address admin) ERC721("BlueCarbonReceipt", "BCR") Ownable(admin) {
        // set admin roles and ownership
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(VERIFIER_ROLE, admin);

        // set owner to admin
        transferOwnership(admin);
    }

    // -------------------------
    // ADMIN & ROLE MANAGEMENT
    // -------------------------

    function setCarbonToken(address tokenAddress) external onlyOwner {
        require(tokenAddress != address(0), "Invalid token address");
        carbonToken = CarbonToken(tokenAddress);
    }

    function addVerifier(address verifier) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(VERIFIER_ROLE, verifier);
    }

    function removeVerifier(address verifier) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(VERIFIER_ROLE, verifier);
    }

    // -------------------------
    // PROJECT LIFECYCLE
    // -------------------------

    /**
     * @notice Register a new restoration project
     * @param name Project name
     * @param location Human readable location or geojson
     * @param area Area measure (units documented by off-chain)
     * @param ownerAddr Wallet address that will receive credits
     * @param metadataURI IPFS metadata URI describing the project
     * @return projectId newly assigned id
     */
    function registerProject(
        string memory name,
        string memory location,
        uint256 area,
        address ownerAddr,
        string memory metadataURI
    ) external onlyOwner returns (uint256 projectId) {
        require(ownerAddr != address(0), "Owner address required");
        projectId = totalProjects + 1;
        projects[projectId] = Project({
            name: name,
            location: location,
            area: area,
            owner: ownerAddr,
            metadataURI: metadataURI,
            exists: true,
            totalIssuedCredits: 0
        });
        totalProjects = projectId;

        emit ProjectRegistered(projectId, ownerAddr, name, metadataURI);
    }

    function updateProjectMetadata(uint256 projectId, string memory metadataURI) external {
        require(projects[projectId].exists, "Project not found");
        require(msg.sender == owner() || msg.sender == projects[projectId].owner, "Only owner or project owner");
        projects[projectId].metadataURI = metadataURI;
    }

    // -------------------------
    // EVIDENCE / MRV
    // -------------------------

    /**
     * @notice Upload an evidence anchor (off-chain file hashed + stored in IPFS)
     * @param projectId project the evidence belongs to
     * @param evidenceHash SHA-256 (or chosen) hash of the evidence payload
     * @param evidenceURI IPFS CID or URI for details
     * @return evidenceId
     */
    function uploadEvidence(
        uint256 projectId,
        bytes32 evidenceHash,
        string memory evidenceURI
    ) external returns (uint256 evidenceId) {
        require(projects[projectId].exists, "Project not found");
        evidenceId = ++_nextEvidenceId;
        evidences[evidenceId] = Evidence({
            projectId: projectId,
            evidenceHash: evidenceHash,
            evidenceURI: evidenceURI,
            uploader: msg.sender,
            verified: false,
            timestamp: block.timestamp,
            receiptTokenId: 0
        });

        emit EvidenceUploaded(evidenceId, projectId, evidenceHash, evidenceURI, msg.sender);
    }

    /**
     * @notice Verifier approves evidence -> optional mint receipt NFT and/or mint fungible credits
     * @param evidenceId evidence to verify
     * @param mintReceipt whether to mint an NFT receipt for the evidence (true = mint)
     * @param receiptTokenURI tokenURI for the NFT receipt if minted
     * @param mintFungibleAmount amount of ERC20 token to mint to project owner (in token base units)
     */
    function verifyEvidenceAndIssue(
        uint256 evidenceId,
        bool mintReceipt,
        string memory receiptTokenURI,
        uint256 mintFungibleAmount
    ) external onlyRole(VERIFIER_ROLE) returns (uint256 receiptTokenId) {
        Evidence storage ev = evidences[evidenceId];
        require(ev.timestamp != 0, "Evidence not found");
        require(!ev.verified, "Already verified");

        ev.verified = true;

        // Mint receipt NFT if requested
        if (mintReceipt) {
            _nextReceiptTokenId++;
            receiptTokenId = _nextReceiptTokenId;
            _safeMint(ev.uploader, receiptTokenId); // mint to uploader (could be project owner or uploader)
            if (bytes(receiptTokenURI).length > 0) {
                _setTokenURI(receiptTokenId, receiptTokenURI);
            }
            ev.receiptTokenId = receiptTokenId;
            emit ReceiptMinted(receiptTokenId, evidenceId, ev.uploader);
        }

        // Mint fungible credits if requested and CarbonToken is set
        if (mintFungibleAmount > 0) {
            require(address(carbonToken) != address(0), "Carbon token not set");
            address projectOwner = projects[ev.projectId].owner;
            // The registry must hold ISSUER_ROLE on the CarbonToken contract for this to succeed
            carbonToken.mint(projectOwner, mintFungibleAmount);
            projects[ev.projectId].totalIssuedCredits += mintFungibleAmount;
            emit CreditsMinted(ev.projectId, projectOwner, mintFungibleAmount);
        }

        emit EvidenceVerified(evidenceId, ev.projectId, msg.sender, ev.receiptTokenId);
    }

    // -------------------------
    // NFT & CREDIT UTILITIES
    // -------------------------

    /// Wrapper to transfer a receipt NFT (standard ERC721 transfer allowed too)
    function transferReceipt(address to, uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        safeTransferFrom(msg.sender, to, tokenId);
        emit ReceiptMinted(tokenId, 0, to); // note: emit a mint-like event for transfer (or remove if not desired)
    }

    /// Retire (burn) a receipt NFT
    function retireReceipt(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        _burn(tokenId);
        emit ReceiptRetired(tokenId, msg.sender);
    }

    /// Admin / owner can withdraw accidentally sent ERC20 tokens (safety)
    function rescueERC20(address tokenAddr, address to, uint256 amount) external onlyOwner {
        IERC20(tokenAddr).transfer(to, amount);
    }

    // -------------------------
    // READ HELPERS
    // -------------------------

    function getProject(uint256 projectId) external view returns (
        string memory name,
        string memory location,
        uint256 area,
        address ownerAddr,
        string memory metadataURI,
        bool exists,
        uint256 totalIssued
    ) {
        Project memory p = projects[projectId];
        return (p.name, p.location, p.area, p.owner, p.metadataURI, p.exists, p.totalIssuedCredits);
    }
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function getEvidence(uint256 evidenceId) external view returns (
        uint256 projectId,
        bytes32 evidenceHash,
        string memory evidenceURI,
        address uploader,
        bool verified,
        uint256 timestamp,
        uint256 receiptTokenId
    ) {
        Evidence memory e = evidences[evidenceId];
        return (e.projectId, e.evidenceHash, e.evidenceURI, e.uploader, e.verified, e.timestamp, e.receiptTokenId);
    }

    // -------------------------
    // Misc
    // -------------------------
    receive() external payable {}
    fallback() external payable {}
}
