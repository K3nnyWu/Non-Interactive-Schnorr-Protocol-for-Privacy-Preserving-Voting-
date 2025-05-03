const { expect } = require("chai");

describe("PrivateVoting", function () {
  it("Should verify a valid Schnorr proof", async function () {
    const PrivateVoting = await ethers.getContractFactory("PrivateVoting");
    const voting = await PrivateVoting.deploy();
    await voting.deployed();

    const tx = await voting.vote(123, 456, 789, 101112, 131415);
    await tx.wait();

    expect(await voting.hasVoted(owner.address)).to.be.true;
  });
});