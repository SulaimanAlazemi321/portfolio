import pygame
import sys
import random
import math

# Game constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)
GRID_COLOR = (40, 40, 40)
GREEN = (0, 255, 0)
BRIGHT_GREEN = (50, 255, 50)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 155, 0)
BLUE = (0, 100, 255)
PURPLE = (128, 0, 128)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ultimate Snake Game")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("arial", 72, bold=True)
menu_font = pygame.font.SysFont("arial", 36, bold=True)
score_font = pygame.font.SysFont("arial", 28, bold=True)
game_over_font = pygame.font.SysFont("arial", 50, bold=True)
info_font = pygame.font.SysFont("arial", 24)

# Load sounds
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    # If sound files don't exist, create dummy sounds
    eat_sound = pygame.mixer.Sound.play = lambda x: None
    crash_sound = pygame.mixer.Sound.play = lambda x: None

# Particle system
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.size = random.randint(2, 5)
        self.life = 30
    
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= 1
        return self.life <= 0
    
    def draw(self, surface):
        alpha = min(255, self.life * 8)
        color = (*self.color, alpha)
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (self.size//2, self.size//2), self.size//2)
        surface.blit(s, (int(self.x), int(self.y)))

# Helper functions
def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(window, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(window, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def draw_snake(snake, time):
    # Head should be different
    head = snake[0]
    pygame.draw.rect(window, BRIGHT_GREEN, (head[0]*CELL_SIZE, head[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(window, GREEN, (head[0]*CELL_SIZE+2, head[1]*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4))
    
    # Body segments
    for i, segment in enumerate(snake[1:]):
        pulse = math.sin(time*0.01 + i*0.5) * 0.2 + 0.8
        size_mod = int(pulse * 2)
        color_mod = int(pulse * 40)
        color = (0, 200 + color_mod, 0)
        
        pygame.draw.rect(window, color, 
                        (segment[0]*CELL_SIZE+size_mod, segment[1]*CELL_SIZE+size_mod, 
                         CELL_SIZE-size_mod*2, CELL_SIZE-size_mod*2))

def draw_food(food, time):
    pulse = math.sin(time*0.05) * 0.2 + 0.8
    food_radius = int(CELL_SIZE/2 * pulse)
    food_center = (food[0]*CELL_SIZE + CELL_SIZE//2, food[1]*CELL_SIZE + CELL_SIZE//2)
    
    # Glow effect
    for r in range(food_radius, 0, -2):
        alpha = 100 - r * 10
        if alpha < 0:
            break
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 100, 100, alpha), (r, r), r)
        window.blit(s, (food_center[0]-r, food_center[1]-r))
    
    # Food itself
    pygame.draw.circle(window, GOLD, food_center, food_radius)
    pygame.draw.circle(window, RED, food_center, food_radius-3)

def draw_score(score, high_score):
    score_surface = score_font.render(f"Score: {score}", True, WHITE)
    high_score_surface = score_font.render(f"High Score: {high_score}", True, GOLD)
    window.blit(score_surface, (10, 10))
    window.blit(high_score_surface, (WINDOW_WIDTH - high_score_surface.get_width() - 10, 10))

def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake:
            return pos

def create_particles(x, y, count, color):
    particles = []
    for _ in range(count):
        particles.append(Particle(x, y, color))
    return particles

def draw_menu():
    window.fill(BLACK)
    
    # Title
    title_surf = title_font.render("ULTIMATE SNAKE", True, GREEN)
    title_rect = title_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
    window.blit(title_surf, title_rect)
    
    # Snake logo
    snake_length = 8
    snake_start_x = WINDOW_WIDTH//2 - snake_length*CELL_SIZE//2
    snake_y = WINDOW_HEIGHT//2
    
    for i in range(snake_length):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(window, color, (snake_start_x + i*CELL_SIZE, snake_y, CELL_SIZE, CELL_SIZE))
    
    # Play instructions
    play_surf = menu_font.render("Press SPACE to Play", True, WHITE)
    play_rect = play_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3))
    window.blit(play_surf, play_rect)
    
    # Controls info
    controls_surf = info_font.render("Controls: Arrow Keys to move", True, WHITE)
    controls_rect = controls_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3 + 50))
    window.blit(controls_surf, controls_rect)

def game_over_screen(score, high_score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    window.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_surf = game_over_font.render("GAME OVER", True, RED)
    game_over_rect = game_over_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))
    window.blit(game_over_surf, game_over_rect)
    
    # Score
    score_surf = menu_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    window.blit(score_surf, score_rect)
    
    # High score
    if score == high_score and score > 0:
        high_score_surf = menu_font.render("NEW HIGH SCORE!", True, GOLD)
        high_score_rect = high_score_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        window.blit(high_score_surf, high_score_rect)
    
    # Restart instructions
    restart_surf = menu_font.render("Press R to Restart", True, WHITE)
    restart_rect = restart_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3))
    window.blit(restart_surf, restart_rect)
    
    quit_surf = menu_font.render("Press Q to Quit", True, WHITE)
    quit_rect = quit_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT*2//3 + 40))
    window.blit(quit_surf, quit_rect)

