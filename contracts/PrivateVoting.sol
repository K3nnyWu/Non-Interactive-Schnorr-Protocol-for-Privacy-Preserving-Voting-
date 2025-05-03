// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract PrivateVoting {
    using ECDSA for bytes32;

    mapping(address => bool) public hasVoted;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Voting function with ECDSA signature validation
    function vote(bytes memory signature, bytes32 messageHash) external {
        require(!hasVoted[msg.sender], "Already voted");

        // Recover the signer from the signature
        address signer = messageHash.recover(signature);
        require(signer == msg.sender, "Invalid signature");

        hasVoted[msg.sender] = true;
    }

    // Optional: Function to allow owner to reset voting status (for testing or reuse)
    function resetVoter(address voter) external {
        require(msg.sender == owner, "Only owner can reset");
        hasVoted[voter] = false;
    }
}