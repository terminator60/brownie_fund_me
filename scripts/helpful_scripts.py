from brownie import network, accounts, config, MockV3Aggregator

LOCAL_DEVELOPMENT_BLOCKCHAINS = ["development", "ganache-local"]
LOCAL_FORKED_BLOCKCHAINS = ["mainnet-fork-dev"]

DECIMALS = 8
INITIAL_VALUE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_DEVELOPMENT_BLOCKCHAINS
        or network.show_active() in LOCAL_FORKED_BLOCKCHAINS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"Active network is {network.show_active()}")
    print("Deploying Mocks...")
    mock_aggregator = MockV3Aggregator.deploy(
        DECIMALS, INITIAL_VALUE, {"from": get_account()}
    )
    price_feed_address = mock_aggregator.address
    print("Mocks Deployed!")
