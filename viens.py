import pygame
import random
import time
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spēle")

Background = (255, 255, 255)
Aplis = (0, 0, 0)
Poga = (0, 255, 0)

circle_radius = 30
num_clicks = 10
button_width, button_height = 200, 60

button_x = (WIDTH - button_width) // 2
button_y = (HEIGHT - button_height) // 2

click_distances = []
reaction_times = []

def draw_start_button():
    pygame.draw.rect(screen, Poga, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Sākt spēli", True, Aplis)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def play_game():
    for _ in range(num_clicks):
        circle_x = random.randint(circle_radius, WIDTH - circle_radius)
        circle_y = random.randint(circle_radius, HEIGHT - circle_radius)

        screen.fill(Background)
        pygame.draw.circle(screen, Aplis, (circle_x, circle_y), circle_radius)
        pygame.display.flip()

        start_time = time.time()
        clicked = False

        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    end_time = time.time()
                    mouse_x, mouse_y = event.pos
                    clicked = True

                    distance = np.sqrt((mouse_x - circle_x)**2 + (mouse_y - circle_x)**2)
                    click_distances.append(distance)

                    reaction_time = end_time - start_time
                    reaction_times.append(reaction_time)

def analyze_data():
    if click_distances:
        mean_distance = np.mean(click_distances)
        std_distance = np.std(click_distances)
        print("Vidējais attālums līdz centram:", mean_distance)
        print("Standartnovirze:", std_distance)

        mean_time = np.mean(reaction_times)
        std_time = np.std(reaction_times)
        print("Vidējais reakcijas laiks:", mean_time)
        print("Reakcijas laika standartnovirze:", std_time)

        print("Gausa sadalījums")
        print("Vidējā vērtība:", mean_distance)
        print("Standartnovirze:", std_distance)

def main():
    running = True
    game_started = False

    while running:
        screen.fill(Background)
        
        if not game_started:
            draw_start_button()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if not game_started and button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    game_started = True
                    play_game()
                    analyze_data()
                    running = False

    pygame.quit()

main()