# Main game loop
def main():
    # Game variables
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)
    next_direction = direction
    food = random_food(snake)
    particles = []
    score = 0
    high_score = 0
    game_state = MENU
    game_time = 0
    
    running = True
    while running:
        game_time += 1
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if game_state == MENU:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        
                elif game_state == PLAYING:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_direction = (1, 0)
                        
                elif game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        # Reset game
                        snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
                        direction = (1, 0)
                        next_direction = direction
                        food = random_food(snake)
                        particles = []
                        score = 0
                        game_state = PLAYING
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
        
        # Update game state
        if game_state == MENU:
            draw_menu()
            
        elif game_state == PLAYING:
            # Update direction
            direction = next_direction
            
            # Move snake
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])
            
            # Check collisions
            if (
                new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake
            ):
                game_state = GAME_OVER
                try:
                    crash_sound.play()
                except:
                    pass
                # Create explosion particles at collision
                head_center_x = head_x * CELL_SIZE + CELL_SIZE // 2
                head_center_y = head_y * CELL_SIZE + CELL_SIZE // 2
                particles.extend(create_particles(head_center_x, head_center_y, 30, (255, 0, 0)))
            else:
                # Move the snake
                snake.insert(0, new_head)
                
                # Check if snake ate food
                if new_head == food:
                    score += 1
                    high_score = max(score, high_score)
                    food = random_food(snake)
                    try:
                        eat_sound.play()
                    except:
                        pass
                    
                    # Create particles at food location
                    food_center_x = new_head[0] * CELL_SIZE + CELL_SIZE // 2
                    food_center_y = new_head[1] * CELL_SIZE + CELL_SIZE // 2
                    particles.extend(create_particles(food_center_x, food_center_y, 15, (255, 215, 0)))
                else:
                    snake.pop()
            
            # Draw game
            window.fill(DARK_GRAY)
            draw_grid()
            
            # Update and draw particles
            i = 0
            while i < len(particles):
                if particles[i].update():
                    particles.pop(i)
                else:
                    particles[i].draw(window)
                    i += 1
            
            draw_snake(snake, game_time)
            draw_food(food, game_time)
            draw_score(score, high_score)
            
        elif game_state == GAME_OVER:
            # Update particles
            i = 0
            while i < len(particles):
                if particles[i].update():
                    particles.pop(i)
                else:
                    particles[i].draw(window)
                    i += 1
                    
            game_over_screen(score, high_score)
        
        pygame.display.flip()
        
        # Control game speed based on score
        speed = min(20, 10 + score // 5)  # Speed increases with score, max 20
        clock.tick(speed)

if __name__ == "__main__":
    main() 