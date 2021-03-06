// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// ************ TODO emit winner 
// https://www.tutorialspoint.com/solidity/solidity_events.htm

interface IERC20 {
    function transfer(address _to, uint256 _amount) external returns (bool);
}

contract WinnerPicker is VRFConsumerBase, Ownable {
    bytes32 internal keyHash;
    uint256 internal fee;
    string[] public winnersPublic;

    uint256 public randomResult;

    // Lottery picker
    function pickWinners(uint256 numberOfWinners, string[] memory contestants)
        external
        returns (string[] memory winners)
    {
        require(numberOfWinners > 0);
        require(numberOfWinners <= contestants.length);
        getRandomNumber();
        // TODO make expand only return unique numbers
        uint256[] memory randomNumberArray = expand(
            randomResult,
            numberOfWinners
        );
        require(randomNumberArray.length == numberOfWinners);
        string[] memory winnersArray = new string[](numberOfWinners);
        require(winnersArray.length == numberOfWinners);

        for (uint256 y = 0; y < numberOfWinners; y++) {
            uint256 index = randomNumberArray[y] % numberOfWinners;
            winnersArray[y] = contestants[index];
        }
        winners = winnersArray;
        return winnersArray;
    }

    function withdrawToken(address _tokenContract, uint256 _amount) external onlyOwner{
        IERC20 tokenContract = IERC20(_tokenContract);
        
        // transfer the token from address of this contract
        // to address of the user (executing the withdrawToken() function)
        tokenContract.transfer(msg.sender, _amount);
    }

    /**
     * Constructor inherits VRFConsumerBase
     *
     * Network: Kovan
     * Chainlink VRF Coordinator address: 0xdD3782915140c8f3b190B5D67eAc6dc5760C46E9
     * LINK token address:                0xa36085F69e2889c224210F603D836748e7dC0088
     * Key Hash: 0x6c3699283bda56ad74f6b855546325b68d482e983852a7a82979cc4807b641f4
     */
    constructor(
        bytes32 _keyhash,
        address _vrfCoordinator,
        address _linkToken,
        uint256 _fee
    )
        VRFConsumerBase(
            _vrfCoordinator, // VRF Coordinator
            _linkToken // LINK Token
        )
    {
        keyHash = _keyhash;
        // fee = 0.1 * 10 ** 18; // 0.1 LINK
        fee = _fee;
    }

    /**
     * Requests randomness
     */
    function getRandomNumber() internal returns (bytes32 requestId) {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Not enough LINK - fill contract with faucet"
        );
        return requestRandomness(keyHash, fee);
    }

    /**
     * Callback function used by VRF Coordinator
     */
    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        randomResult = randomness;
    }

    function expand(uint256 randomValue, uint256 n)
        internal
        pure
        returns (uint256[] memory expandedValues)
    {
        expandedValues = new uint256[](n);
        for (uint256 i = 0; i < n; i++) {
            expandedValues[i] = uint256(keccak256(abi.encode(randomValue, i)));
        }
        return expandedValues;
    }
}
