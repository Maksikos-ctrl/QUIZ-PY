import pygame

import random
import requests
import json
import sys
import database
import socket
from client import Client

from colors import WHITE, GREEN,WHITE, BLACK, RED, BANANA, PINK, DARK_GREEN, BLUE
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('QUIZ GAME')

# Load the font
font_answer = pygame.font.Font("assets/main.ttf", 30)
font_popUp = pygame.font.Font("assets/main.ttf", 20)

font = pygame.font.Font("assets/main.ttf", 80)
font_question = pygame.font.Font("assets/main.ttf", 23)
fps_font = pygame.font.Font("assets/main.ttf", 25)
score_font = pygame.font.Font("assets/main.ttf", 30)
account_font = pygame.font.Font("assets/main.ttf", 20)
popup_font = pygame.font.Font("assets/main.ttf", 25)
ps_font = pygame.font.Font(None, 32)

background = pygame.image.load('assets/index.png')
background_game = pygame.image.load('assets/bg.png')

# Define the start button
button_rect = pygame.Rect(250, 250, 300, 100)
button_text = font.render("START", True, WHITE)





popup_width = 800
popup_height = 600
popup_surface = pygame.Surface((popup_width, popup_height))
popup_rect = popup_surface.get_rect(center=screen.get_rect().center)
popup_bg = pygame.image.load('assets/bg_popup.jpg')
popup_bg = pygame.transform.scale(popup_bg, (popup_width, popup_height))
popup_surface.blit(popup_bg, (0, 0))


# Create the input fields and the submit button
nickname_input = pygame.Rect(200, 200, 300, 30)
password_input = pygame.Rect(200, 250, 300, 30)
submit_button = pygame.Rect(300, 300, 100, 30)
pop_up_button = GREEN

