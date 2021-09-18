"""" This contains Sudoku UI components. """

from sudoku import Sudoku
from sudokuai import SudokuAI
import pygame
import sys
import datetime
import time
from random import choice, sample


# Meta
ROW_COUNT = 9
COLUMN_COUNT = 9
HOUSE_COUNT = 9

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
LIGHTBLUE = (173, 216, 230)
LIGHTGREEN = (144, 238, 144)
PURPLE = (128, 0, 128)
SPRINGGREEN = (0, 255, 127)
PINK = (255, 192, 203)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
small_font = pygame.font.Font(OPEN_SANS, 20)
medium_font = pygame.font.Font(OPEN_SANS, 26)
large_font = pygame.font.Font(OPEN_SANS, 36)
title_font = pygame.font.Font(OPEN_SANS, 70)

# Load splash image
splash_image = pygame.image.load("assets/images/sudoku_splash.png")
splash_image = pygame.transform.scale(splash_image, (width, height))

# Board
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (2 * BOARD_PADDING)
board_height = height - (2 * BOARD_PADDING)
cell_size = int(min(board_width / COLUMN_COUNT, board_height / ROW_COUNT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Create game and AI agent
game = None
ai = None
solve = None

won = False
highlight = None
current = (0, 0)
valid = None
game_mode = "Easy"

# Time variables
starting_time = None
end_time = None
elapsed_time = None

# Screen variables
splash = True
home = False
instructions = False
mode = False
custom = False


def make_shadow(text, center, color, shadow_color, font, screen):
    """Make shadow effect for a given text."""

    shadow_text = font.render(text, True, shadow_color)
    shadow_text_rect = shadow_text.get_rect()
    shadow_text_rect.center = (center[0] + 1, center[1] + 1)
    screen.blit(shadow_text, shadow_text_rect)

    fore_text = font.render(text, True, color)
    fore_text_rect = fore_text.get_rect()
    fore_text_rect.center = center
    screen.blit(fore_text, fore_text_rect)
    return


while True:
    # Event loop.

    for event in pygame.event.get():

        # Quit event.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Navigation using arrow keys.
        if event.type == pygame.KEYDOWN and not (
            splash or home or instructions or mode
        ):
            key = event.key
            if key == pygame.K_UP:
                for i in range(current[0] - 1, -1, -1):
                    if game.get_cell(i + 1, current[1] + 1).get_color():
                        current = i, current[1]
                        break
            if key == pygame.K_DOWN:
                for i in range(current[0] + 1, 9):
                    if game.get_cell(i + 1, current[1] + 1).get_color():
                        current = i, current[1]
                        break
            if key == pygame.K_LEFT:
                for j in range(current[1] - 1, -1, -1):
                    if game.get_cell(current[0] + 1, j + 1).get_color():
                        current = current[0], j
                        break
            if key == pygame.K_RIGHT:
                for j in range(current[1] + 1, 9):
                    if game.get_cell(current[0] + 1, j + 1).get_color():
                        current = current[0], j
                        break
            i, j = current
            if game.get_cell(i + 1, j + 1).get_color():
                highlight = current

        # Get input.
        if (
            event.type == pygame.KEYDOWN
            and highlight
            and not (splash or home or instructions or mode)
        ):
            i, j = highlight
            key = event.key
            key_dowm = False
            if key == pygame.K_1:
                game.add_value(i + 1, j + 1, 1)
                key_dowm = True
            if key == pygame.K_2:
                game.add_value(i + 1, j + 1, 2)
                key_dowm = True
            if key == pygame.K_3:
                game.add_value(i + 1, j + 1, 3)
                key_dowm = True
            if key == pygame.K_4:
                game.add_value(i + 1, j + 1, 4)
                key_dowm = True
            if key == pygame.K_5:
                game.add_value(i + 1, j + 1, 5)
                key_dowm = True
            if key == pygame.K_6:
                game.add_value(i + 1, j + 1, 6)
                key_dowm = True
            if key == pygame.K_7:
                game.add_value(i + 1, j + 1, 7)
                key_dowm = True
            if key == pygame.K_8:
                game.add_value(i + 1, j + 1, 8)
                key_dowm = True
            if key == pygame.K_9:
                game.add_value(i + 1, j + 1, 9)
                key_dowm = True
            if key == pygame.K_ESCAPE:
                game.delete_value(i + 1, j + 1)
                key_dowm = True
            if key == pygame.K_DELETE:
                game.delete_value(i + 1, j + 1)
                key_dowm = True

            # Starting Time.
            if starting_time is None and key_dowm:
                starting_time = datetime.datetime.now().strftime("%H:%M:%S")
                starting_time = datetime.datetime.strptime(starting_time, "%H:%M:%S")
                end_time = None

    screen.fill(BLACK)

    # Show splash screen.
    if splash:
        screen.blit(splash_image, pygame.Rect(0, 0, width, height))
        pygame.display.flip()
        splash = False
        home = True
        time.sleep(2)
        continue

    # Show home screen.
    if home:

        # Title
        title = title_font.render("Sudoku", True, BLUE)
        title_rect = title.get_rect()
        title_rect.center = (width / 2), 100
        screen.blit(title, title_rect)

        # Sub Title
        sub_title = medium_font.render("Game with Solver", True, LIGHTBLUE)
        sub_title_rect = sub_title.get_rect()
        sub_title_rect.center = (width / 2), 150
        screen.blit(sub_title, sub_title_rect)

        # Play button
        play_button_rect = pygame.Rect((width / 2) - 115, (height / 2) + 30, 230, 40)
        play_button_text = large_font.render("Play Game", True, LIGHTBLUE)
        play_button_text_rect = play_button_text.get_rect()
        play_button_text_rect.center = play_button_rect.center
        screen.blit(play_button_text, play_button_text_rect)

        # Instructions button
        info_button_rect = pygame.Rect((width / 2) - 115, (height / 2) + 100, 230, 40)
        info_button_text = large_font.render("Instructions", True, LIGHTBLUE)
        info_button_text_rect = info_button_text.get_rect()
        info_button_text_rect.center = info_button_rect.center
        screen.blit(info_button_text, info_button_text_rect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse):
                home = False
                mode = True
            if info_button_rect.collidepoint(mouse):
                home = False
                instructions = True
            time.sleep(0.3)
        else:
            mouse = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse):
                make_shadow(
                    "Play Game",
                    play_button_text_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    large_font,
                    screen,
                )
            elif info_button_rect.collidepoint(mouse):
                make_shadow(
                    "Instructions",
                    info_button_text_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    large_font,
                    screen,
                )

        pygame.display.flip()
        continue

    # Show mode screen.
    if mode:

        # Title
        title = large_font.render("Select Mode", True, BLUE)
        title_rect = title.get_rect()
        title_rect.center = (width / 2), 60
        screen.blit(title, title_rect)

        # modes
        y = 80 + 50
        easy = medium_font.render("Easy", True, LIGHTBLUE)
        easy_rect = easy.get_rect()
        easy_rect.center = (width / 2), y + 0 * 50
        screen.blit(easy, easy_rect)

        medium = medium_font.render("Medium", True, LIGHTBLUE)
        medium_rect = medium.get_rect()
        medium_rect.center = (width / 2), y + 1 * 50
        screen.blit(medium, medium_rect)

        hard = medium_font.render("Hard", True, LIGHTBLUE)
        hard_rect = hard.get_rect()
        hard_rect.center = (width / 2), y + 2 * 50
        screen.blit(hard, hard_rect)

        custom_text = medium_font.render("Custom", True, LIGHTBLUE)
        custom_rect = custom_text.get_rect()
        custom_rect.center = (width / 2), y + 3 * 50
        screen.blit(custom_text, custom_rect)

        # back
        back = medium_font.render("Back", True, LIGHTBLUE)
        back_rect = back.get_rect()
        back_rect.center = (width / 2), y + 4 * 50
        screen.blit(back, back_rect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if back_rect.collidepoint(mouse):
                home = True
                mode = False
            if custom_rect.collidepoint(mouse):
                custom = True
                mode = False
                game = Sudoku(mode="custom")
                game_mode = "Custom"
            else:
                if easy_rect.collidepoint(mouse):
                    game = Sudoku(mode="easy")
                    game_mode = "Easy"
                    mode = False
                elif medium_rect.collidepoint(mouse):
                    game = Sudoku(mode="medium")
                    game_mode = "Medium"
                    mode = False
                elif hard_rect.collidepoint(mouse):
                    game = Sudoku(mode="hard")
                    game_mode = "Hard"
                    mode = False
            if game is not None:
                ai = SudokuAI(game)
                solve = ai.solve()
            time.sleep(0.2)
        else:
            mouse = pygame.mouse.get_pos()
            if easy_rect.collidepoint(mouse):
                make_shadow(
                    "Easy",
                    easy_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    medium_font,
                    screen,
                )
            elif medium_rect.collidepoint(mouse):
                make_shadow(
                    "Medium",
                    medium_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    medium_font,
                    screen,
                )
            elif hard_rect.collidepoint(mouse):
                make_shadow(
                    "Hard",
                    hard_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    medium_font,
                    screen,
                )
            elif custom_rect.collidepoint(mouse):
                make_shadow(
                    "Custom",
                    custom_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    medium_font,
                    screen,
                )
            elif back_rect.collidepoint(mouse):
                make_shadow(
                    "Back",
                    back_rect.center,
                    LIGHTBLUE,
                    BLUE,
                    medium_font,
                    screen,
                )

        pygame.display.flip()
        continue

    # Show instructions screen.
    if instructions:

        # Title
        title = large_font.render("Sudoku Instructions", True, BLUE)
        title_rect = title.get_rect()
        title_rect.center = (width / 2), 46
        screen.blit(title, title_rect)

        # Rules
        rules = [
            "Click a cell or use arrow keys to select a cell.",
            "Each row, column and house must have",
            "distinct numbers ranging from 1 throuh 9.",
            "A house is a color coded 3 x 3 block.",
            "Fill all the cells to complete the puzzle!",
            'Use "AI move" for hint and "Solve" for solution.',
        ]
        for i, rule in enumerate(rules):
            color = LIGHTGREEN if i == 5 else LIGHTBLUE
            rule_text = small_font.render(rule, True, color)
            rule_rect = rule_text.get_rect()
            rule_rect.center = (width / 2), (100 + i * 40)
            screen.blit(rule_text, rule_rect)

        # back
        button_rect = pygame.Rect((width / 2) - 40, height - 66, 80, 36)
        button_text = medium_font.render("Back", True, BLACK)
        text_rect = button_text.get_rect()
        text_rect.center = button_rect.center
        pygame.draw.rect(screen, WHITE, button_rect)
        screen.blit(button_text, text_rect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse):
                instructions = False
                home = True
                time.sleep(0.3)
        else:
            mouse = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse):
                make_shadow(
                    "Back",
                    text_rect.center,
                    BLUE,
                    LIGHTBLUE,
                    medium_font,
                    screen,
                )

        pygame.display.flip()
        continue

    # draw board
    cells = []
    for i in range(ROW_COUNT):
        row = []
        for j in range(COLUMN_COUNT):

            rect = pygame.Rect(
                board_origin[0] + 2 * (j // 3) + j * cell_size,
                board_origin[1] + 2 * (i // 3) + i * cell_size,
                cell_size,
                cell_size,
            )

            r = 1 if i + 1 in [1, 2, 3] else 2 if i + 1 in [4, 5, 6] else 3
            c = 1 if j + 1 in [1, 2, 3] else 2 if j + 1 in [4, 5, 6] else 3
            house = 3 * (r - 1) + c

            color = LIGHTBLUE if house % 2 == 0 else PINK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            cell = game.get_cell(i + 1, j + 1)
            cell_value = str(cell.get_value()) if cell.get_value() != 0 else ""
            cell_color = (
                BLUE
                if cell.get_color() == 1
                else BLACK
                if cell.get_color() == 0
                else PURPLE
            )

            text = small_font.render(cell_value, True, cell_color)
            text_rect = text.get_rect()
            text_rect.center = rect.center
            screen.blit(text, text_rect)

            # Draw red box if it is a conflit
            if cell.get_conflicts_count():
                conflict_rect = pygame.Rect(
                    board_origin[0] + 1 + 2 * (j // 3) + j * cell_size,
                    board_origin[1] + 1 + 2 * (i // 3) + i * cell_size,
                    cell_size - 3,
                    cell_size - 3,
                )
                pygame.draw.rect(screen, RED, conflict_rect, 2)

            row.append(rect)
        cells.append(row)

    # Highlighting the current cell
    if highlight and not (splash or home or instructions or mode):
        i, j = highlight
        pygame.draw.rect(screen, SPRINGGREEN, cells[i][j], 3)

    # Show custom screen.
    if custom:
        # Draw Generate button.
        generate_button = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING,
            (1 / 3) * height - 110,
            (width / 3) - 2 * BOARD_PADDING,
            40,
        )
        button_text = medium_font.render("Generate", True, BLACK)
        button_rect = button_text.get_rect()
        button_rect.center = generate_button.center
        pygame.draw.rect(screen, WHITE, generate_button)
        screen.blit(button_text, button_rect)

        # Draw Validate button.
        valid_button = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING,
            (1 / 3) * height - 30,
            (width / 3) - 2 * BOARD_PADDING,
            48,
        )
        valid_text = "Valid!" if valid else "Validate" if valid is None else "Invalid"
        valid_color = SPRINGGREEN if valid else WHITE if valid is None else RED
        button_text = medium_font.render(valid_text, True, BLACK)
        button_rect = button_text.get_rect()
        button_rect.center = valid_button.center
        pygame.draw.rect(screen, valid_color, valid_button)
        screen.blit(button_text, button_rect)

        # Draw Play button.
        play_button = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING,
            (1 / 3) * height + 40,
            (width / 3) - 2 * BOARD_PADDING,
            48,
        )
        button_text = medium_font.render("Play", True, BLACK)
        button_rect = button_text.get_rect()
        button_rect.center = play_button.center
        pygame.draw.rect(screen, WHITE, play_button)
        screen.blit(button_text, button_rect)

    else:
        # Time
        if starting_time is None:
            elapsed_time = "0:00:00"
        elif end_time is None:
            curr_time = datetime.datetime.now().strftime("%H:%M:%S")
            curr_time = datetime.datetime.strptime(curr_time, "%H:%M:%S")
            elapsed_time = str(curr_time - starting_time)
        time_button = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING,
            (1 / 3) * height - 110,
            (width / 3) - 2 * BOARD_PADDING,
            40,
        )
        button_text = medium_font.render(elapsed_time, True, BLUE)
        button_rect = button_text.get_rect()
        button_rect.center = time_button.center
        pygame.draw.rect(screen, WHITE, time_button)
        screen.blit(button_text, button_rect)

        # Render game_mode
        game_mode_text = small_font.render(game_mode, True, SPRINGGREEN)
        game_mode_text_rect = game_mode_text.get_rect()
        game_mode_text_rect.center = (5 / 6) * width, (1 / 3) * height - 110 + 50
        screen.blit(game_mode_text, game_mode_text_rect)

        # Draw AI hint button
        ai_button = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING,
            (1 / 3) * height - 30,
            (width / 3) - 2 * BOARD_PADDING,
            48,
        )
        button_text = medium_font.render("AI Move", True, BLACK)
        button_rect = button_text.get_rect()
        button_rect.center = ai_button.center
        pygame.draw.rect(screen, WHITE, ai_button)
        screen.blit(button_text, button_rect)

        # Draw AI solve button
        solve_button = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING,
            (1 / 3) * height + 40,
            (width / 3) - 2 * BOARD_PADDING,
            48,
        )
        button_text = medium_font.render("Solve", True, BLACK)
        button_rect = button_text.get_rect()
        button_rect.center = solve_button.center
        pygame.draw.rect(screen, WHITE, solve_button)
        screen.blit(button_text, button_rect)

        # Draw won message
        if game.check_goal_state():
            won = True
            won_button = pygame.Rect(
                (2 / 3) * width + BOARD_PADDING,
                (1 / 3) * height - 30,
                (width / 3) - 2 * BOARD_PADDING,
                48,
            )
            button_text = medium_font.render("You Won!", True, BLACK)
            button_rect = button_text.get_rect()
            button_rect.center = won_button.center
            pygame.draw.rect(screen, SPRINGGREEN, won_button)
            screen.blit(button_text, button_rect)
            end_time = elapsed_time
        else:
            won = False

    # Draw Reset button
    reset_button = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING,
        (1 / 3) * height + 130,
        (width / 3) - 2 * BOARD_PADDING,
        48,
    )
    button_text = medium_font.render("Reset", True, BLACK)
    button_rect = button_text.get_rect()
    button_rect.center = reset_button.center
    pygame.draw.rect(screen, WHITE, reset_button)
    screen.blit(button_text, button_rect)

    # Draw Home button
    home_button = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING,
        (1 / 3) * height + 200,
        (width / 3) - 2 * BOARD_PADDING,
        48,
    )
    button_text = medium_font.render("Home", True, BLACK)
    button_rect = button_text.get_rect()
    button_rect.center = home_button.center
    pygame.draw.rect(screen, WHITE, home_button)
    screen.blit(button_text, button_rect)

    # Draw lines in between houses
    pygame.draw.line(
        screen,
        BLACK,
        (
            board_origin[0] + 3 * cell_size,
            board_origin[1] + 0 * cell_size,
        ),
        (
            board_origin[0] + 3 * cell_size,
            board_origin[1] + 9 * cell_size,
        ),
        2,
    )
    pygame.draw.line(
        screen,
        BLACK,
        (
            2 + board_origin[0] + 6 * cell_size,
            board_origin[1] + 0 * cell_size,
        ),
        (
            2 + board_origin[0] + 6 * cell_size,
            board_origin[1] + 9 * cell_size,
        ),
        2,
    )
    pygame.draw.line(
        screen,
        BLACK,
        (
            board_origin[0] + 0 * cell_size,
            board_origin[1] + 3 * cell_size,
        ),
        (
            board_origin[0] + 9 * cell_size,
            board_origin[1] + 3 * cell_size,
        ),
        2,
    )
    pygame.draw.line(
        screen,
        BLACK,
        (
            board_origin[0] + 0 * cell_size,
            2 + board_origin[1] + 6 * cell_size,
        ),
        (
            board_origin[0] + 9 * cell_size,
            2 + board_origin[1] + 6 * cell_size,
        ),
        2,
    )

    # show validation status.
    if valid is not None:
        pygame.display.flip()
        time.sleep(1)
        valid = None

    left, _, _ = pygame.mouse.get_pressed()
    if left == 1:

        mouse = pygame.mouse.get_pos()
        highlight = None

        if reset_button.collidepoint(mouse):
            game.reset()
            starting_time = None
            current = (0, 0)
            time.sleep(0.2)
        elif home_button.collidepoint(mouse):
            home = True
            game.reset()
            starting_time = None
            current = (0, 0)
            time.sleep(0.2)

        if custom:

            # Generate puzzle.
            if generate_button.collidepoint(mouse):
                gen_mode = choice(("Easy", "Medium", "Hard"))
                game_mode = "Custom " + gen_mode
                num_var = (
                    48 if gen_mode == "Easy" else 36 if gen_mode == "Medium" else 21
                )
                game = Sudoku(mode="custom")
                game.add_value(1, 1, choice(range(1, 10)), 0)
                game.add_value(2, 8, choice(range(1, 10)), 0)
                game.add_value(8, 2, choice(range(1, 10)), 0)
                game.add_value(9, 9, choice(range(1, 10)), 0)
                game.add_value(5, 5, choice(range(1, 10)), 0)
                ai = SudokuAI(game)
                solve = ai.solve()
                stack_1 = [(i, j) for i in range(1, 4) for j in range(1, 10)]
                stack_2 = [(i, j) for i in range(4, 7) for j in range(1, 10)]
                stack_3 = [(i, j) for i in range(7, 10) for j in range(1, 10)]
                stack_1 = sample(stack_1, num_var // 3)
                stack_2 = sample(stack_2, num_var // 3)
                stack_3 = sample(stack_3, num_var // 3)
                stack = stack_1 + stack_2 + stack_3
                puzzle = {loc: solve[loc] for loc in stack}
                game = Sudoku(mode="custom", puzzle=puzzle)

            # Validate puzzle.
            if valid_button.collidepoint(mouse) or play_button.collidepoint(mouse):
                new_game = Sudoku(mode="custom")
                cells_custom = game.get_cells()
                for cell in cells_custom:
                    if cells_custom[cell].value:
                        value = cells_custom[cell].value
                        x = cells_custom[cell].x
                        y = cells_custom[cell].y
                        new_game.add_value(x, y, value, 0)
                ai = SudokuAI(new_game)
                solve = ai.solve()
                valid = True if solve else False
                time.sleep(0.2)

            # Create game.
            if play_button.collidepoint(mouse) and valid:
                custom = False
                starting_time = None
                puzzle = {}
                cells_custom = game.get_cells()
                for cell in cells_custom:
                    if cells_custom[cell].value:
                        puzzle[cell] = cells_custom[cell].value
                game = Sudoku(mode="custom", puzzle=puzzle)

        else:

            # Display solution.
            if solve_button.collidepoint(mouse):
                for i, j in solve.items():
                    game.add_value(*i, j, 2)
                time.sleep(0.2)

            # Display hint.
            elif ai_button.collidepoint(mouse) and not won:
                hint_var, hint = ai.hint()
                game.add_value(*hint_var, hint, 2)
                time.sleep(0.2)

        # Get highlight.
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                if (
                    cells[i][j].collidepoint(mouse)
                    and game.get_cell(i + 1, j + 1).get_color()
                ):
                    highlight = (i, j)
                    current = highlight
                    break

    else:
        
        mouse = pygame.mouse.get_pos()
        if reset_button.collidepoint(mouse):
            make_shadow(
                "Reset", reset_button.center, BLUE, LIGHTBLUE, medium_font, screen
            )
        elif home_button.collidepoint(mouse):
            make_shadow(
                "Home", home_button.center, BLUE, LIGHTBLUE, medium_font, screen
            )

        if custom:
            if valid_button.collidepoint(mouse):
                make_shadow(
                    "Validate",
                    valid_button.center,
                    BLUE,
                    LIGHTBLUE,
                    medium_font,
                    screen,
                )
            elif play_button.collidepoint(mouse):
                make_shadow(
                    "Play", play_button.center, BLUE, LIGHTBLUE, medium_font, screen
                )
            elif generate_button.collidepoint(mouse):
                make_shadow(
                    "Generate",
                    generate_button.center,
                    BLUE,
                    LIGHTBLUE,
                    medium_font,
                    screen,
                )
        else:
            if solve_button.collidepoint(mouse):
                make_shadow(
                    "Solve", solve_button.center, BLUE, LIGHTBLUE, medium_font, screen
                )
            elif ai_button.collidepoint(mouse) and not won:
                make_shadow(
                    "AI Move", ai_button.center, BLUE, LIGHTBLUE, medium_font, screen
                )

    pygame.display.flip()
