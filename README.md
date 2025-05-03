# Project Directory Structure

- **voting-system/**
  - **contracts/**
    - `PrivateVoting.sol` *Solidity smart contract (Step 2)*
  - **scripts/**
    - `deploy.js` *Deployment script*
  - **test/**
    - `PrivateVoting_test.js` *Test script*
  - `hardhat.config.js` *Hardhat configuration file*
  - **schnorr_prover/**
    - `schnorr_prover.py` *Python script (this project)*
    - `vote.py` *Python script interacting with the smart contract*

# How to Deploy and Test Contract

1. **Compile Contract:**
   ```bash
   npx hardhat compile
