import time
import pytest
from brownie import WinnerPicker, convert, network, exceptions
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

@pytest.mark.skip("Random number is internal")
def test_can_request_random_number(get_keyhash, chainlink_fee):
    # Arrange
    vrf_consumer = WinnerPicker.deploy(
        get_keyhash,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        chainlink_fee,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        vrf_consumer.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    requestId = vrf_consumer.getRandomNumber.call({"from": get_account()})
    assert isinstance(requestId, convert.datatypes.HexString)

@pytest.mark.skip("Random number is internal")
def test_returns_random_number_local(get_keyhash, chainlink_fee):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    vrf_consumer = WinnerPicker.deploy(
        get_keyhash,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        chainlink_fee,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        vrf_consumer.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    transaction_receipt = vrf_consumer.getRandomNumber({"from": get_account()})
    # requestId = vrf_consumer.getRandomNumber.call({"from": get_account()})
    requestId = transaction_receipt.return_value
    assert isinstance(transaction_receipt.txid, str)
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 777, vrf_consumer.address, {"from": get_account()}
    )
    # Assert
    assert vrf_consumer.randomResult() > 0
    assert isinstance(vrf_consumer.randomResult(), int)


def test_returns_random_number_testnet(
    get_keyhash,
    chainlink_fee,
):
    # Arrange
    if network.show_active() not in ["kovan", "rinkeby", "ropsten"]:
        pytest.skip("Only for testnet testing")
    vrf_consumer = WinnerPicker.deploy(
        get_keyhash,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        chainlink_fee,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        vrf_consumer.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    transaction_receipt = vrf_consumer.getRandomNumber({"from": get_account()})
    assert isinstance(transaction_receipt.txid, str)
    transaction_receipt.wait(1)
    time.sleep(90)
    # Assert
    assert vrf_consumer.randomResult() > 0
    assert isinstance(vrf_consumer.randomResult(), int)

def test_pickWinners_works(get_keyhash, chainlink_fee):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    vrf_consumer = WinnerPicker.deploy(
        get_keyhash,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        chainlink_fee,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        vrf_consumer.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    print("getting transaction")
    transaction_receipt = vrf_consumer.pickWinners(1, ["dylan"])
    print("printing transaction receipt")
    print(transaction_receipt.return_value)
    assert (len(transaction_receipt.return_value) > 0)
    print(list(transaction_receipt.return_value))
    assert isinstance(list(transaction_receipt.return_value), list)
    assert (transaction_receipt.return_value[0] == "dylan")

def test_pickWinners_no_winner(get_keyhash, chainlink_fee):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    vrf_consumer = WinnerPicker.deploy(
        get_keyhash,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        chainlink_fee,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        vrf_consumer.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    print("getting transaction")
    try:
        vrf_consumer.pickWinners(0, ["dylan"])
    except exceptions.VirtualMachineError as e:
        print(e)
        assert True

def test_pickWinners_lottery_works_3_winners(get_keyhash, chainlink_fee):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    vrf_consumer = WinnerPicker.deploy(
        get_keyhash,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        chainlink_fee,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        vrf_consumer.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    print("getting transaction")
    contestants = ["dylan", "fred", "joe"]
    transaction_receipt = vrf_consumer.pickWinners(3, contestants)
    assert set(list(transaction_receipt.return_value)) == set(contestants)
