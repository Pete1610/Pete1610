# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Step 1: Create a Piece class for the checker pieces (either black or white)
class Piece:
    def __init__(self, color, is_king=False):  # Make a piece with color and king status
        self.color = color  # Save color of the piece ('black' or 'white')
        self.is_king = is_king  # Save if the piece is a king

    def promote(self):  # Promote a piece to a king
        self.is_king = True  # Change piece to a king

    def __repr__(self):  # Show piece on the board
        # 'k' for black king, 'K' for white king, 'X' for black, 'O' for white
        if self.is_king:
            return "k" if self.color == "black" else "K"
        else:
            return "X" if self.color == "black" else "O"
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Step 2: Create the CheckersBoard class to manage the board and game rules
class CheckersBoard:
    def __init__(self):
        self.board = self.initialize_board()  # Set up the board
        self.turn = "white"  # White moves first

    def initialize_board(self):
        # Step 3: Place the pieces at the start
        board = [[None] * 8 for _ in range(8)]  # Make empty 8x8 board

        # Place black pieces on rows 0, 1, 2
        for row in range(3):
            for col in range(row % 2, 8, 2):  # Black on every other space
                board[row][col] = Piece("black")

        # Place white pieces on rows 5, 6, 7
        for row in range(5, 8):
            for col in range(row % 2, 8, 2):  # White on every other space
                board[row][col] = Piece("white")

        return board  # Return board with pieces

    def print_board(self):
        # Step 4: Show the board
        print("  +" + "---+" * 8)  # Top border
        for i, row in enumerate(self.board):
            row_label = 8 - i  # Row number for display
            row_pieces = [str(piece) if piece else " " for piece in row]  # Show pieces
            print(f"{row_label} | " + " | ".join(row_pieces) + " |")  # Print row
            print("  +" + "---+" * 8)  # Row border
        print("    a   b   c   d   e   f   g   h")  # Column labels

    def is_valid_move(self, start, end):
        # Step 5: Check if the move is allowed
        x1, y1 = start  # Starting position
        x2, y2 = end  # Ending position
        piece = self.board[x1][y1]  # Get piece at start position

        if not piece:  # No piece to move
            print(f"No piece at {chr(y1 + ord('a'))}{8 - x1}.")
            return False
        if piece.color != self.turn:  # Wrong player's turn
            print(f"It's {self.turn}'s turn!")
            return False
        if abs(x2 - x1) != abs(y2 - y1):  # Must move diagonally
            print("Move must be diagonal.")
            return False
        if abs(x2 - x1) > 2:  # Can move only 1 or 2 spaces
            print("Move can only be 1 or 2 squares.")
            return False
        if abs(x2 - x1) == 1 and self.board[x2][y2] is not None:  # End space must be empty
            print(f"Destination {chr(y2 + ord('a'))}{8 - x2} is not empty.")
            return False
        if abs(x2 - x1) == 2:  # For a jump (2 squares)
            mid_x = (x1 + x2) // 2  # Middle row
            mid_y = (y1 + y2) // 2  # Middle column
            opponent = "white" if piece.color == "black" else "black"  # Opponent color
            if self.board[mid_x][mid_y] is None or self.board[mid_x][mid_y].color != opponent:
                print("No opponent's piece to jump over.")
                return False
            self.board[mid_x][mid_y] = None  # Remove opponent's piece after jump
        return True  # Valid move

    def move_piece(self, start, end):
        # Step 6: Move piece if move is allowed
        x1, y1 = start  # Start position
        x2, y2 = end  # End position
        piece = self.board[x1][y1]  # Get piece at start position

        if self.is_valid_move(start, end):  # If move is valid
            self.board[x2][y2] = piece  # Move piece to end position
            self.board[x1][y1] = None  # Clear start position

            # Make piece a king if it reaches the last row
            if piece.color == "white" and x2 == 0:  # White at top row
                piece.promote()  # Promote to king
            elif piece.color == "black" and x2 == 7:  # Black at bottom row
                piece.promote()  # Promote to king

            # Switch turns
            self.turn = "black" if self.turn == "white" else "white"  # Change turn
        else:
            print("Invalid move, try again.")  # Show error if move not valid

    def check_winner(self):
        # Step 7: Check if a player has won
        white_pieces = black_pieces = 0  # Count pieces
        for row in self.board:
            for piece in row:
                if piece:
                    if piece.color == "white":
                        white_pieces += 1  # Count white
                    elif piece.color == "black":
                        black_pieces += 1  # Count black
        if white_pieces == 0:  # No white pieces
            return "Black wins!"
        elif black_pieces == 0:  # No black pieces
            return "White wins!"
        return None  # No winner yet
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Step 8: Main function to run the game
def main():
    board = CheckersBoard()  # Set up a new game

    while True:
        board.print_board()  # Show the board each turn

        winner = board.check_winner()  # Check for a winner
        if winner:  # If winner found
            print(winner)  # Show who won
            break  # End game

        # Get the player's move
        move = input(f"{board.turn}'s move (e.g., 'a3 b4') or 'stop' to quit: ").strip().lower()
        if move == "stop":  # Stop game
            break
        elif move == "reset":  # Reset game
            board = CheckersBoard()  # New game
        else:
            try:
                # Parse move from input
                start_pos, end_pos = move.split()
                x1, y1 = 8 - int(start_pos[1]), ord(start_pos[0]) - ord('a')
                x2, y2 = 8 - int(end_pos[1]), ord(end_pos[0]) - ord('a')
                board.move_piece((x1, y1), (x2, y2))  # Try to move piece
            except (ValueError, IndexError):  # If move format is wrong
                print("Invalid move format. Please try again.")
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Step 9: Start the game
if __name__ == "__main__":
    main()  # Start game
