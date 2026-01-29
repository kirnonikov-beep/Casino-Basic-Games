#Old split logic. here for any people who may need it
elif move == "p":
            if player_hand[0] == player_hand[1] and bet <= balance:
                bet *= 2
                second_hand = [player_hand.pop(), shoe.pop()]
                player_hand.append(shoe.pop())
                if len(shoe) < 10:
                    shoe = create_shoe()
                print(f"First hand: {player_hand}, total = {sum(player_hand)}")
                print(f"Second hand: {second_hand}, total = {sum(second_hand)}")
                while sum(player_hand) < 21:
                    move1 = input("First hand - (h)it or (s)tand: ").lower()
                    if move1 == "h":
                        player_hand.append(shoe.pop())
                        if len(shoe) < 10:
                            shoe = create_shoe()
                        print(f"First hand: {player_hand}, total = {sum(player_hand)}")
                    elif move1 == "s":
                        break
                while sum(second_hand) < 21:
                    move2 = input("Second hand - (h)it or (s)tand: ").lower()
                    if move2 == "h":
                        second_hand.append(shoe.pop())
                        if len(shoe) < 10:
                            shoe = create_shoe()
                        print(f"Second hand: {second_hand}, total = {sum(second_hand)}")
                    elif move2 == "s":
                        break
                player_total = sum(player_hand)
                second_total = sum(second_hand)
                dealer_total = sum(dealer_hand)
                while dealer_total < 17:
                    dealer_hand.append(shoe.pop())
                    if len(shoe) < 10:
                        shoe = create_shoe()
                    dealer_total = sum(dealer_hand)
                while player_total > 21 and 11 in player_hand:
                    player_total -= 10
                while second_total > 21 and 11 in second_hand:
                    second_total -= 10
                while dealer_total > 21 and 11 in dealer_hand:
                    dealer_total -= 10
                print(f"Dealer's cards: {dealer_hand}, total = {dealer_total}")

                for idx, total in enumerate([player_total, second_total], start=1):
                    if total > 21:
                        print(f"Hand {idx} busted! Dealer wins.")
                        balance -= bet // 2
                    elif dealer_total > 21 or total > dealer_total:
                        print(f"Hand {idx} wins!")
                        balance += bet // 2
                    elif total == dealer_total:
                        print(f"Hand {idx} ties!")
                    else:
                        print(f"Hand {idx} loses.")
                        balance -= bet #fix entire split logic. appears to be wrong