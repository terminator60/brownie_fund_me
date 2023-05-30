from brownie import accounts, FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_DEVELOPMENT_BLOCKCHAINS,
)


def deploy_contract():
    account = get_account()

    if network.show_active() not in LOCAL_DEVELOPMENT_BLOCKCHAINS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_USD_price_feed_address"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    print("Deploying Contract..")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("publish"),
    )
    print(f"Contact Deployed at Address - {fund_me.address}")
    return fund_me


def main():
    deploy_contract()
