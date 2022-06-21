from scripts.support_scripts import get_account, get_contract, withdraw
from brownie import KrazyHues
import time


def deploy_krazyhues():
    account = get_account()
    krazyhues = KrazyHues.deploy(
        get_contract("eth_usd_price_feed").address, {"from": account}
    )
    print("DEPLOYED KRAZYHUES!")
    return krazyhues


def start_game():
    account = get_account()
    krazyhues = KrazyHues[-1]
    starting_tx = krazyhues.startGame({"from": account})
    starting_tx.wait(1)
    print("The game has started!")


def enter_game():
    account = get_account()
    krazyhues = KrazyHues[-1]
    value = krazyhues.getEntranceFee() + 100000000
    tx = krazyhues.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the game!")


def end_game():
    account = get_account()
    krazyhues = KrazyHues[-1]
    ending_transaction = krazyhues.endGame({"from": account})
    ending_transaction.wait(1)
    time.sleep(5)
    print(f"{krazyhues.recentWinner()} is the new winner!")


def main():
    deploy_krazyhues()
    start_game()
    enter_game()
    end_game()
