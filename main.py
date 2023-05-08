import pygame

import random
import requests
import json
import sys
import database
from questions import get_questions_from_api

from client import Client
from colors import *
from fonts import *
from pygame.locals import *
from moviepy.editor import VideoFileClip

# Initialize Pygame
pygame.init()

WIDTH = 800
HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Trivia Titans')

background = pygame.image.load('assets/index.gif')
background = pygame.transform.scale(background, (background.get_width() * 1.7, background.get_height() * 1.7))
background_game = pygame.image.load('assets/bg.png')

icon = pygame.image.load("assets/icon.png")


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
input_active = 0

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


#finish button
finish_rect = pygame.Rect(300, 300, 100, 30)
finish_text = pygame.image.load("assets/finish.png")
finish_text = pygame.transform.scale(finish_text, (finish_text.get_width() // 6, finish_text.get_height() // 6))
finish_rect.topright = screen.get_rect().topright

# Add a variable to track the current player's turn
current_player = 1

# Add a variable to track if the game has started
game_started = False

# Add a variable to track if a player has answered the current question
player_answered = False

# Add a variable to store the current player's score
player1_score = 0
player2_score = 0



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

# for displaying my nickname
nickname_surf = None
nickname_entered = 0
popup_closed = 0



conn = database.connect()
# conn_postgresql = database.connect_postgresql()
# database.create_scores_table(conn_postgresql)







# Fetch questions from the Open Trivia API and add them to the database
def get_questions_from_api(amount=50, category=None, difficulty=None, type=None):
    url = 'https://opentdb.com/api.php'
    params = {'amount': amount}
    if category:
        params['category'] = category
    if difficulty:
        params['difficulty'] = difficulty
    if type:
        params['type'] = type
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data['results']
        # Clear existing questions from the database
        database.clear_questions(conn)
        for result in results:
            question_type = result['type']
            question = result['question']
            correct_answer = result['correct_answer']

            if question_type == 'multiple':
                # Multiple Choice Question
                options = result['incorrect_answers'] + [correct_answer]
                database.add_questions(conn, question, correct_answer, *options)
            elif question_type == 'boolean':
                # True/False Question
                options = ['True', 'False']
                database.add_questions(conn, question, correct_answer, *options)
            elif question_type == 'text':
                # Short Answer Question
                database.add_questions(conn, question, correct_answer)

# Create the questions table in the database if it doesn't exist
cursor = conn.cursor()
database.create_questions_table(cursor)
database.create_scores_table(cursor)

# Add questions to the database if it's empty
if len(database.get_questions(conn)) == 0:
    get_questions_from_api(50)
    

# Define a variable to keep track of the current question index
current_question_index = 0

selected_answer = None

client = Client("localhost", 5555, nickname)

    



pygame.display.set_icon(icon)



score = 0
    
# Create the clock object to track FPS
clock = pygame.time.Clock()

FPS = 60

# Main game loop
while True:

    # Track time between frames
    dt = clock.tick(FPS)

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
    score_text = score_font.render(f"Score: {score}", True, YELLOW)
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


    def draw_nickname(nickname):
        nickname_surf = font.render(nickname, True, (255, 255, 255))
        nickname_rect = nickname_surf.get_rect()
        nickname_rect.topright = (WIDTH - 10, 10)
        screen.blit(nickname_surf, nickname_rect)




    
    def handle_input(client):
        global nickname_surf, password_surf, input_active, active_input, nickname, password, form_submitted, submit_text, submit_button, submit_color, account, nickname_entered, popup_closed
        
       
        if not nickname_entered and not popup_closed:
            nickname = ''
            password = ''
            active_input = None
            input_active = True
            nickname_surf = popup_font.render('', True, BLACK)
            password_surf = popup_font.render('', True, BLACK)
            

       
        
        
            while input_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        input_active = 0
                        nickname = ''
                        password = ''
                        popup_closed = 1

                            
                    
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
                                nickname_surf = account_nickname.render(nickname.upper(), True, BLUE)
                                account = nickname_surf
                                
                                
                                input_active = 0
                                popup_closed = 1
                            else:
                                print('Please enter a nickname')
                                nickname_entered = 0
                                input_active = 1
                                nickname = ''
                                password = ''
                                nickname_surf = popup_font.render('', True, BLACK)
                                password_surf = popup_font.render('', True, BLACK)
                                active_input = None
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                                                         
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

        
                
                # submit_color = GREEN if nickname else RED       
                pygame.draw.rect(popup_surface,  submit_color, submit_button, border_radius=10)
                submit_text = font_popUp.render("SIGN IN", True, BLACK)
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
            

    
    popup_open = 0   
       

    
   

    
    # Event handling
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            client.disconnect()
            
            pygame.quit()
            sys.exit()
         
            
            
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if account_rect.collidepoint(mouse_pos):
                popup_open = 1
                if not nickname_entered:

                    screen.blit(popup_surface, popup_rect)

                             
                pygame.display.flip()
                nickname = handle_input(client)
                if nickname:
                    client.nickname = nickname
                    client.send_message(nickname)
                    screen.blit(background_game, (0, 0))
                    screen.blit(account, account_rect)
                    draw_nickname(nickname)
                    pygame.display.flip()
                else:
                    screen.blit(background, (0, 0))
                    screen.blit(account, account_rect)
                    pygame.display.flip()

                popup_open = 0    
                    
                
                
                
                    
                    
                            
    
                
                
                
                
          
      
        if nickname_entered:
            if event.type == pygame.MOUSEBUTTONDOWN:

               
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

                    # Display the question and option buttons
                    question_surface = font_question.render(question['question'], True, PINK)
                    screen.blit(question_surface, (100, 100))

                    if question['type'] == 'multiple':
                        option3_rect = pygame.Rect(100, 300, 200, 30)
                        option3_text = font_answer.render(options[2], True, WHITE)
                        option4_rect = pygame.Rect(400, 300, 200, 30)
                        option4_text = font_answer.render(options[3], True, WHITE)

                        screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                        screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
                        screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                        screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))
                    elif question['type'] == 'boolean':
                        screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                        screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))   


                    # Draw the arrow image
                    arrow_rect = arrow.get_rect()
                    arrow_rect.bottomright = screen.get_rect().bottomright
                    screen.blit(arrow, arrow_rect)

                    # draw the finish button
                    finish_rect = arrow.get_rect()
                    finish_rect.topright = screen.get_rect().topright
                    screen.blit(finish_text, finish_rect)
                    


                   

    

                    # Check if an option button is clicked
                    selected_answer = None
             
                    while True:

                        # Track time between frames
                        dt = clock.tick(60)

                        # Calculate FPS
                        fps = int(clock.get_fps())


                    

                        
        


                        
                        screen.blit(fps_text, fps_rect)
                        screen.blit(score_text, score_rect)

                        # if score is greater than 150, the player wins the game and the pop up window appears with the message "You won!"
                        # if score > 150:
                        #     score = font.render("You won!", True, WHITE)
                        #     pygame.quit()
                        #     sys.exit()
                        

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                client.disconnect()
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if finish_rect.collidepoint(event.pos):
                                    nickname = client.nickname
                                    database.add_score(conn, nickname, score)   
                                    database.update_results(nickname, score) 
                                    client.disconnect()
                                    
                                    pygame.quit()
                                    sys.exit()
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

                                    # Display the question and option buttons
                                    question_surface = font_question.render(question['question'], True, PINK)
                                    screen.blit(question_surface, (100, 100))

                                    if question['type'] == 'multiple':
                                        option3_rect = pygame.Rect(100, 300, 200, 30)
                                        option3_text = font_answer.render(options[2], True, WHITE)
                                        option4_rect = pygame.Rect(400, 300, 200, 30)
                                        option4_text = font_answer.render(options[3], True, WHITE)

                                        screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                                        screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
                                        screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                                        screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))
                                    elif question['type'] == 'boolean':
                                        screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                                        screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))   


                                    # Draw the arrow image
                                    arrow_rect = arrow.get_rect()
                                    arrow_rect.bottomright = screen.get_rect().bottomright
                                    screen.blit(arrow, arrow_rect)


                                    finish_rect = arrow.get_rect()
                                    finish_rect.topright = screen.get_rect().topright
                                    screen.blit(finish_text, finish_rect)
                                    
                                





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
                                score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                pygame.display.flip()
                                
                            else:
                                message = font_answer.render("Nespravna odpoved!", True, RED)
                                screen.blit(message, (100, 400))
                                print("Nespravna odpoved")
                                score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                pygame.display.flip()
                                
                        

                            

                            # Wait for a keypress to continue
                            waiting = True
                            answered = False
                            while waiting:
                                
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN and finish_rect.collidepoint(event.pos)):
                                        client.disconnect()
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
                                        
                                        if question['type'] == 'multiple':
                                            option3_rect = pygame.Rect(100, 300, 200, 30)
                                            option3_text = font_answer.render(options[2], True, WHITE)
                                            option4_rect = pygame.Rect(400, 300, 200, 30)
                                            option4_text = font_answer.render(options[3], True, WHITE)

                                            screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                                            screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))
                                            screen.blit(option3_text, (option3_rect.x + 10, option3_rect.y + 5))
                                            screen.blit(option4_text, (option4_rect.x + 10, option4_rect.y + 5))
                                        elif question['type'] == 'boolean':
                                            screen.blit(option1_text, (option1_rect.x + 10, option1_rect.y + 5))
                                            screen.blit(option2_text, (option2_rect.x + 10, option2_rect.y + 5))   
                                
                                
                                        # Draw the arrow image
                                        arrow_rect = arrow.get_rect()
                                        arrow_rect.bottomright = screen.get_rect().bottomright
                                        screen.blit(arrow, arrow_rect)

                                        finish_rect = arrow.get_rect()
                                        finish_rect.topright = screen.get_rect().topright
                                        screen.blit(finish_text, finish_rect)
                    
                                    
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
                                            score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                            pygame.display.flip()
                                            
                                            
                                        else:
                                            message = font_answer.render("Nespravna odpoved!", True, RED)
                                            screen.fill(BLACK, (100, 400, message.get_width(), message.get_height()))
                                            screen.blit(message, (100, 400))
                                            print("Nespravna odpoved")
                                            score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                            pygame.display.flip()        
                                
                                    elif event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_SPACE:
                                            waiting = False
                                          
                                            pygame.display.flip() 
                                    
                           
                           
                   
                                           
                                            
                                    #break
                            nickname = client.nickname
                            database.add_score(conn, nickname, score)   
                            # database.store_results(nickname, score)  
                            database.update_results(nickname, score)        
                            
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


