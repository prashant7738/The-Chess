import pygame

pygame.init()
WIDTH, HEIGHT = 1000, 800  
SQUARE_SIZE = 100 
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('THE CHESSSSSS !!!!!!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

# Colors
LIGHT_COLOR = (211, 211, 211)  
DARK_COLOR = (105, 105, 105)   
HIGHLIGHT_COLOR = (255, 0, 0)

# Game variables
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook'] + ['pawn']*8
white_locations = [(i, j) for j in range(2) for i in range(8)]
black_pieces = white_pieces.copy()
black_locations = [(i, 7-j) for j in range(2) for i in range(8)]
turn_step, selection, valid_moves = 0, 100, []
counter, winner, game_over = 0, '', False

# Load images
pieces = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
white_images = [pygame.transform.scale(pygame.image.load(f'assets/images/white {piece}.png'), (70, 70)) for piece in pieces]
black_images = [pygame.transform.scale(pygame.image.load(f'assets/images/black {piece}.png'), (70, 70)) for piece in pieces]

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # Status Bar
    font = pygame.font.Font(None, 40)
    status_text = ["White's Turn", "Black's Turn"]
    text_surface = font.render(status_text[turn_step % 2], True, (0, 0, 0))
    screen.blit(text_surface, (820, 750)) 
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
        pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)

def draw_pieces():
    for i, (piece, (x, y)) in enumerate(zip(white_pieces, white_locations)):
        index = pieces.index(piece)
        screen.blit(white_images[index], (x * 100 + 10, y * 100 + 10))
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', [x * 100 + 1, y * 100 + 1, 100, 100], 2)
    for i, (piece, (x, y)) in enumerate(zip(black_pieces, black_locations)):
        index = pieces.index(piece)
        screen.blit(black_images[index], (x * 100 + 10, y * 100 + 10))
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', [x * 100 + 1, y * 100 + 1, 100, 100], 2)

def check_options(pieces, locations, turn):
    moves_list = []
    for i, (piece, (x, y)) in enumerate(zip(pieces, locations)):
        if piece == 'pawn': moves_list.append(check_pawn((x, y), turn))
        elif piece == 'rook': moves_list.append(check_rook((x, y), turn))
        elif piece == 'knight': moves_list.append(check_knight((x, y), turn))
        elif piece == 'bishop': moves_list.append(check_bishop((x, y), turn))
        elif piece == 'queen': moves_list.append(check_queen((x, y), turn))
        elif piece == 'king': moves_list.append(check_king((x, y), turn))
    return moves_list

def check_king(position, color):
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    return [(position[0] + x, position[1] + y) for x, y in targets if 0 <= position[0] + x <= 7 and 0 <= position[1] + y <= 7]

def check_queen(position, color):
    return check_bishop(position, color) + check_rook(position, color)

def check_bishop(position, color):
    moves_list = []
    directions = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
    for dx, dy in directions:
        x, y = position[0] + dx, position[1] + dy
        while 0 <= x <= 7 and 0 <= y <= 7:
            moves_list.append((x, y))
            if (x, y) in (black_locations if color == 'white' else white_locations): break
            x, y = x + dx, y + dy
    return moves_list

def check_rook(position, color):
    moves_list = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in directions:
        x, y = position[0] + dx, position[1] + dy
        while 0 <= x <= 7 and 0 <= y <= 7:
            moves_list.append((x, y))
            if (x, y) in (black_locations if color == 'white' else white_locations): break
            x, y = x + dx, y + dy
    return moves_list

def check_pawn(position, color):
    moves_list = []
    dy = 1 if color == 'white' else -1
    if (position[0], position[1] + dy) not in white_locations + black_locations:
        moves_list.append((position[0], position[1] + dy))
        if (position[1] == 1 if color == 'white' else position[1] == 6) and (position[0], position[1] + 2*dy) not in white_locations + black_locations:
            moves_list.append((position[0], position[1] + 2*dy))
    for dx in [-1, 1]:
        if (position[0] + dx, position[1] + dy) in (black_locations if color == 'white' else white_locations):
            moves_list.append((position[0] + dx, position[1] + dy))
    return moves_list

def check_knight(position, color):
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    return [(position[0] + x, position[1] + y) for x, y in targets if 0 <= position[0] + x <= 7 and 0 <= position[1] + y <= 7]

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    return options_list[selection]

def draw_valid(moves):
    color = 'red' if turn_step < 2 else 'blue'
    for x, y in moves:
        pygame.draw.circle(screen, color, (x * 100 + 50, y * 100 + 50), 5)

def draw_check():
    try:
        if turn_step < 2:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            if any(king_location in moves for moves in black_options):
                pygame.draw.rect(screen, 'dark red', [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)
        else:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            if any(king_location in moves for moves in white_options):
                pygame.draw.rect(screen, 'dark blue', [king_location[0] * 100 + 1, king_location[1] * 100 + 1, 100, 100], 5)
    except ValueError:
        pass 

def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game of chess Suiiiii!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    counter = (counter + 1) % 30
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x, y = event.pos[0] // 100, event.pos[1] // 100
            click_coords = (x, y)
            if click_coords == (8, 8) or click_coords == (9, 8):
                winner = 'black' if turn_step <= 1 else 'white'
            elif turn_step <= 1 and click_coords in white_locations:
                selection = white_locations.index(click_coords)
                turn_step = 1
            elif turn_step > 1 and click_coords in black_locations:
                selection = black_locations.index(click_coords)
                turn_step = 3
            elif click_coords in valid_moves and selection != 100:
                if turn_step <= 1:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        if black_pieces[black_locations.index(click_coords)] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_locations.index(click_coords))
                        black_locations.pop(black_locations.index(click_coords))
                    turn_step = 2
                else:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        if white_pieces[white_locations.index(click_coords)] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_locations.index(click_coords))
                        white_locations.pop(white_locations.index(click_coords))
                    turn_step = 0
                selection, valid_moves = 100, []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_RETURN:
            game_over, winner = False, ''
            white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook'] + ['pawn']*8
            white_locations = [(i, j) for j in range(2) for i in range(8)]
            black_pieces = white_pieces.copy()
            black_locations = [(i, 7-j) for j in range(2) for i in range(8)]
            turn_step, selection, valid_moves = 0, 100, []
            black_options = check_options(black_pieces, black_locations, 'black')
            white_options = check_options(white_pieces, white_locations, 'white')

    if winner:
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame