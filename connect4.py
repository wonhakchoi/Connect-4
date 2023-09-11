import numpy as np
import pygame
import sys
import math

#  testing testing

ROWS = 6
COLUMNS = 7
CONNECT = 4

BLUE = (62, 103, 206)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (24, 25, 26)




def initialize_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    # ok to drop the piece; last 
    return board[ROWS - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))

def win_game(board, piece):

    # check horizontal locations for win
    for c in range(COLUMNS - (CONNECT - 1)):
        for r in range(ROWS):
            count_to_win = 0
            for connect in range (CONNECT + 1):
                if board[r][c + connect] != piece:
                    break
                else:
                    count_to_win += 1

                if (count_to_win == CONNECT):
                    return True
                    

    # check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS  - (CONNECT - 1)):
            count_to_win = 0
            for connect in range (CONNECT + 1):
                if board[r + connect][c] != piece:
                    break
                else:
                    count_to_win += 1
                if (count_to_win == CONNECT):
                    return True

    # check positive slope diagonals
    for c in range(COLUMNS - (CONNECT - 1)):
        for r in range(ROWS  - (CONNECT - 1)):
            count_to_win = 0
            for connect in range (CONNECT + 1):
                if board[r + connect][c + connect] != piece:
                    break
                elif board[r + connect][c + connect] == piece:
                    count_to_win += 1
                if (count_to_win == CONNECT):
                    return True


    # check negative slope diagonals
    for c in range(COLUMNS - (CONNECT - 1)):
        for r in range(CONNECT - 1, ROWS):
            count_to_win = 0
            for connect in range (CONNECT + 1):
                if board[r - connect][c + connect] != piece:
                    break
                elif board[r - connect][c + connect] == piece:
                    count_to_win += 1

                if (count_to_win == CONNECT):
                    return True

# GUI
def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()

# initialize 
board = initialize_board()
print(board)

game_over = False
turn = 0

# pygame
pygame.init()

SQUARE_SIZE = 100
width = COLUMNS * SQUARE_SIZE
height = (ROWS + 1) * SQUARE_SIZE # +1 for area where it gets dropped
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)

draw_board(board)
pygame.display.update() # ensures we see what we drew

myFont = pygame.font.SysFont("verdana", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE)) # covers it to be black each loop
            posX = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posX, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posX, int(SQUARE_SIZE/2)), RADIUS)

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE)) 
            # print(event.pos)

            # # Ask for player 1 input;
            if turn == 0:
                posX = event.pos[0] # this number is between 0 and 700
                col = int(math.floor(posX/SQUARE_SIZE))
                # col = int(input("Player 1, make your selection (0-6): "))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if win_game(board, 1):
                        # print("player 1 wins!")
                        label = myFont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))

                        game_over = True


            # Ask for player 2 input
            else:
                posX = event.pos[0] 
                col = int(math.floor(posX/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if win_game(board, 2):
                        # print("player 2 wins!")
                        label = myFont.render("Player 2 wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True 



            # UI ONLY
            # else:
            #     col = int(input("Player 2, make your selection (0-6): "))

            #     if is_valid_location(board, col):
            #         row = get_next_open_row(board, col)
            #         drop_piece(board, row, col, 2)

            #         if win_game(board, 2):
            #             print("player 2 wins!")
            #             game_over = True 

            draw_board(board)

            turn += 1
            turn = turn % 2 # alternate between 0 and 1

            if game_over:
                pygame.time.wait(5000)
