import random
from collections import Counter

def play_number_gamble(balance):
    print("\nWelcome to the Number Gamble Game!V1.5")
    print(f"Your current balance: {balance} coins")

    bet = int(input("How many coins do you want to bet? "))

    if bet > balance or bet <= 0:
        print("Invalid bet amount. Loans haven't been invented yet, so you can't bet more than you have.")
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


def create_shoe():
    """Create a shoe with 4 decks shuffled together."""
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    shoe = deck * 4
    random.shuffle(shoe)
    return shoe

def play_blackjack(balance):
    print("\nWelcome to Blackjack!V7.4")
    print(f"Your current balance: {balance} coins")

    bet = int(input("How many coins do you want to bet? "))

    if bet > balance or bet <= 0:
        print("Invalid bet amount. Loans haven't been invented yet, so you can't bet more than you have.")
        return balance
    shoe = create_shoe()
    player_hand = [shoe.pop(), shoe.pop()]
    if len(shoe) < 10:
        shoe = create_shoe()
    if sum(player_hand) == 21:
        print(f"Your cards: {player_hand}, total = {sum(player_hand)}")
        print("Blackjack! You win!")
        balance += int(1.5 * bet)
        return balance
    dealer_hand = [shoe.pop(), shoe.pop()]
    if sum(dealer_hand) == 21:
        print(f"Dealer's cards: {dealer_hand}, total = {sum(dealer_hand)}")
        print("Dealer has Blackjack! You lose.")
        balance -= bet
        return balance
    elif sum(dealer_hand) == 21 and sum(player_hand) == 21:
        print(f"Dealer's cards: {dealer_hand}, total = {sum(dealer_hand)}")
        print("Both have Blackjack! It's a tie.")
        balance += bet
        return balance

    print(f"Your cards: {player_hand}, total = {sum(player_hand)}")
    print(f"Dealer shows: {dealer_hand[0]}")

    while sum(player_hand) < 21:
        move = input("Do you want to (h)it or (s)tand or (d)ouble or S(p)lit? ").lower()
        if move == "h":
            player_hand.append(shoe.pop())
            if len(shoe) < 10:
                shoe = create_shoe()
            print(f"Your cards: {player_hand}, total = {sum(player_hand)}")
        elif move == "s":
            break
        elif move == "d":
            if bet <= balance:
                bet *= 2
                print("You doubled your bet.")
                player_hand.append(shoe.pop())
                if len(shoe) < 10:
                    shoe = create_shoe()
                print(f"Your cards: {player_hand}, total = {sum(player_hand)}")
                
                break
            else:
                print("Not enough coins to double your bet.")
        elif move == "p":
            if player_hand[0] == player_hand[1] and bet <= balance:
                print("You split your hand.")
                balance -= bet   # pay second bet

                first_bet = bet
                second_bet = bet
                first_hand = [player_hand[0], shoe.pop()]
                second_hand = [player_hand[1], shoe.pop()]

                if len(shoe) < 10:
                    shoe = create_shoe()

                print(f"First hand: {first_hand}, total = {sum(first_hand)}")
                print(f"Second hand: {second_hand}, total = {sum(second_hand)}")

                for hand, hand_bet in [(first_hand, first_bet), (second_hand, second_bet)]:
                    while sum(hand) < 21:
                        move = input(f"Do you want to (h)it or (s)tand for hand {hand}? ").lower()
                        if move == "h":
                            hand.append(shoe.pop())
                        if len(shoe) < 10:
                            shoe = create_shoe()
                        print(f"Hand: {hand}, total = {sum(hand)}")
                        if move == "s":
                            break

    else:
        print("Invalid input. Please choose 'h' or 's' or 'd' or 'p'.")

    player_total = sum(player_hand)
    dealer_total = sum(dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(shoe.pop())
        if len(shoe) < 10:
            shoe = create_shoe()
        dealer_total = sum(dealer_hand)
        while player_total > 21 and 11 in player_hand:
            player_total -= 10
        while dealer_total > 21 and 11 in dealer_hand:
            dealer_total -= 10
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

    print("\nWelcome to the Slot Machine!V5.0")
    print(f"Your current balance: {balance} coins")

    bet = int(input("Enter your bet amount: "))
    if bet > balance or bet <= 0:
        print("Invalid bet amount. Loans haven't been invented yet, so you can't bet more than you have.")
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

    winnings = evaluate_spin(top, middle, bottom, bet)
    if winnings > 0:
        print(f"You win {winnings} coins!")
        balance += winnings
    else:
        print(f"You lose {bet} coins.")
        balance -= bet

    return balance

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
    elif middle[0] == middle[1] == middle[2]:
        winnings += bet * 2
        print("Middle row three of a kind!")
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
        "Straight": 3,
        "Three of a kind": 2,
        "Two pairs": 1.1,
        "One pair": 0,
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
        print("Invalid bet amount. Loans haven't been invented yet, so you can't bet more than you have.")
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

def play_roulette(balance):
    print("\nWelcome to Roulette!V3.3")
    print(f"Your current balance: {balance} coins")

    bet = int(input("Bet amount: "))
    if bet <= 0 or bet > balance:
        print("Invalid bet. Loans haven't been invented yet, so you can't bet more than you have.")
        return balance

    choice = input("Choose your bet (0-36, red, black, even, odd): ").lower()

    
    winning_number = random.randint(0, 36)

    
    red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

    if winning_number == 0:
        color = "green"
    elif winning_number in red_numbers:
        color = "red"
    else:
        color = "black"

    odd_even = "even" if winning_number % 2 == 0 and winning_number != 0 else "odd"

    print(f"The winning number is {winning_number} ({color}, {odd_even}).")

   
    if choice.isdigit():
        if int(choice) == winning_number:
            print("You won! 35 to 1 payout!")
            balance += bet * 35
        else:
            print("You lost.")
            balance -= bet
        return balance

    if choice == "red" and color == "red":
        print("You won!")
        balance += bet
    elif choice == "black" and color == "black":
        print("You won!")
        balance += bet
    elif choice == "even" and odd_even == "even":
        print("You won!")
        balance += bet
    elif choice == "odd" and odd_even == "odd":
        print("You won!")
        balance += bet
    else:
        print("You lost!")
        balance -= bet

    return balance

def play_horse_racing(balance):
    horses = ["Yellow", "Red", "Green", "Blue", "Purple"]
    print ("Welcome to Horse Racing! V1.0")
    print(f"Your current balance: {balance} coins")
    bet = int(input("Bet amount: "))
    if bet <= 0 or bet > balance:
        print("Invalid bet. Loans haven't been invented yet, so you can't bet more than you have.")
        return balance
    print("Horses:", ", ".join(horses))
    choice = input("Choose a horse to bet on: ").capitalize()
    if choice not in horses:
        print("Invalid horse choice.")
        return balance
    winning_horse = random.choice(horses)
    print(f"Winning Horse is {winning_horse}!")
    if choice == winning_horse:
            print("You won the very fair and special horse race! x4 payout!")
            balance += bet * 4
    else:
            print("You lost to a RANDOMLY SELECTED HORSE! How could you lose to a random selection? You should be ashamed of yourself.")
            balance -= bet
    return balance

def main():
    balance = 20
    print("Welcome to The Gambling House 4.0")

    while True:
        print("\n====== MAIN MENU ======")
        print("1. Play Slot Machine")
        print("2. Play number gamble")
        print("3. Play Blackjack")
        print("4. Play Poker Dice")
        print("5. Play Roulette")
        print("6. Play Horse Racing")
        print("7. Check Balance")
        print("8. Quit")
        print("=========================")
        print("This is a project in work with no visuals whatsoever, so I hope you have a vivid imagination! :)")


        choice = input("Choose an option (1-8): ")

        if choice == "1":
            balance = play_slot_machine(balance)
        elif choice == "7":
            print(f"Your current balance: {balance} coins")
        elif choice == "3":
            balance = play_blackjack(balance)
        elif choice == "2":
            balance = play_number_gamble(balance)
        elif choice == "4":
            balance = play_poker_dice(balance)
        elif choice == "5":
            balance = play_roulette(balance)
        elif choice == "8":
            print("Thanks for playing!:)")
            break
        elif choice == "6":
            balance = play_horse_racing(balance)
        else:
            print("Invalid choice. Try again.")

        if balance <= 0:
            print("You're out of coins! How irresponsible, how will you pay the taxes? Game over.")
            break

main()
