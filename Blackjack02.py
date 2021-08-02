# A basic text based blackjack game against a computer dealer

# *It's a little hard to follow all of the text ingame, therefore there are times when you need to press enter to continue the game
# if you want to disable them put a '#' symbol before lines 24, 88, 167 (Another way to make it easier can be to use python's time library and have the program sleep occasionally)*
import random

class Player:
    def __init__(self, name, money):
        self.my_name = name
        self.my_hand = list()
        self.my_money = money
        self.my_status = "Taking_turn"

    # pick a certain amount of cards from the deck to a hand
    
    def pick_cards(self, deck, cards_to_pick):
        i = 0
        while i < cards_to_pick:
            new_card = random.choice(deck)
            self.my_hand.append(new_card)
            print(new_card, "was drawn")

            # unnecessary input - check line 87
            input("->")

            deck.remove(new_card)
            i += 1
        print("")  

    # set an amount to bet
    
    def make_bet(self, amount):
        self.my_bet = amount

# create a list of the cards in a standard 52 card deck without jokers (royals are represented by their value which in poker is 10) and suit doesnt matter

def make_deck():
    deck = list()
    card = 1
    iterater = 1
    while iterater <= 52:
        if iterater > 1 and iterater % 4 == 1:
            card += 1
        if card > 10:
            deck.append(10)
        else:
            deck.append(card)
        iterater+=1

    return deck

# The player can hit(draw another card) or stand (end your turn). As of now no side rules are implemented

def player_turn_action(player, deck):
    print(player.my_name, "currently has these cards:", player.my_hand, "for a sum of", + sum(player.my_hand))
    player_action = input(f"Would {player.my_name} like to (h)it or (s)tand? ")
    if player_action == "h":
        print(player.my_name, "hit!")
        player.pick_cards(deck, 1)
        print(f"{player.my_name}'s hand now equals: {sum(player.my_hand)}")
    elif player_action == "s":
        print(player.my_name, "Stood!\n")
        player.my_status = 'Stood'
    else:
        print("couldn't recognize command please enter 'h' or 's'.")

# Will run for each player letting them take action and checking if they bust or blackjack
 
def player_turn(player, deck):
    while player.my_status == 'Taking_turn':
        player_turn_action(player, deck)

        # Check if player got blackjack or busted
        if sum(player.my_hand) == 21:
            player.my_status = "Done"
            print(f"{player.my_name} got blackjack!\n")
        if sum(player.my_hand) > 21:
            player.my_status = "Done"
            print(f"{player.my_name} busted. Better luck next time.\n")

# Where the code actually starts running

def main():
    print("Welcome to BlackJack - a classic casino game!")
    print("The rules will follow the normal rules of blackjack which can be found at 'https://www.officialgamerules.org/blackjack' \n(note: this game uses a standard 52 card deck without jokers)")
    
    # These inputs are just used to pause the program for ease and can be deleted or commented out if you want!
    input("\nWhen you see this symbol '->' press enter to continue. \n->")

    # create the deck and the Players and Dealer objects

    new_deck = make_deck()
    players = list()
    dealer = Player("Dealer", None)

    while True:
        num_players = input("How many will be playing today?! ")
        if num_players.isdigit():
            if int(num_players) > 4:
                print("Cannot play with more then 4 players.")
            else:
                break
        else:
            print("Must enter a valid number!")

    for i in range(int(num_players)):
        player_name = input("Enter next player's name: ")
        players.append(Player(player_name, 1500))

    # Give every player two cards and make them place a bet

    print("")
    for player in players:
        while True:
            bet_amount = input(f"How much will {player.my_name} bet? ")
            if bet_amount.isdigit():
                if int(bet_amount) > player.my_money:
                    print(f"Can't bet more then you have. Current funds: {player.my_money}")
                else:
                    player.make_bet(int(bet_amount))
                    break
            else:
                print("Please enter a valid betting number (No Decimals). ")

        print(player.my_name, "will be dealt two cards")
        player.pick_cards(new_deck, 2)
        print(player.my_name, "has these cards:", player.my_hand, "for a sum of", sum(player.my_hand))
        print("")


    print("\nNow the dealer will be dealt one card face up and one face down")
    dealer.pick_cards(new_deck, 1)

    # Have each player take their turn hitting or standing

    for player in players:
        player_turn(player, new_deck)


    # After everyone takes their turns, the dealer will take their turn (the entire turn is determined by the rules of blackjack so their are no choices)

    print("\n\nThe dealer will now flip over their hidden card")
    dealer.pick_cards(new_deck, 1)
    print("the dealer now has a total of", sum(dealer.my_hand))
            
    # According to the rules while the dealer has less then 17 if he hasn't won then he must draw

    while sum(dealer.my_hand) < 17:
        print("Since the dealer has a hand lower then 17 they must hit. ")
        dealer.pick_cards(new_deck, 1)

        # Check for a bust    (Does anybody read these comments?)

        if sum(dealer.my_hand) > 21:
            dealer.my_status = "Bust"
            print("The dealer has busted! ")
            break

    # Determine the outcome based on hand values
    
    for player in players:
        player_sum = sum(player.my_hand)
        dealer_sum = sum(dealer.my_hand)
        print(f"\n ***The results for {player.my_name} are...*** \n")
        
        # Another unecessary input - see line 87
        input("->")

        if player_sum > 21 and dealer_sum > 21:
            print(f"Both {player.my_name} and The Dealer busted therefore the result is a push. Nothing is won or loss.")
        elif player_sum > 21:
            print(f"{player.my_name} busted and lost ${player.my_bet}. Better luck next time!")
        elif player_sum == 21 and dealer_sum != 21:
            print(f"{player.my_name} blackjacked and won ${player.my_bet * 1.5} !!!! Congratulations!!!")
        elif player_sum == 21 and dealer_sum == 21:
            print(f"The dealer and {player.my_name} both hit blackjack, therefore nothing is lost or won.")
        elif dealer_sum == 21:
            print("The dealer had blackjack. Better luck next time!")
            print(f"{player.my_name} lost ${player.my_bet}")
        elif dealer_sum > 21:
            print("The dealer busted. Congratulations!")
            print(f"{player.my_name} won ${player.my_bet}")
        elif dealer_sum > player_sum:
            print("The dealer had a higher value. Better luck next time!")
            print(f"{player.my_name} lost ${player.my_bet}")
        elif dealer_sum == player_sum:
            print(player.my_name, "tied. Nothing will be won or lost.")
        else:
            print(f"{player.my_name}'s hand had a higher value. Congratulations!")
            print(f"{player.my_name} won ${player.my_bet}")


# Time to actually run the game. Unlike in many other languages such as C++ and Java, python doesn't require a main function to run, however 
# it can be considered good practice to do so, in order that other programmers know where to start reading the code.
main()
