import pygame
import sys
import os

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Load the sound effect for redirection
redirect_sound = pygame.mixer.Sound("C:\\Users\\codys\\OneDrive\\Desktop\\2d Game\\sound.mp3")
redirect_sound.set_volume(0.8)  # Set volume for the sound effect

# Load and play background music
background_music = "C:\\Users\\codys\\OneDrive\\Desktop\\2d Game\\background_music.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.2)  # Set volume for the background music
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Constants
WIDTH, HEIGHT = 400, 600
BALL_SIZE = 25  # Increased ball size
INITIAL_BALL_SPEED = 1.5  # Start off slow
MAX_BALL_SPEED = 100  # Maximum speed
BALL_SPEED_INCREMENT = 0.0041  # Increment speed gradually
LINE_WIDTH = 3  # Increased line width
GREY_LINE_OFFSET = 65  # Distance between grey lines and border lines (editable)
LINE_COLOR = (128, 128, 128)  # Grey color for the inside lines
BALL_COLOR = (0, 0, 255)  # Blue ball color
TEXT_COLOR = (0, 0, 0)  # Black text color
BACKGROUND_COLOR = (255, 255, 255)  # White background color

# File path for the high score
HIGH_SCORE_FILE = "C:\\Users\\codys\\OneDrive\\Desktop\\2d Game\\high score.txt"

# Scale background images to fit the screen
main_background = pygame.transform.scale(
    pygame.image.load(r"C:\Users\codys\OneDrive\Desktop\2d Game\outgame.png"),
    (WIDTH, HEIGHT)
)
fail_background = main_background  # Using the same background for fail and leaderboard pages
leaderboard_background = main_background  # Using the same background for fail and leaderboard pages
game_background = pygame.transform.scale(
    pygame.image.load(r"C:\Users\codys\OneDrive\Desktop\2d Game\ingame.png"),
    (WIDTH, HEIGHT)
)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Ball Game")

# Game objects
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
top_border = pygame.Rect(0, 50, WIDTH, LINE_WIDTH)
bottom_border = pygame.Rect(0, HEIGHT - 50, WIDTH, LINE_WIDTH)
top_grey_line = pygame.Rect(0, top_border.y + GREY_LINE_OFFSET, WIDTH, LINE_WIDTH)
bottom_grey_line = pygame.Rect(0, bottom_border.y - GREY_LINE_OFFSET, WIDTH, LINE_WIDTH)

# Variables
ball_speed = INITIAL_BALL_SPEED
ball_direction = ball_speed
game_active = False
points = 0
crossed_grey_line = False  # Tracks if the ball has fully crossed the grey line
high_score = 0  # Initialize high score
game_over = False
leaderboard_active = False  # Tracks if the leaderboard is active

# Fonts
font = pygame.font.Font(None, 36)

# Buttons
start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
leaderboard_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
home_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 120, 100, 50)

def draw_text(text, position, size=36, color=TEXT_COLOR, background=None):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)
    
    if background:
        # Expand the rectangle by a few pixels to ensure it covers the entire text
        pygame.draw.rect(screen, background, text_rect.inflate(50, 35))
    
    screen.blit(text_surface, position)

def load_high_score():
    global high_score
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                content = file.read().strip()
                if content.isdigit():
                    high_score = int(content)
                else:
                    high_score = 0
        else:
            high_score = 0
    except ValueError:
        high_score = 0

def save_high_score(score):
    if score > high_score:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))

