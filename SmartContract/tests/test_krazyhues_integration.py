from brownie import network
from scripts.deploy_game import deploy_krazyhues
from scripts.support_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    krazyhues = deploy_krazyhues()
    account = get_account()
    krazyhues.startGame({"from": account})
    krazyhues.enter({"from": account, "value": krazyhues.getEntranceFee()})
    krazyhues.enter({"from": account, "value": krazyhues.getEntranceFee()})
    krazyhues.endGame({"from": account})
    starting_balance_of_account = account.balance()
    balance_of_krazyhues = krazyhues.balance()
    assert krazyhues.recentWinner() == account
    assert krazyhues.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_krazyhues
