import random
from collections import Counter

def play_number_gamble(balance):
    print("\nWelcome to the Number Gamble Game!")
    print(f"Your current balance: {balance} coins")

    bet = int(input("How many coins do you want to bet? "))

    if bet > balance or bet <= 0:
        print("Invalid bet amount.")
        return balance

    player_number = int(input("Pick a number between 1 and 10: "))
    computer_number = random.randint(1, 10)
    print(f"The computer chose {computer_number}.")

    if player_number == computer_number:
        print("You won! Doubling your bet!")
        balance += bet
    else:
        print("You lost!")
        balance -= bet

    return balance


def play_blackjack(balance):
    print("\nWelcome to Blackjack!")
    print(f"Your current balance: {balance} coins")

    bet = int(input("How many coins do you want to bet? "))

    if bet > balance or bet <= 0:
        print("Invalid bet amount.")
        return balance

    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    player_hand = [random.choice(cards), random.choice(cards)]
    dealer_hand = [random.choice(cards), random.choice(cards)]

    print(f"Your cards: {player_hand}, total = {sum(player_hand)}")
    print(f"Dealer shows: {dealer_hand[0]}")

    while sum(player_hand) < 21:
        move = input("Do you want to (h)it or (s)tand? ").lower()
        if move == "h":
            player_hand.append(random.choice(cards))
            print(f"Your cards: {player_hand}, total = {sum(player_hand)}")
        elif move == "s":
            break
        else:
            print("Invalid input. Please choose 'h' or 's'.")

    player_total = sum(player_hand)
    dealer_total = sum(dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(random.choice(cards))
        dealer_total = sum(dealer_hand)

    print(f"Dealer's cards: {dealer_hand}, total = {dealer_total}")

    if player_total > 21:
        print("You busted! Dealer wins.")
        balance -= bet
    elif dealer_total > 21 or player_total > dealer_total:
        print("You win!")
        balance += bet
    elif player_total == dealer_total:
        print("It's a tie!")
    else:
        print("Dealer wins.")
        balance -= bet

    return balance

spin_stats = {
    "total": Counter(),
    "rows": {"top": Counter(), "middle": Counter(), "bottom": Counter()},
    "spins_played": 0,
    "last_middle": None,
    "current_middle_streak": 0,
    "max_middle_streak": 0
}

def play_slot_machine(balance):
    symbols = ["Cherry", "Lemon", "Orange", "Bell", "Seven"]
    drum1 = [0,1,3,4,2]
    drum2 = [2,4,0,1,3]
    drum3 = [3,2,1,4,0]

    print("\nWelcome to the Slot Machine!")
    print(f"Your current balance: {balance} coins")

    bet = int(input("Enter your bet amount: "))
    if bet > balance or bet <= 0:
        print("Invalid bet amount.")
        return balance
    n = len(drum1)
    spin = [random.choice(symbols) for _ in range(3)]
    spin1 = random.randrange(0,4)
    spin2 = random.randrange(0,4)
    spin3 = random.randrange(0,4)
    top = [
           
            symbols[drum1[(spin1-1) % n]],
            symbols[drum2[(spin2-1) % n]],
            symbols[drum3[(spin3-1) % n]]
        ]
    middle = [
            symbols[drum1[spin1]],
            symbols[drum2[spin2]],
            symbols[drum3[spin3]]
        ]
    bottom = [
            symbols[drum1[(spin1+1) % n]],
            symbols[drum2[(spin2+1) % n]],
            symbols[drum3[(spin3+1) % n]]
        ]
    print(f". [ {symbols[drum1[(spin1-1) % 4]]} ] [ {symbols[drum2[(spin2-1) % 4]]} ] [ {symbols[drum3[(spin3-1) % 4]]} ]. ")
    print(f"--[ {symbols[drum1[spin1]]} ] [ {symbols[drum2[spin2]]} ] [ {symbols[drum3[spin3]]} ]--")
    print(f". [ {symbols[drum1[(spin1+1) % 4]]} ] [ {symbols[drum2[(spin2+1) % 4]]} ] [ {symbols[drum3[(spin3+1) % 4]]} ]. ")
def evaluate_spin(top, middle, bottom, bet):
    winnings = 0
    if middle[0] == middle[1] == middle[2]:
        winnings += bet * 5
        print("Jackpot! Middle row three of a kind!")
    elif top[0] == top[1] == top[2]:
        winnings += bet * 3
        print("Top row three of a kind!")
    elif bottom[0] == bottom[1] == bottom[2]:
        winnings += bet * 3
        print("Bottom row three of a kind!")
    elif middle[0] == middle[1] or middle[1] == middle[2] or middle[0] == middle[2]:
        winnings += bet * 2
        print("Middle row two of a kind!")
    elif top[0] == middle[1] == bottom[2] or bottom[0] == middle[1] == top[2] or top[2] == middle[1] == bottom[0] or bottom[2] == middle[1] == top[0]:
        winnings += bet * 4
        print("Diagonal three of a kind!")

    return winnings

def roll_dice():
    return [random.randint(1, 6) for _ in range(5)]

def evaluate_hand(dice):
    counts = Counter(dice)
    freq = sorted(counts.values(), reverse=True)
    unique_sorted = sorted(set(dice))

    if freq == [5]:
        return "Five of a kind"
    if freq == [4, 1]:
        return "Four of a kind"
    if freq == [3, 2]:
        return "Full house"
    if unique_sorted == [1, 2, 3, 4, 5] or unique_sorted == [2, 3, 4, 5, 6]:
        return "Straight"
    if freq == [3, 1, 1]:
        return "Three of a kind"
    if freq == [2, 2, 1]:
        return "Two pairs"
    if freq == [2, 1, 1, 1]:
        return "One pair"
    return "Nothing"

def payout_multiplier(category):
    table = {
        "Five of a kind": 10,
        "Four of a kind": 7,
        "Full house": 5,
        "Straight": 4,
        "Three of a kind": 3,
        "Two pairs": 2,
        "One pair": 1,
        "Nothing": 0
    }
    return table.get(category, 0)

def play_poker_dice(balance):
    print(f"\nCurrent balance: {balance} coins")
    try:
        bet = int(input("Enter your bet amount: "))
    except ValueError:
        print("Invalid number.")
        return balance

    if bet <= 0 or bet > balance:
        print("Invalid bet amount.")
        return balance

    dice = roll_dice()
    print("You rolled:", dice)
    category = evaluate_hand(dice)
    print("Result:", category)

    mult = payout_multiplier(category)
    if mult == 0:
        print(f"You lose {bet} coins.")
        balance -= bet
    else:
        winnings = bet * mult
        print(f"You win! Payout: {winnings} coins ({mult}×).")
        balance += winnings

    return balance




def main():
    balance = 20
    print("Welcome to The Gambling House 4.0")

    while True:
        print("\n====== MAIN MENU ======")
        print("1. Play Slot Machine")
        print("2. Play number gamble")
        print("3. Play Blackjack")
        print("4. Check balance")
        print("5. Play Poker Dice")
        print("6. Quit")
        print("=========================")


        choice = input("Choose an option (1-6): ")

        if choice == "1":
            balance = play_slot_machine(balance)
        elif choice == "4":
            print(f"Your current balance: {balance} coins")
        elif choice == "3":
            balance = play_blackjack(balance)
        elif choice == "2":
            balance = play_number_gamble(balance)
        elif choice == "5":
            balance = play_poker_dice(balance)
        elif choice == "6":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Try again.")

        if balance <= 0:
            print("You're out of coins! Game over.")
            break

main()
