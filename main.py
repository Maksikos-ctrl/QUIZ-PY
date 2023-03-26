import pygame
import database
import random
import requests
import json
import sys

from colors import WHITE, GREEN, RED


# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Milujeme Slovensko')

# Load the font
font = pygame.font.Font("assets/main.ttf", 20)

background = pygame.image.load('assets/index.png')

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



# Main game loop
while True:

    screen.blit(background, (0, 0))
    
    
    # Get a random question from the database
    question = database.get_random_question(conn)
    options = question['options']
    correct_answer = question['answer']

    # Render the question and options
    question_surface = font.render(question['question'], True, WHITE)
    option1_surface = font.render(options[0], True,  WHITE)
    option2_surface = font.render(options[1], True,  WHITE)
    option3_surface = font.render(options[2], True,  WHITE)
    option4_surface = font.render(options[3], True,  WHITE)

    # Create option boxes with background color
    option1_rect = pygame.Rect(100, 200, 200, 30)
    option2_rect = pygame.Rect(400, 200, 200, 30)
    option3_rect = pygame.Rect(100, 300, 200, 30)
    option4_rect = pygame.Rect(400, 300, 200, 30)

    

    # Display the question and options with background color
    screen.blit(question_surface, (100, 100))
    pygame.draw.rect(screen, (50, 50, 50), option1_rect)
    screen.blit(option1_surface, (100, 200))
    pygame.draw.rect(screen, (50, 50, 50), option2_rect)
    screen.blit(option2_surface, (400, 200))
    pygame.draw.rect(screen, (50, 50, 50), option3_rect)
    screen.blit(option3_surface, (100, 300))
    pygame.draw.rect(screen, (50, 50, 50), option4_rect)
    screen.blit(option4_surface, (400, 300))


    # Update the screen
    pygame.display.flip()

    selected_answer = None
    # Wait for a keypress
    while not selected_answer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if option1_rect.collidepoint(mouse_pos):
                    selected_answer = options[0]
                elif option2_rect.collidepoint(mouse_pos):
                    selected_answer = options[1]
                elif option3_rect.collidepoint(mouse_pos):
                    selected_answer = options[2]
                elif option4_rect.collidepoint(mouse_pos):
                    selected_answer = options[3]
                


        # Check if the selected answer is correct
        if selected_answer is not None:
            for i in range(4):
                if options[i] == correct_answer:
                    color = GREEN
                elif options[i] == selected_answer:
                    color = RED
                else:
                    color = (50, 50, 50) # Other options are gray
                pygame.draw.rect(screen, color, (option1_rect.x, option1_rect.y + 100*i, option1_rect.width, option1_rect.height))
                option_surface = font.render(options[i], True, (255, 255, 255))
                screen.blit(option_surface, (option1_rect.x, option1_rect.y + 100*i))

        # Wait for a keypress to continue
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        selected_answer = None
                        
                    
        break

    pygame.display.flip()
    
                

     
        
# Close the database connection
conn.close()

# Quit Pygame
pygame.quit()


