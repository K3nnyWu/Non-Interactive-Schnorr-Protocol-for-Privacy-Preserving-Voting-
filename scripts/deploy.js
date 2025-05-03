const hre = require("hardhat");

async function main() {
  const PrivateVoting = await hre.ethers.getContractFactory("PrivateVoting");
  const voting = await PrivateVoting.deploy();
  await voting.waitForDeployment();
  const contractAddress = await voting.getAddress();
  console.log("PrivateVoting deployed to:", contractAddress);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});