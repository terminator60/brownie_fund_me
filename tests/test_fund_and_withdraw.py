from brownie import FundMe, MockV3Aggregator, network, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_DEVELOPMENT_BLOCKCHAINS
from scripts.deploy import deploy_contract
import pytest


def test_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_contract()
    eth_amount = fund_me.getEntranceFee()
    fund_tx = fund_me.fund({"from": account, "value": eth_amount})
    fund_tx.wait(1)
    assert fund_me.addressToBalance(account.address) == eth_amount

    withdraw_tx = fund_me.withdraw({"from": account})
    withdraw_tx.wait(1)
    assert fund_me.addressToBalance(account.address) == 0


def test_only_onwer_can_withdraw():
    if network.show_active() not in LOCAL_DEVELOPMENT_BLOCKCHAINS:
        pytest.skip("Only for Local Testing")
    fund_me = deploy_contract()
    bad_actor = accounts.add()
    # with pytest.raises(exceptions.VirtualMachineError):
    fund_me.withdraw({"from": bad_actor})
