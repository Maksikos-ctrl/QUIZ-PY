import pygame
import database
import random
import requests
import json
import sys

from colors import WHITE, GREEN,WHITE, BLACK, RED, YELLOW


# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('QUIZ GAME')

# Load the font
font_answer = pygame.font.Font("assets/main.ttf", 20)
font = pygame.font.Font("assets/main.ttf", 80)
font_question = pygame.font.Font("assets/main.ttf", 30)
fps_font = pygame.font.Font("assets/main.ttf", 20)

background = pygame.image.load('assets/index.png')
background_game = pygame.image.load('assets/background.png')

# Define the start button
button_rect = pygame.Rect(250, 250, 300, 100)
button_text = font.render("START", True, WHITE)

conn = database.connect()


# Fetch questions from the Open Trivia API and add them to the database
def get_questions_from_api(num_questions):
    url = f'https://opentdb.com/api.php?amount={num_questions}&type=multiple'
    response = requests.get(url)
    data = json.loads(response.text)
    results = data.get('results')
    if results:
        for result in results:
            question = result['question']
            correct_answer = result['correct_answer']
            incorrect_answers = result['incorrect_answers']
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)
            database.add_questions(conn, question, correct_answer, *options)

# Create the questions table in the database if it doesn't exist
cursor = conn.cursor()
database.create_questions_table(cursor)

# Add questions to the database if it's empty
if len(database.get_questions(conn)) == 0:
    get_questions_from_api(50)


    
# Create the clock object to track FPS
clock = pygame.time.Clock()


# Main game loop
while True:

    # Track time between frames
    dt = clock.tick(60)

    # Calculate FPS
    fps = int(clock.get_fps())

    # Fill the background with white
    screen.fill(WHITE)

    # Draw the background image
    screen.blit(background, (0, 0))

    # Draw the start button
    pygame.draw.rect(screen, BLACK, button_rect, border_radius=10)
    button_rect.center = screen.get_rect().center
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))


    # Render the current FPS on the screen
    fps_text = fps_font.render(f"FPS: {fps}", True, GREEN)
    fps_rect = fps_text.get_rect(bottomright=screen.get_rect().bottomright)
    screen.blit(fps_text, fps_rect)

    # Update the display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # Move to part 2
                # PART 2
                screen.blit(background_game, (0, 0))

                # Get a random question from the database
                question = database.get_random_question(conn)
                options = question['options']
                correct_answer = question['answer']

                # Create option buttons with background color and text
                option1_rect = pygame.Rect(100, 200, 200, 30)
                option1_text = font_answer.render(options[0], True, WHITE)
                option2_rect = pygame.Rect(400, 200, 200, 30)
                option2_text = font_answer.render(options[1], True, WHITE)
                option3_rect = pygame.Rect(100, 300, 200, 30)
                option3_text = font_answer.render(options[2], True, WHITE)
                option4_rect = pygame.Rect(400, 300, 200, 30)
                option4_text = font_answer.render(options[3], True, WHITE)

                # Display the question and option buttons
                question_surface = font_question.render(question['question'], True, YELLOW)
                screen.blit(question_surface, (100, 100))
                
                screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
               
                screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
              
                screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                
                screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))

   

                # Check if an option button is clicked
                selected_answer = None
                while True:

                    # Track time between frames
                    dt = clock.tick(60)

                    # Calculate FPS
                    fps = int(clock.get_fps())


                    # Render the current FPS on the screen
                    # fps_text = fps_font.render(f"FPS: {fps}", True, GREEN)
                    # fps_rect = fps_text.get_rect(bottomright=screen.get_rect().bottomright)
                    screen.blit(fps_text, fps_rect)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if option1_rect.collidepoint(event.pos):
                                selected_answer = options[0]
                            elif option2_rect.collidepoint(event.pos):
                                selected_answer = options[1]
                            elif option3_rect.collidepoint(event.pos):
                                selected_answer = options[2]
                            elif option4_rect.collidepoint(event.pos):
                                selected_answer = options[3]

                    # Check if an option button was clicked
                    if selected_answer:
                        # Check if the answer is correct
                        if selected_answer == correct_answer:
                            message = font.render("Spravna odpoved!", True, GREEN)
                            screen.blit(message, (100, 400))
                            print("Spravna odpoved")
                            pygame.display.flip()
                        else:
                            message = font.render("Nespravna odpoved!", True, RED)
                            screen.blit(message, (100, 400))
                            print("Nespravna odpoved")
                            pygame.display.flip()

                        # Wait for a keypress to continue
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        waiting = False

                                        
                                        
                        
                        # Exit the outer while loop
                        break

                    pygame.display.flip()

                  

                pygame.display.flip()


                




     
        
# Close the database connection
conn.close()

# Quit Pygame
pygame.quit()


