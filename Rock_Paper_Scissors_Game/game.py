class Game:
    def __init__(self, id):
        self.player_1_Went = False
        self.player_2_Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, player):
        """
        Get the move of a specific player.
        Args:
            player (int): The player number (0 or 1).
        Returns:
            The move of the specified player.
        """
        return self.moves[player]

    def play(self, player, move):
        """
        Record a player's move.
        Args:
            player (int): The player number (0 or 1).
            move (str): The move played by the player ('R', 'P', or 'S').
        """
        self.moves[player] = move
        if player == 0:
            self.player_1_Went = True
        else:
            self.player_2_Went = True

    def connected(self):
        """
        Check if both players are connected and ready to play.
        Returns:
            True if both players are connected and ready, False otherwise.
        """
        return self.ready

    def bothWent(self):
        """
        Check if both players have made their moves.
        Returns:
            True if both players have made their moves, False otherwise.
        """
        return self.player_1_Went and self.player_2_Went
    
    def winner(self):
        """
        Determine the winner of the game based on the moves of the players.
        Returns:
            -1: If the game is a tie.
            0: If player 1 wins.
            1: If player 2 wins.
        """
        player_1 = self.moves[0].upper()[0] 
        player_2 = self.moves[1].upper()[0]

        winner = -1
        if player_1 == "R" and player_2 == "S":
            winner = 0 
        elif player_1 == "S" and player_2 == "R":
            winner = 1  
        elif player_1 == "P" and player_2 == "R":
            winner = 0
        elif player_1 == "R" and player_2 == "P":
            winner = 1
        elif player_1 == "S" and player_2 == "P":
            winner = 0
        elif player_1 == "P" and player_2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        """
        Reset the flags indicating whether players have made their moves.
        """
        self.player_1_Went = False
        self.player_2_Went = False
