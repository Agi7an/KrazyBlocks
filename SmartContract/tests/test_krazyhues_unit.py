from brownie import KrazyHues, network, config, accounts, exceptions
from scripts.deploy_game import deploy_krazyhues
from scripts.support_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    krazyhues = deploy_krazyhues()
    expectedFee = Web3.toWei(0.025, "ether")
    entranceFee = krazyhues.getEntranceFee()
    assert expectedFee == entranceFee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    krazyhues = deploy_krazyhues()
    with pytest.raises(exceptions.VirtualMachineError):
        krazyhues.enter({"from": get_account(), "value": krazyhues.getEntranceFee()})


def test_can_start_and_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    krazyhues = deploy_krazyhues()
    account = get_account()
    krazyhues.startGame({"from": account})
    krazyhues.enter({"from": account, "value": krazyhues.getEntranceFee()})
    assert krazyhues.players(0) == account


def test_can_end_game():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    krazyhues = deploy_krazyhues()
    account = get_account()
    krazyhues.startGame({"from": account})
    krazyhues.enter({"from": account, "value": krazyhues.getEntranceFee()})
    krazyhues.endGame({"from": account})
    assert krazyhues.game_state == 2


def test_handles_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    krazyhues = deploy_krazyhues()
    account = get_account()
    krazyhues.startGame({"from": account})
    krazyhues.enter({"from": account, "value": krazyhues.getEntranceFee()})
    krazyhues.enter({"from": get_account(index=1), "value": krazyhues.getEntranceFee()})
    transaction = krazyhues.endGame({"from": account})
    starting_balance_of_account = account.balance()
    balance_of_krazyhues = krazyhues.balance()
    assert krazyhues.recentWinner() == account
    assert krazyhues.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_krazyhues
