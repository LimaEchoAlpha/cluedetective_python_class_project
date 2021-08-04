
from sys import exit
from printouts import *
from errors import *
from board import *
from detective import *


class Engine():
    """This class moves the clue detective program from one state to another.
       
       Attributes:
       - board = current instance of the Board class 
       - notebook = current instance of the Notebook class 
       - detective = current instance of the Detective class
       
       Functions:
       - setup(): Sets up the particular instance of Board, Notebook, and Detective classes. 
       - take_turn(): Takes the player whose turn it is as an argument.  
                      Manages all that needs to happen during a turn: 
                      creates a current instance of Turn, 
                      calls turn_input function, 
                      passes current turn information to the detective, 
                      calls deductions function and prints out current notes, 
                      and determines whose turn is next.
       - turn_input(): Takes the player whose turn it is and an instance of Turn as an argument.  
                       Prompts user to input information about the turn: what suspect, room, 
                       and weapon was suggested, who disproved it (if any), what card was revealed (if any).  
                       Stores information in the current turn.
       - deductions(): Checks what is stored in the solution.  
                       If no solution or partial solution, go back to taking turns.  
                       If full solution is found, print and exit the program.
    """

    def __init__(self, board=None, notebook=None, detective=None):
        self.board = board
        self.notebook = notebook
        self.detective = detective
        self.setup()
    
    
    def setup(self):
        welcome()
        instructions()
        print()
        print("Let's start by setting up your board!")
        print()
        
        q1 = "Which suspect are you? "
        q2 = "\nPress ENTER to accept or type N to re-do: "
        
        # prompt user to enter their name
        while not is_valid_player(me_input := input(q1)):
            print("Please enter a valid Suspect.")     
        me_decoded = Board.identify(me_input)
        print(f"Hello, {me_decoded.name}!")
        print()
        
        # prompt user to enter the players in their turn order
        print("Enter ALL the players one by one in the order of their turn.")
        print("When you are done, enter #")
        accept = 'N'
        while accept == 'N':
            players_decoded, suspects_decoded = collect_players_and_suspects_list()
            if len(players_decoded) == 1:
                print("Not enough players. Try again.")
                continue
            elif len(players_decoded) > 6:
                print("Too many players. Try again.")
                continue            
            print("The players in order are:", end=" ")
            for player in players_decoded:
                print(player, end="  ")
            accept = input(q2).upper()
            if accept == 'Q':
                exit("\nExiting program. Thanks for using Clue Detective!\n")
        print()
                
        # prompt user to enter other suspects that aren't players
        # if number of players is not 6
        number = 6 - len(players_decoded)
        if number > 0:
            print("Enter the rest of the suspects that are not players")
            print("When you are done, enter #")
            accept = 'N'
            more_suspects = []
            while accept == 'N':
                more_suspects = collect_cards()
                if len(more_suspects) != number:
                    print(f"You need to enter {number} suspects. Try again.")
                    continue          
                print("The players in order are:", end=" ")
                for suspect in more_suspects:
                     print(suspect, end="  ")
                accept = input(q2).upper()
                if accept == 'Q':
                    exit("\nExiting program. Thanks for using Clue Detective!\n")
        
            # add suspects that aren't players to suspects list
            for suspect in more_suspects:
                suspects_decoded.append(suspect)
        
        # create an instance of Board
        b = Board(me_decoded, players_decoded, suspects_decoded)
        self.board = b
        print()
        
        # figure out the number of cards each player has
        if len(players_decoded) == 4 or len(players_decoded) == 5:
            print("Enter the two players with less cards one by one.")
            print("When you are done, enter #")
            accept2 = 'N'
            while accept2 == 'N':
                different_decoded = collect_players_list()
                if len(different_decoded) != 2:
                    print("Please enter two valid players.")
                    continue           
                print("The two players are:", end=" ")
                for player in different_decoded:
                    print(player.name, end="  ")
                accept2 = input(q2).upper()
                if accept2 == 'Q':
                    exit("\nExiting program. Thanks for using Clue Detective!\n")
            b.num_card_calc(different_decoded)
            print()
        else:
            b.num_card_calc()
        
        # prompt user to enter the cards in their hand
        print("Enter all the cards in your hand one by one.")
        print("When you are done, enter #")
        accept3 = 'N'
        while accept3 == 'N':
            hand_decoded = collect_cards()
            if len(hand_decoded) != self.board.me.num_cards:
                print(f"You need to enter {self.board.me.num_cards} cards. Try again.")
                continue           
            print("Your hand is:", end=" ")
            for card in hand_decoded:
                print(card, end="  ")
            accept3 = input(q2).upper()
            if accept3 == 'Q':
                exit("\nExiting program. Thanks for using Clue Detective!\n")
        b.me.hand = hand_decoded
        print()
        
        # create an instance of Notebook and Detective
        n = Notebook(self.board)
        self.notebook = n
        d = Detective(self.board, self.notebook)
        self.detective = d
        
        print("Your board is now set up!  We're ready to play Clue!")
        print()
        self.notebook.printout()
        
        self.take_turn(players_decoded[0])
        
     
    def take_turn(self, player):
                
        current_turn = self.board.log_turn(player)
        i = self.board.history.index(current_turn)
        print()
        print("~"*22+f" START TURN #{i+1:<2d} " +"~"*21)
        print()
        
        # use turn_input function to prompt user for turn information
        self.turn_input(player, current_turn)
        
        print()
        print("~"*23+f" END TURN #{i+1:<2d} "+"~"*22)
        print()
        
        self.detective.take_notes(current_turn)
        self.deductions()
        
        next_player = self.board.next_player(player)
        self.take_turn(next_player)

   
    def turn_input(self, player, turn):
        if player == self.board.me:
            print("It's YOUR turn!")
        else:
            print(f"It is {player}'s turn.")
        print()
        
        q1 = "Which ROOM did {} enter? \nTo skip this turn, type X: ".format(player)
        q2 = "Which SUSPECT did {} guess? ".format(player)
        q3 = "Which WEAPON did {} guess? ".format(player)
        q4 = "Which player disproved the suggestion? \nIf no one disproved it, type X: "
        q5 = "What card was revealed? "
        q6 = "Press ENTER to accept or type N to re-do: "
        
        # prompt user to input all the information for the turn
        # handles typos and allows user to review entry
        # allows user to quit at any time
        accept = 'N'
        while accept == 'N':
            
            # prompt user to enter room or skip the turn
            while not is_valid(room_input := input(q1), 'Room', skip=True):
                print("Please enter a valid Room.")
            if room_input.upper() == 'X':
                print()
                print("~"*25+" END TURN "+"~"*25)
                next_player = self.board.next_player(player)
                self.take_turn(next_player)
            room_decoded = Board.translate(room_input)
            print()
        
            # prompt user to enter suspect
            while not is_valid(suspect_input := input(q2), 'Suspect'):
                print("Please enter a valid Suspect.")
            suspect_decoded = Board.translate(suspect_input)
            print()
        
            # prompt user to enter weapon
            while not is_valid(weapon_input := input(q3), 'Weapon'):
                print("Please enter a valid Weapon.")
            weapon_decoded = Board.translate(weapon_input)
            print()
            
            # store suggestion in current turn
            suggestion = (suspect_decoded, weapon_decoded, room_decoded)
            turn.suggestion = suggestion
        
            # prompt user to enter disprover, if any
            while not is_valid(disprover_input := input(q4), 'Suspect', skip=True):
                print("Please enter a valid Suspect.")
            if disprover_input.upper() != 'X':
                disprover_decoded = Board.translate(disprover_input)
                turn.disprover = disprover_decoded
            print()
        
            # prompt user to enter revealed card, if any
            if player == self.board.me and disprover_input != 'X':
                while not is_valid(revealed_input := input(q5)):
                    print("Please enter a valid card.")
                revealed_decoded = Board.translate(revealed_input)
                turn.revealed = revealed_decoded
                print()
                
            # print confirmation of entry for user to review
            if player == self.board.me:
                print(f"You suggested {suspect_decoded} with the {weapon_decoded} in the {room_decoded}.")
                if disprover_input.upper() == 'X':
                    print("No player disproved.")
                else:
                    print(f"{disprover_decoded} disproved and revealed {revealed_decoded}.")
            else:
                print(f"{player} suggested {suspect_decoded} with the {weapon_decoded} in the {room_decoded}.")
                if disprover_input.upper() == 'X':
                    print("No player disproved.")
                else:
                    print(f"{disprover_decoded} disproved.")
            
            # allows user to accept or reject entry and try again
            accept = input(q6).upper()
            print()
            if accept == 'Q':
                exit("\nExiting program. Thanks for using Clue Detective!\n")
 

    def deductions(self):
        print()
        print("*"*24+" DEDUCTIONS "+"*"*24)
        print()
        notes_legend()
        print()
              
        if self.board.solution.is_solved():
            suspect = self.board.solution.suspect
            weapon = self.board.solution.weapon
            room = self.board.solution.room
            solution_banner(suspect, weapon, room)
            print()
            exit("Exiting program. Thanks for using Clue Detective!\n")
        
        elif self.board.solution.not_solved():
            print("No solutions found yet.")
            print()
            self.notebook.printout()
        
        elif self.board.solution.partially_solved():
            print("Partial solution found.")
            if self.board.solution.suspect:
                print("SUSPECT = ", self.board.solution.suspect)
            if self.board.solution.weapon:
                print("WEAPON = ", self.board.solution.weapon)
            if self.board.solution.room:
                print("ROOM = ", self.board.solution.room)
            print()
            self.notebook.printout()

if __name__ == "__main__":
    start = Engine()
