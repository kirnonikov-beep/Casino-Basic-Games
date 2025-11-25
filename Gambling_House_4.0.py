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




def main():
    balance = 20
    print("Welcome to The Gambling House 4.0")

    while True:
        print("\n====== MAIN MENU ======")
        print("1. Play Slot Machine")
        print("2. Play number gamble")
        print("3. Play Blackjack")
        print("4. Check balance")
        print("5. Quit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            balance = play_slot_machine(balance)
        elif choice == "4":
            print(f"Your current balance: {balance} coins")
        elif choice == "3":
            balance = play_blackjack(balance)
        elif choice == "2":
            balance = play_number_gamble(balance)
        elif choice == "5":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Try again.")

        if balance <= 0:
            print("You're out of coins! Game over.")
            break

main()
