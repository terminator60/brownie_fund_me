// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToBalance;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Unauthorized User");
        _;
    }

    function fund() public payable {
        uint256 minimum_USD = 50 * 10 ** 18;
        require(
            ethConversionRate(msg.value) >= minimum_USD,
            "Send more ETH!!!"
        );
        addressToBalance[msg.sender] = msg.value;
        funders.push(msg.sender);
    }

    function priceFeed_Version() public view returns (uint256) {
        return priceFeed.version();
    }

    function get_EthUSDRate() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * (10 ** 10));
    }

    // 1905.55000000000000000

    function ethConversionRate(
        uint256 _ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = get_EthUSDRate();
        uint256 ethAmountinUSD = (ethPrice * _ethAmount) / (10 ** 18);
        return ethAmountinUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 price = get_EthUSDRate();
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 precision = 1 * 10 ** 18;
        return ((minimumUSD * precision) / price) + 1;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 index; index < funders.length; index++) {
            addressToBalance[funders[index]] = 0;
        }
        funders = new address[](0);
    }
}