def draw_start_screen():
    screen.blit(main_background, (0, 0))
    draw_text("2D Ball Game", (WIDTH // 2 - 100, HEIGHT // 2 - 100), size=48)
    pygame.draw.rect(screen, BALL_COLOR, start_button)
    draw_text("Start", (start_button.x + 20, start_button.y + 10), background=BALL_COLOR)
    pygame.draw.rect(screen, BALL_COLOR, leaderboard_button)
    draw_text("Leaderboard", (leaderboard_button.x + 15, leaderboard_button.y + 10), background=BALL_COLOR)
    pygame.display.flip()

def draw_leaderboard():
    screen.blit(leaderboard_background, (0, 0))
    draw_text("Leaderboard", (WIDTH // 2 - 100, HEIGHT // 2 - 100), size=48)
    draw_text(f"Player 1: {high_score} Points", (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    pygame.draw.rect(screen, BALL_COLOR, home_button)
    draw_text("Home", (home_button.x + 20, home_button.y + 10), background=BALL_COLOR)
    pygame.display.flip()

def draw_game():
    screen.blit(game_background, (0, 0))
    # Draw lines
    pygame.draw.rect(screen, (0, 0, 0), top_border)
    pygame.draw.rect(screen, (0, 0, 0), bottom_border)
    pygame.draw.rect(screen, LINE_COLOR, top_grey_line)
    pygame.draw.rect(screen, LINE_COLOR, bottom_grey_line)

    # Draw ball
    pygame.draw.ellipse(screen, BALL_COLOR, ball)

    # Draw points with white color only when the game is active
    if game_active:
        points_color = (255, 255, 255)  # White color when game is playing
    else:
        points_color = TEXT_COLOR  # Default text color otherwise

    points_surface = font.render(f"Points: {points}", True, points_color)
    screen.blit(points_surface, (10, 10))

def draw_game_over():
    screen.blit(fail_background, (0, 0))
    draw_text("Game Over", (WIDTH // 2 - 80, HEIGHT // 2 - 150), size=48)
    draw_text(f"Your Score: {points}", (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    draw_text(f"High Score: {high_score}", (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.draw.rect(screen, BALL_COLOR, restart_button)
    draw_text("Restart", (restart_button.x + 10, restart_button.y + 10), background=BALL_COLOR)
    pygame.draw.rect(screen, BALL_COLOR, home_button)
    draw_text("Home", (home_button.x + 20, home_button.y + 10), background=BALL_COLOR)
    pygame.display.flip()

def reset_ball():
    global ball_speed, ball_direction, crossed_grey_line
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed = INITIAL_BALL_SPEED  # Reset speed
    ball_direction = ball_speed
    crossed_grey_line = False

def check_fail_or_point():
    global game_active, points, crossed_grey_line, game_over
    if crossed_grey_line:
        points += 1  # Point scored
    else:
        game_active = False  # Fail condition
        game_over = True
        save_high_score(points)
        load_high_score()

def redirect_ball():
    global game_active, ball_direction, crossed_grey_line, game_over
    redirect_sound.play()
    
    # Check if the ball is fully past the grey line before redirecting
    if (ball_direction > 0 and ball.bottom > bottom_grey_line.bottom) or \
       (ball_direction < 0 and ball.top < top_grey_line.top):
        check_fail_or_point()
        ball_direction *= -1
        crossed_grey_line = False  # Reset after redirecting
    else:
        game_active = False  # Fail if redirected too early
        game_over = True
        save_high_score(points)
        load_high_score()

# Load the initial high score
load_high_score()

# Main menu loop
while True:
    if leaderboard_active:
        draw_leaderboard()
    elif game_over:
        draw_game_over()
    elif not game_active:
        draw_start_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if leaderboard_active:
                if home_button.collidepoint(event.pos):
                    leaderboard_active = False
            elif game_over:
                if restart_button.collidepoint(event.pos):
                    game_active = True
                    game_over = False
                    points = 0
                    reset_ball()
                elif home_button.collidepoint(event.pos):
                    game_over = False
            else:
                if start_button.collidepoint(event.pos):
                    game_active = True
                    points = 0
                    reset_ball()
                elif leaderboard_button.collidepoint(event.pos):
                    leaderboard_active = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                redirect_ball()

    if game_active:
        screen.fill(BACKGROUND_COLOR)
        ball.y += ball_direction

        # Gradually increase the ball's speed
        if abs(ball_direction) < MAX_BALL_SPEED:
            ball_direction += BALL_SPEED_INCREMENT if ball_direction > 0 else -BALL_SPEED_INCREMENT

        # Check if the ball is fully past the grey lines
        if ball_direction > 0 and ball.top >= bottom_grey_line.bottom + LINE_WIDTH:
            crossed_grey_line = True
        elif ball_direction < 0 and ball.bottom <= top_grey_line.top - LINE_WIDTH:
            crossed_grey_line = True

        # Fail if the ball touches the borders
        if ball.top <= top_border.bottom or ball.bottom >= bottom_border.top:
            game_active = False
            game_over = True
            save_high_score(points)
            load_high_score()

        draw_game()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