# Draw the input fields and the submit button on the popup surface
pygame.draw.rect(popup_surface, (0, 0, 0), nickname_input, 2)
pygame.draw.rect(popup_surface, (0, 0, 0), password_input, 2)
pygame.draw.rect(popup_surface, pop_up_button, submit_button, border_radius=10)
nickname_img = pygame.image.load('assets/acc.png')
nickname_img = pygame.transform.scale(nickname_img, (nickname_img.get_width() // 16, nickname_img.get_height() // 16))
popup_surface.blit(nickname_img, (159, 200))
password_img = pygame.image.load('assets/password.png')
password_img = pygame.transform.scale(password_img, (password_img.get_width() // 8, password_img.get_height() // 8))
popup_surface.blit(password_img, (159, 250))
submit_text = font_popUp.render("Submit", True, BLACK)
popup_surface.blit(submit_text, (313, 307))
submit_button.center = popup_surface.get_rect().center
            
# Event handling
input_active = 1

active_input = None
nickname = ''
password = ''

#hover colors
button_hovered_color = BANANA
button_color = BLACK


active_color = 0
color_active = pygame.Color('lightskyblue3')
submit_hovered = WHITE
submit_color = GREEN

color = color_active
form_submitted = True  




# Load the arrow image
arrow = pygame.image.load('assets/arrow1.png')
arrow = pygame.transform.scale(arrow, (arrow.get_width() // 2, arrow.get_height() // 2))


arrow_rect = arrow.get_rect()
arrow_rect.bottomright = screen.get_rect().bottomright

# Load the account image
account = pygame.image.load('assets/acc.png')
account = pygame.transform.scale(account, (account.get_width() // 8, account.get_height() // 8))

account_rect = account.get_rect()
account_rect.topright = screen.get_rect().topright



conn = database.connect()
# conn_postgresql = database.connect_postgresql()
# database.create_scores_table(conn_postgresql)







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
    

# Define a variable to keep track of the current question index
current_question_index = 0

selected_answer = None








# player_name = input('Enter your name: ')
score = 0
    
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


    mouse_pos = pygame.mouse.get_pos()
    
    


    if button_rect.collidepoint(mouse_pos):
        button_color = button_hovered_color
    else:
        button_color = BLACK

    # Draw the start button
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    button_rect.center = screen.get_rect().center
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))


    


    # Render the current FPS on the screen
    fps_text = fps_font.render(f"FPS: {fps}", True, BLUE)
    fps_rect = fps_text.get_rect(bottomleft=screen.get_rect().bottomleft)
    screen.blit(fps_text, fps_rect)


    # render the current score on the screen
    score_text = score_font.render(f"Score: {score}", True, DARK_GREEN)
    score_rect = score_text.get_rect(topleft=screen.get_rect().topleft)
    screen.blit(score_text, score_rect)

    screen.blit(account, account_rect)

         


    # Update the display
    pygame.display.flip()
    


    def draw_popup_images():
        nickname_img = pygame.image.load('assets/acc.png')
        nickname_img = pygame.transform.scale(nickname_img, (nickname_img.get_width() // 16, nickname_img.get_height() // 16))
        popup_surface.blit(nickname_img, (159, 200))
        password_img = pygame.image.load('assets/password.png')
        password_img = pygame.transform.scale(password_img, (password_img.get_width() // 8, password_img.get_height() // 8))
        popup_surface.blit(password_img, (159, 250))
       
 
      
        
    client = Client("localhost", 5555, nickname)

    def handle_input(client):
        global nickname_surf, password_surf, input_active, active_input, nickname, password, form_submitted, submit_text, submit_button, submit_color
        nickname = ''
        password = ''
        active_input = None
        input_active = 1
        nickname_surf = popup_font.render('', True, BLACK)
        password_surf = popup_font.render('', True, BLACK)
        nickname_entered = 0
        

       
        
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = 0
                    nickname = ''
                    password = ''
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                     
                    if nickname_input.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                        active_input = "nickname"
                    
                    elif password_input.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                        active_input = "password"

                    elif submit_button.collidepoint(event.pos):
                        if nickname:
                            nickname_entered = 1
                            client.nickname = nickname
                        input_active = 0
                      
                    
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        active_input = None
                
                elif event.type == pygame.KEYDOWN:
                    if active_input == "nickname":
                        if event.key == pygame.K_BACKSPACE:
                            nickname = nickname[:-1]
                        else:
                            nickname += event.unicode
                        nickname_surf = popup_font.render(nickname, True, BLACK)

                    elif active_input == "password":
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        else:
                            password += event.unicode
                        password_surf = popup_font.render("*" * len(password), True, BLACK)
                    if event.key == pygame.K_RETURN:
                        active_input = "password" 
                    elif event.key == pygame.K_RETURN and nickname:
                        input_active = False
                       

                        
            
                
                     
                        
                

            
            popup_surface.blit(popup_bg, (0, 0))
            draw_popup_images()

            
            submit_color = GREEN if nickname else RED       
            pygame.draw.rect(popup_surface,  submit_color, submit_button, border_radius=10)
            submit_text = font_popUp.render("Submit", True, BLACK)
            popup_surface.blit(submit_text, (313, 307))
            submit_button.center = (350, 316)
            nickname_input = pygame.Rect(200, 200, 300, 30)
            password_input = pygame.Rect(200, 250, 300, 30)
            pygame.draw.rect(screen, color, nickname_input)
            pygame.draw.rect(screen, color, password_input)
            

            nickname_surface = popup_font.render(nickname, True, WHITE)
            password_surface = ps_font.render("*" * len(password), True, WHITE)
            
            
            screen.blit(nickname_surface, (nickname_input.x+5, nickname_input.y+5))
            screen.blit(password_surface, (password_input.x+5, password_input.y+5))
            
            
            nickname_input.w = max(200, nickname_surface.get_width()+10)
            password_input.w = max(200, password_surface.get_width()+10)
            
            
            
            pygame.display.flip()
            clock.tick(60)

        if nickname_entered:
            return nickname   
        else:
            return None


    # Event handling
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if account_rect.collidepoint(mouse_pos):
                screen.blit(popup_surface, popup_rect)
                       
                pygame.display.flip()
                print("account clicked")
                nickname = handle_input(client)
                if nickname:
                    nickname_entered = 1
                client = Client("localhost", 5555, nickname)
                
                
                
                
          
      
                     
            elif button_rect.collidepoint(event.pos):                  
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
                question_surface = font_question.render(question['question'], True, PINK)
                screen.blit(question_surface, (100, 100))
                
                screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
               
                screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
              
                screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                
                screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))


                # Draw the arrow image
                arrow_rect = arrow.get_rect()
                arrow_rect.bottomright = screen.get_rect().bottomright
                screen.blit(arrow, arrow_rect)

                # Display the player's name
                # player_text = font_question.render(f"Player: {player_name}", True, WHITE)
                # screen.blit(player_text, (-30, 10))
                # pygame.display.update()

   

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
                    screen.blit(score_text, score_rect)

                       # if score is greater than 150, the player wins the game and the pop up window appears with the message "You won!"
                    # if score > 150:
                    #     score = font.render("You won!", True, WHITE)
                    #     pygame.quit()
                    #     sys.exit()
                    

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if arrow_rect.collidepoint(event.pos):

                                dt = clock.tick(60)

                                # Calculate FPS
                                fps = int(clock.get_fps())

                                print("Clicked on arrow")

                                screen.blit(background_game, (0, 0))
                                # when i have clicked on arrow, next question has to appear on the screen and old clears out
                                current_question_index += 1
                                

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
                                question_surface = font_question.render(question['question'], True, PINK)
                                screen.blit(question_surface, (100, 100))
                                
                                screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                            
                                screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
                            
                                screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                                
                                screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))


                                # Draw the arrow image
                                arrow_rect = arrow.get_rect()
                                arrow_rect.bottomright = screen.get_rect().bottomright
                                screen.blit(arrow, arrow_rect)
                            





                            elif option1_rect.collidepoint(event.pos):
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
                            message = font_answer.render("Spravna odpoved!", True, GREEN)
                            screen.blit(message, (100, 400))
                            print("Spravna odpoved")
                            score += 10
                            score_text = score_font.render("Score:" + str(score), True, DARK_GREEN)
                            pygame.display.flip()
                            
                        else:
                            message = font_answer.render("Nespravna odpoved!", True, RED)
                            screen.blit(message, (100, 400))
                            print("Nespravna odpoved")
                            score_text = score_font.render("Score:" + str(score), True, DARK_GREEN)
                            pygame.display.flip()
                            
                      

                         

                        # Wait for a keypress to continue
                        waiting = True
                        answered = False
                        while waiting:
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN and arrow_rect.collidepoint(event.pos):

                                    
       
                                    dt = clock.tick(60)

                                    # Calculate FPS
                                    fps = int(clock.get_fps())


                                    
                                    print("Clicked on arrow")

                                    screen.blit(background_game, (0, 0))
                                  

                                    

                                    # when i have clicked on arrow, next question has to appear on the screen and old clears out
                                    current_question_index += 1
                                    answered = False
                                    selected_answer = None
                                    
                        
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
                                    question_surface = font_question.render(question['question'], True, PINK)
                                    screen.blit(question_surface, (100, 100))
                                    
                                    screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                                
                                    screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
                                
                                    screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                                    
                                    screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))
                            
                            
                                    # Draw the arrow image
                                    arrow_rect = arrow.get_rect()
                                    arrow_rect.bottomright = screen.get_rect().bottomright
                                    screen.blit(arrow, arrow_rect)
                                 
                                    screen.blit(fps_text, fps_rect)
                                    
                                    screen.blit(score_text, score_rect)
                                    
                                  


                                    pygame.display.flip()
                                    
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    

                                    
                                
                                    if option1_rect.collidepoint(event.pos):
                                        selected_answer = options[0]
                                        
                                    elif option2_rect.collidepoint(event.pos):
                                        selected_answer = options[1]
                                        
                                    elif option3_rect.collidepoint(event.pos):
                                        selected_answer = options[2]
                                        
                                    elif option4_rect.collidepoint(event.pos):
                                        selected_answer = options[3]
                                        
                                        
                                    if selected_answer == correct_answer:
                                        message = font_answer.render("Spravna odpoved!!!!", True, GREEN)
                                        screen.fill(BLACK, (100, 400, message.get_width(), message.get_height()))
                                        screen.blit(message, (100, 400))
                                        print("Spravna odpoved")
                                        score += 10
                                        score_text = score_font.render("Score:" + str(score), True, DARK_GREEN)
                                        pygame.display.flip()
                                        
                                        
                                    else:
                                        message = font_answer.render("Nespravna odpoved!", True, RED)
                                        screen.fill(BLACK, (100, 400, message.get_width(), message.get_height()))
                                        screen.blit(message, (100, 400))
                                        print("Nespravna odpoved")
                                        score_text = score_font.render("Score:" + str(score), True, DARK_GREEN)
                                        pygame.display.flip()        
                            
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        waiting = False
                                        pygame.display.flip() 
                                 
                                        #break
                                    
                                #break
                                   
                        
                        # Exit the outer while loop
                        break

                    pygame.display.flip()

               
                
                
                
                
                

                  

                pygame.display.flip()



                




     
        
# Close the database connection to SQLlite
conn.close()

# Close the connection to the Postgree database
# conn_postgresql.close()

# Quit Pygame
pygame.quit()


