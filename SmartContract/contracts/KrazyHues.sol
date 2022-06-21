// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract KrazyHues is Ownable {
    address payable[] public players;
    uint256 public entryFee;
    address payable public recentWinner;
    AggregatorV3Interface internal ethPriceFeed;
    enum GAME_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    GAME_STATE public game_state;

    constructor(address _priceFeedAddress) public {
        entryFee = 50 * (10**18); // 12.81 dollars is around 1000 rupees
        ethPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        game_state = GAME_STATE.CLOSED;
    }

    function enter() public payable {
        require(game_state == GAME_STATE.OPEN, "The game hasn't started yet!");
        require(
            msg.value >= getEntranceFee(),
            "Not enough ETH to enter the game!"
        );
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 Decimals
        uint256 costToEnter = (entryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startGame() public onlyOwner {
        require(game_state == GAME_STATE.CLOSED, "Can't start a new game yet!");
        game_state = GAME_STATE.OPEN;
    }

    function endGame() public onlyOwner {
        game_state = GAME_STATE.CALCULATING_WINNER;
        recentWinner = players[0];
        recentWinner.transfer(address(this).balance);

        // Reset
        players = new address payable[](0);
        game_state = GAME_STATE.CLOSED;
    }
}
