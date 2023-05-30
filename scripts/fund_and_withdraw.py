from brownie import FundMe, MockV3Aggregator
from scripts.helpful_scripts import get_account


def fund():
    account = get_account()
    fund_me = FundMe[-1]
    eth_amount = fund_me.getEntranceFee()
    print(f"The Curent Entrance Fee is {eth_amount}")
    print("Funding..")
    fund_tx = fund_me.fund({"from": account, "value": eth_amount})
    print("Funded!!")


def withdraw():
    account = get_account()
    fund_me = FundMe[-1]
    print("Withdrawing..")
    withdraw_tx = fund_me.withdraw({"from": account})
    print("Withdrawed!!")


def main():
    fund()
    withdraw()
