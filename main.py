import pygame
import socket
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
background_game = pygame.transform.scale(background_game, (background_game.get_width() // 1.4, background_game.get_height() // 1.5))

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




# for input answer + enter button
input_rect = pygame.Rect(100, 300, 400, 40)
input_text = ''
input_active = False
input_color = pygame.Color('lightskyblue3')
input_color_active = pygame.Color('dodgerblue2')
input_color = input_color_active
input_rect.center = (WIDTH // 2, HEIGHT // 2)
enter_button = pygame.Rect(300, 300, 100, 30)
enter_text = font_popUp.render("Enter", True, WHITE)
enter_button.center = (350, 316)


#img for rules
rules_img = pygame.image.load('assets/rules.png')
rules_img = pygame.transform.scale(rules_img, (rules_img.get_width() // 8, rules_img.get_height() // 8))
rules_rect = rules_img.get_rect()
rules_rect.bottomright = screen.get_rect().bottomright




# for sounds 
pygame.mixer.init()
correct_sound = pygame.mixer.Sound('assets/correct.mp3')
wrong_sound = pygame.mixer.Sound('assets/wrong.mp3')



conn = database.connect()


         
# Create the questions table in the database if it doesn't exist
cursor = conn.cursor()
database.create_questions_table(cursor)
database.create_scores_table(cursor)


# # Execute the query to fetch all rows from the questions table
# cursor.execute('SELECT type FROM questions')

# # Fetch all the rows and print the values in the type column
# rows = cursor.fetchall()
# for row in rows:
#     print(row[0])

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
    fps_text = fps_font.render(f"FPS: {fps}", True, DARK_GREEN)
    fps_rect = fps_text.get_rect(bottomleft=screen.get_rect().bottomleft)
    screen.blit(fps_text, fps_rect)


    # render the current score on the screen
    score_text = score_font.render(f"Score: {score}", True, YELLOW)
    score_rect = score_text.get_rect(topleft=screen.get_rect().topleft)
    screen.blit(score_text, score_rect)

    screen.blit(account, account_rect)
    screen.blit(rules_img, rules_rect)

         


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
                                database.store_results(nickname, score)
                                database.update_results(nickname, score)
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
            if rules_rect.collidepoint(mouse_pos):
                rules_bg = pygame.image.load('assets/rules_bg.jpg')
                rules_bg = pygame.transform.scale(rules_bg, (rules_bg.get_width() * 2, rules_bg.get_height() * 2))
                screen.blit(rules_bg, (0, 0))
                
                title_surface = title_font.render("RULES", True, WHITE)
                title_rect = title_surface.get_rect()
                title_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 100)
                screen.blit(title_surface, title_rect)

                rules_text = [
                    "1. To play the game, you need to sign in with a nickname and password.",
                    "2. Answer the questions correctly to earn points.",
                    "3. You can choose from multiple-choice options, boolean or provide an input answer.",
                    "4. Each correct answer earns you 10 points and you will be notified your answer is correct.",
                    "5. Incorrect answers won't cost you any points. You will be notified your answer is wrong.",
                    "6. Use the arrow button to proceed to the next question.",
                    "7. Click on the 'Finish' button to end the game and see your final score.",
                ]

       
                
                rules_margin = 20  # Margin between each rule line
                rules_position = (90, title_rect.bottom + 30)  # Starting position of the rules text

                for i, rule in enumerate(rules_text):
                    rule_surface = rules_font.render(rule, True, WHITE)
                    rule_rect = rule_surface.get_rect()
                    rule_rect.topleft = (rules_position[0], rules_position[1] + (i * (rule_rect.height + rules_margin)))
                    screen.blit(rule_surface, rule_rect)

                pygame.display.flip()
                quit_rules = False  # Flag to indicate if the user wants to quit the rules screen

                # Wait for the user to click outside the rules image
                while not quit_rules:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            quit_rules = True  
                            break

                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if not rules_rect.collidepoint(mouse_pos):  # Check if the mouse is outside the rules image
                                break

                    clock.tick(60)



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

                    # Display the type of question in console
                    print("Question: ", question)    

                    
                    options = question['options']
                    correct_answer = question['answer']
                    question_type = question['type']

                    # Display the question and option buttons
                    question_surface = font_question.render(question['question'].replace('&quot;', ' ').replace('&#039', ' ').replace(";s ", '"').replace('&#039;', " "), True, ORANGE)
                    screen.blit(question_surface, (50, 100))


                    
                    
                    # Display the type of question in console
                    print("Type of question is: ", question_type)

                   

                    

                 

                    if question_type == 'multiple':
                        option1_rect = pygame.Rect(100, 200, 200, 30)
                        option1_text = font_answer.render(options[0].replace('&quot;', '"') if options else '', True, WHITE)
                        option2_rect = pygame.Rect(400, 200, 200, 30)
                        option2_text = font_answer.render(options[1].replace('&quot;', '"') if len(options) > 1 else '', True, WHITE)
                        screen.blit(option1_text, (option1_rect.x, option1_rect.y + 5))
                        screen.blit(option2_text, (option2_rect.x, option2_rect.y + 5))

                        if len(options) > 2 and len(options) != 3:
                            option3_rect = pygame.Rect(100, 300, 200, 30)
                            option3_text = font_answer.render(options[2].replace('&quot;', '"'), True, WHITE)
                            screen.blit(option3_text, (option3_rect.x, option3_rect.y + 5))

                        # Clear the third option if len(options) == 3
                        elif len(options) == 3:
                            option3_rect = pygame.Rect(100, 300, 200, 30)
                            option3_text = font_answer.render('', True, WHITE)
                            screen.blit(option3_text, (option3_rect.x, option3_rect.y + 5))

                        if len(options) > 3:
                            option4_rect = pygame.Rect(400, 300, 200, 30)
                            option4_text = font_answer.render(options[3].replace('&quot;', '"') if len(options) > 3 else '', True, WHITE)
                            screen.blit(option4_text, (option4_rect.x, option4_rect.y + 5))


                        # Clear the fourth and fifth options if len(options)
                        if len(options) == 5 and len(options) > 5:
                            option5_text = font_answer.render('', True, WHITE)
                            option6_text = font_answer.render('', True, WHITE)
                            option7_text = font_answer.render('', True, WHITE)
                            option5_rect = pygame.Rect(400, 300, 200, 30)
                            option6_rect = pygame.Rect(400, 300, 200, 30)
                            option7_rect = pygame.Rect(400, 300, 200, 30)
                            screen.blit(option5_text, (option5_rect.x, option5_rect.y + 5))
                            screen.blit(option6_text, (option6_rect.x, option6_rect.y + 5))
                            screen.blit(option7_text, (option7_rect.x, option7_rect.y + 5))


                            



                   
                    if question_type == 'input':
                        # Display the input field
                        input_text = ''
                        input_active = True
                        active_input = None
                        input_surface = input_font.render('', True, WHITE)

                        while input_active:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    input_active = False
                                    input_text = ''

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if input_rect.collidepoint(event.pos):
                                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                                        active_input = "input"

                                    elif (enter_button.collidepoint(event.pos) or event.type == pygame.K_RETURN) and input_text:
                                        if input_text == correct_answer:
                                            correct_sound.play()
                                            score += 10
                                            input_active = False
                                            input_text = ''
                                            message = font_answer.render("Spravna odpoved!", True, GREEN)
                                            screen.blit(message, (300, 500))
                                            pygame.display.flip()
                                            break

                                        else:
                                            wrong_sound.play()
                                            input_active = False
                                            message = font_answer.render("Nespravna odpoved!", True, RED)
                                            screen.blit(message, (300, 500))
                                            input_text = ''
                                            pygame.display.flip()
                                            break

                                elif event.type == pygame.KEYDOWN:
                                    if active_input == "input":
                                        

                                        if event.key == pygame.K_BACKSPACE:
                                            input_text = input_text[:-1]
                                            
                                        elif event.unicode.isnumeric() or event.unicode in ['-', '.']:
                                            input_text += event.unicode
                                        else:
                                            if len(input_text) < 35:
                                             
                                                input_text += event.unicode   
                                        input_surface = input_font.render(input_text, True, WHITE)
                                      

                            enter_button = pygame.Rect(300, 390, 100, 30)
                            enter_text = font_input.render("Enter", True, WHITE)
                            pygame.draw.rect(screen, input_color, enter_button, border_radius=10)
                            screen.blit(enter_text, (313, 390))

                       
                            pygame.draw.rect(screen, BLUE, input_rect)
                            input_surface = input_font.render(input_text, True, WHITE)
                            # input_rect.width = max(input_surface.get_width() + 10, 100) 
                            screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

                            if input_surface.get_width() > input_rect.width - 10:
                                input_rect.x = WIDTH // 2 - input_rect.width // 2
                            else:
                                input_rect.center = (WIDTH // 2, HEIGHT // 2)
                            

                            pygame.display.flip()
                            clock.tick(60)

                                           
                            
                                            
                    arrow_rect = arrow.get_rect()
                    arrow_rect.bottomright = screen.get_rect().bottomright
                    screen.blit(arrow, arrow_rect)


                    finish_rect = arrow.get_rect()
                    finish_rect.topright = screen.get_rect().topright
                    screen.blit(finish_text, finish_rect)
            
            




                   

    

                    # Check if an option button is clicked
                    selected_answer = None
                    input_text = ''
             
                    while True:

                        # Track time between frames
                        dt = clock.tick(60)

                        # Calculate FPS
                        fps = int(clock.get_fps())


                                  
                        screen.blit(fps_text, fps_rect)
                        screen.blit(score_text, score_rect)

                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if event.type == pygame.QUIT:
                                    client.disconnect()
                                    pygame.quit()
                                    sys.exit()
                          
                                if finish_rect.collidepoint(event.pos):
                                    nickname = client.nickname
                                    database.store_results(nickname, score)
                                    database.update_results(nickname, score)
                                    client.disconnect()

                                    results = []
                                    with open('results.txt', 'r') as f:
                                        for line in f:
                                            if line.strip():
                                                last_comma_index = line.rfind(', has earned: ')
                                                if last_comma_index != -1:
                                                    nickname = line[:last_comma_index].strip()
                                                    score = line[last_comma_index + len(', has earned: '):].strip()
                                                    results.append((nickname, int(score)))

                                    # Sort the results by score
                                    results.sort(key=lambda x: x[1], reverse=True)

                                    # Determine the winner and display it
                                    if len(results) >= 2:
                                        if results[0][1] > results[1][1]:
                                            winner_nickname = results[0][0]
                                        else:
                                            winner_nickname = results[1][0]
                                    elif len(results) == 1:
                                        winner_nickname = results[0][0]
                                    else:
                                        winner_nickname = ""

                                  

                                    winner_bg_image = pygame.image.load("assets/winnerBg.jpg")
                                    winner_bg_image = pygame.transform.scale(winner_bg_image, (winner_bg_image.get_width() * 1.4, winner_bg_image.get_height() * 1.1))
                                    screen.blit(winner_bg_image, (0, 0))

                                    # Display the results on the screen
                                    y_position = 10
                                    for nickname, score in results:
                                        result_text = font_player.render(f"Nickname: {nickname}, has earned: {score}", True, WHITE)
                                        screen.blit(result_text, (30, y_position))
                                        y_position += 40

                                    # Display the winner
                                    winner_text = font_winner.render(f"The user {winner_nickname} has won", True, YELLOW)
                                    screen.blit(winner_text, (10, y_position))

                                    pygame.display.update()

                                    # Wait for a few seconds to display the results
                                    pygame.time.delay(5000)

                                    pygame.quit()


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

                                    # Display the type of question in console
                                    print("Type of question is: ", question)    

                                 
                                    options = question['options']
                                    correct_answer = question['answer']
                                    question_type = question['type']

                                    question_surface = font_question.render(question['question'].replace('&quot;', ' ').replace('&#039', ' ').replace(";s ", ' ').replace('&#039;', ' '), True, ORANGE)
                                    screen.blit(question_surface, (50, 100))


                                

                                    # Display the input field
                                    #pygame.draw.rect(screen, WHITE, input_rect, 2)
                                    input_surface = input_font.render(input_text, True, WHITE)
                                   
                        

                                  
                                    if question_type == 'multiple':
                                        option1_rect = pygame.Rect(100, 200, 200, 30)
                                        option1_text = font_answer.render(options[0].replace('&quot;', '"') if options else '', True, WHITE)
                                        option2_rect = pygame.Rect(400, 200, 200, 30)
                                        option2_text = font_answer.render(options[1].replace('&quot;', '"') if len(options) > 1 else '', True, WHITE)
                                        screen.blit(option1_text, (option1_rect.x, option1_rect.y + 5))
                                        screen.blit(option2_text, (option2_rect.x, option2_rect.y + 5))

                                        if len(options) > 2 and len(options) != 3:
                                            option3_rect = pygame.Rect(100, 300, 200, 30)
                                            option3_text = font_answer.render(options[2].replace('&quot;', '"'), True, WHITE)
                                            screen.blit(option3_text, (option3_rect.x, option3_rect.y + 5))

                                        # Clear the third option if len(options) == 3
                                        elif len(options) == 3:
                                            option3_rect = pygame.Rect(100, 300, 200, 30)
                                            option3_text = font_answer.render('', True, WHITE)
                                            screen.blit(option3_text, (option3_rect.x, option3_rect.y + 5))

                                        if len(options) > 3:
                                            option4_rect = pygame.Rect(400, 300, 200, 30)
                                            option4_text = font_answer.render(options[3].replace('&quot;', '"') if len(options) > 3 else '', True, WHITE)
                                            screen.blit(option4_text, (option4_rect.x, option4_rect.y + 5))


                                        # Clear the fourth and fifth options if len(options) > 5
                                        if len(options) == 5 and len(options) > 5:
                                            option5_text = font_answer.render('', True, WHITE)
                                            option6_text = font_answer.render('', True, WHITE)
                                            option7_text = font_answer.render('', True, WHITE)
                                            option5_rect = pygame.Rect(400, 300, 200, 30)
                                            option6_rect = pygame.Rect(400, 300, 200, 30)
                                            option7_rect = pygame.Rect(400, 300, 200, 30)
                                            screen.blit(option5_text, (option5_rect.x, option5_rect.y + 5))
                                            screen.blit(option6_text, (option6_rect.x, option6_rect.y + 5))
                                            screen.blit(option7_text, (option7_rect.x, option7_rect.y + 5))

                                    if question_type == 'input':
                                        #  Display the input field
                                    
                                        input_text = ''
                                        input_active = True
                                        active_input = None
                                        input_surface = popup_font.render('', True, WHITE)
                                        
                                    
                                        
                                    
                                        
                                        while input_active:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    input_active = False
                                                    input_text = ''

                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                    if input_rect.collidepoint(event.pos):
                                                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                                                        active_input = "input"

                                                    elif (enter_button.collidepoint(event.pos) or event.type == pygame.K_RETURN) and input_text:
                                                        if input_text == correct_answer:
                                                            correct_sound.play()
                                                            score += 10
                                                            input_active = False
                                                            input_text = ''
                                                            message = font_answer.render("Spravna odpoved!", True, GREEN)
                                                    
                                                            screen.blit(message, (300, 500))
                                                            
                                                            pygame.display.flip()
                                                            break

                                                        else:
                                                            wrong_sound.play()
                                                            input_active = False
                                                            message = font_answer.render("Nespravna odpoved!", True, RED)
                                                    
                                                            screen.blit(message, (300, 500))
                                                            input_text = ''
                                                        
                                                            pygame.display.flip()
                                                            break

                                                elif event.type == pygame.KEYDOWN:
                                                    if active_input == "input":
                                                    

                                                        if event.key == pygame.K_BACKSPACE:
                                                            input_text = input_text[:-1]
                                                            
                                                        elif event.unicode.isnumeric() or event.unicode in ['-', '.']:
                                                            input_text += event.unicode
                                                        else:
                                                            if len(input_text) < 35:
                                                                
                                                                input_text += event.unicode 
                                                        input_surface = input_font.render(input_text, True, WHITE)
                                                        
                                                        

                                            
                                            enter_button = pygame.Rect(300, 390, 100, 30)
                                            enter_text = font_input.render("Enter", True, WHITE)
                                            pygame.draw.rect(screen, input_color, enter_button, border_radius=10)
                                            screen.blit(enter_text, (313, 390))

                                    
                                            pygame.draw.rect(screen, BLUE, input_rect)
                                            input_surface = input_font.render(input_text, True, WHITE)
                                            # input_rect.width = max(input_surface.get_width() + 10, 100) 
                                            screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

                                            if input_surface.get_width() > input_rect.width - 10:
                                                input_rect.x = WIDTH // 2 - input_rect.width // 2
                                            else:
                                                input_rect.center = (WIDTH // 2, HEIGHT // 2)
                                            

                                            pygame.display.flip()
                                            clock.tick(60)

                                           

                                
  


                                    # Draw the arrow image
                                    arrow_rect = arrow.get_rect()
                                    arrow_rect.bottomright = screen.get_rect().bottomright
                                    screen.blit(arrow, arrow_rect)


                                    finish_rect = arrow.get_rect()
                                    finish_rect.topright = screen.get_rect().topright
                                    screen.blit(finish_text, finish_rect)

                                if question_type == 'multiple':
                                    if option1_rect.collidepoint(event.pos):
                                        selected_answer = options[0]
                                        
                                    elif option2_rect.collidepoint(event.pos):
                                        selected_answer = options[1]
                                        
                                    elif option3_rect.collidepoint(event.pos):
                                        selected_answer = options[2]
                                        
                                    elif option4_rect.collidepoint(event.pos):
                                        selected_answer = options[3]

                             
                                    

                                                                    
                                    
                                             
                        # Check if an option button was clicked or text was entered
                        if selected_answer:
                            # Check if the answer is correct
                            if selected_answer or input_text == correct_answer:
                                message = font_answer.render("Spravna odpoved!", True, GREEN)
                                screen.fill(BLACK, (300, 500, message.get_width(), message.get_height()))
                                screen.blit(message, (300, 500))
                                correct_sound.play()
                                print("Spravna odpoved")
                                score += 10
                                score_text = score_font.render("Score:" + str(score), True, YELLOW)

                                pygame.display.flip()
                                
                            else:
                                message = font_answer.render("Nespravna odpoved!", True, RED)
                                screen.fill(BLACK, (300, 500, message.get_width(), message.get_height()))
                                screen.blit(message, (300, 500))
                                wrong_sound.play()
                                print("Nespravna odpoved")
                                score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                pygame.display.flip()
                                
                        

                            

                            # Wait for a keypress to continue
                            waiting = True
                            answered = False

                            while waiting:
                                try: 
                                    for event in pygame.event.get():
                                                                  
                                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                            client.disconnect()
                                            pygame.quit()
                                            sys.exit()

                                        if event.type == pygame.MOUSEBUTTONDOWN and finish_rect.collidepoint(event.pos):
                                            nickname = client.nickname
                                            database.store_results(nickname, score)
                                            database.update_results(nickname, score)
                                            client.disconnect()

                                            results = []
                                            with open('results.txt', 'r') as f:
                                                for line in f:
                                                    if line.strip():
                                                        last_comma_index = line.rfind(', has earned: ')
                                                        if last_comma_index != -1:
                                                            nickname = line[:last_comma_index].strip()
                                                            score = line[last_comma_index + len(', has earned: '):].strip()
                                                            results.append((nickname, int(score)))

                                            # Sort the results by score
                                            results.sort(key=lambda x: x[1], reverse=True)

                                            # Determine the winner and display it
                                            if len(results) >= 2:
                                                if results[0][1] > results[1][1]:
                                                    winner_nickname = results[0][0]
                                                else:
                                                    winner_nickname = results[1][0]
                                            elif len(results) == 1:
                                                winner_nickname = results[0][0]
                                            else:
                                                winner_nickname = ""

                                            # # Create a socket connection to the server
                                            # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                            # server_address = ("localhost", 5555)
                                            # server_socket.connect(server_address)

                                            # Send the winner's nickname to the server
                                            # server_socket.send(f"Winner: {winner_nickname}".encode("utf-8"))

                                            # # Close the socket connection
                                            # server_socket.close()

                                            winner_bg_image = pygame.image.load("assets/winnerBg.jpg")
                                            winner_bg_image = pygame.transform.scale(winner_bg_image, (winner_bg_image.get_width() * 1.4, winner_bg_image.get_height() * 1.1))
                                            screen.blit(winner_bg_image, (0, 0))

                                            # Display the results on the screen
                                            y_position = 10
                                            for nickname, score in results:
                                                result_text = font_player.render(f"Nickname: {nickname}, has earned: {score}", True, WHITE)
                                                screen.blit(result_text, (30, y_position))
                                                y_position += 40

                                            # Display the winner
                                            winner_text = font_winner.render(f"The user {winner_nickname} has won", True, YELLOW)
                                            screen.blit(winner_text, (10, y_position))

                                            pygame.display.update()

                                            # Wait for a few seconds to display the results
                                            pygame.time.delay(5000)

                                            pygame.quit()


                                        if event.type == pygame.MOUSEBUTTONDOWN and arrow_rect.collidepoint(event.pos):

                                            
            
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

                                            # Display the type of question in console
                                            print("Type of question is: ", question)    

                                            
                                            options = question['options']
                                            correct_answer = question['answer']
                                            question_type = question['type']

                                            # Display the question and option buttons
                                            question_surface = font_question.render(question['question'].replace('&quot;', ' ').replace('&#039', ' ').replace(";s ", ' ').replace('&#039;', ' '), True, ORANGE)
                                            screen.blit(question_surface, (50, 100))

                                            

                                


                                            if question_type == 'multiple':
                                                option1_rect = pygame.Rect(100, 200, 200, 30)
                                                option1_text = font_answer.render(options[0].replace('&quot;', '"') if options else '', True, WHITE)
                                                option2_rect = pygame.Rect(400, 200, 200, 30)
                                                option2_text = font_answer.render(options[1].replace('&quot;', '"') if len(options) > 1 else '', True, WHITE)
                                                screen.blit(option1_text, (option1_rect.x, option1_rect.y + 5))
                                                screen.blit(option2_text, (option2_rect.x, option2_rect.y + 5))

                                                if len(options) > 2 and len(options) != 3:
                                                    option3_rect = pygame.Rect(100, 300, 200, 30)
                                                    option3_text = font_answer.render(options[2].replace('&quot;', '"'), True, WHITE)
                                                    screen.blit(option3_text, (option3_rect.x + 5, option3_rect.y + 5))

                                                # Clear the third option if len(options) == 3
                                                elif len(options) == 3:
                                                    option3_rect = pygame.Rect(100, 300, 200, 30)
                                                    option3_text = font_answer.render('', True, WHITE)
                                                    screen.blit(option3_text, (option3_rect.x, option3_rect.y + 5))

                                                if len(options) > 3:
                                                    option4_rect = pygame.Rect(400, 300, 200, 30)
                                                    option4_text = font_answer.render(options[3].replace('&quot;', '"') if len(options) > 3 else '', True, WHITE)
                                                    screen.blit(option4_text, (option4_rect.x, option4_rect.y + 5))


                                                # Clear the fourth and fifth options if len(options) > 5
                                                if len(options) == 5 and len(options) > 5:
                                                    option5_text = font_answer.render('', True, WHITE)
                                                    option6_text = font_answer.render('', True, WHITE)
                                                    option7_text = font_answer.render('', True, WHITE)
                                                    option5_rect = pygame.Rect(400, 300, 200, 30)
                                                    option6_rect = pygame.Rect(400, 300, 200, 30)
                                                    option7_rect = pygame.Rect(400, 300, 200, 30)
                                                    screen.blit(option5_text, (option5_rect.x + 5, option5_rect.y + 5))
                                                    screen.blit(option6_text, (option6_rect.x + 5, option6_rect.y + 5))
                                                    screen.blit(option7_text, (option7_rect.x + 5, option7_rect.y + 5))

                                                
                                                # Clear the fourth and fifth options if len(options) > 5
                                                if len(options) == 5 and len(options) > 5:
                                                    option5_text = font_answer.render('', True, WHITE)
                                                    option6_text = font_answer.render('', True, WHITE)
                                                    option7_text = font_answer.render('', True, WHITE)
                                                    option5_rect = pygame.Rect(400, 300, 200, 30)
                                                    option6_rect = pygame.Rect(400, 300, 200, 30)
                                                    option7_rect = pygame.Rect(400, 300, 200, 30)
                                                    screen.blit(option5_text, (option5_rect.x, option5_rect.y + 5))
                                                    screen.blit(option6_text, (option6_rect.x, option6_rect.y + 5))
                                                    screen.blit(option7_text, (option7_rect.x, option7_rect.y + 5))

                                                    
                                            if question_type == 'input':
                                                # Display the input field
                                            
                                                input_text = ''
                                                input_active = True
                                                active_input = None
                                                input_surface = popup_font.render('', True, WHITE)
                                                
                                            
                                                
                                            
                                                
                                                while input_active:
                                                    for event in pygame.event.get():
                                                        if event.type == pygame.QUIT:
                                                            input_active = False
                                                            

                                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                                            if input_rect.collidepoint(event.pos):
                                                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                                                                active_input = "input"

                                                            elif (enter_button.collidepoint(event.pos) or event.type == pygame.K_RETURN) and input_text:
                                                                if input_text == correct_answer:
                                                                    correct_sound.play()
                                                                    score += 10
                                                                    input_active = False
                                                                    input_text = ''
                                                                    message = font_answer.render("Spravna odpoved!", True, GREEN)
                                                            
                                                                    screen.blit(message, (300, 500))
                                                                    
                                                                    pygame.display.flip()
                                                                    break

                                                                else:
                                                                    wrong_sound.play()
                                                                    input_active = False
                                                                    message = font_answer.render("Nespravna odpoved!", True, RED)
                                                            
                                                                    screen.blit(message, (300, 500))
                                                                    input_text = ''
                                                                
                                                                    pygame.display.flip()
                                                                    break

                                                        elif event.type == pygame.KEYDOWN:
                                                            if active_input == "input":
                                                        

                                                                if event.key == pygame.K_BACKSPACE:
                                                                    input_text = input_text[:-1]
                                                                    
                                                                elif event.unicode.isnumeric() or event.unicode in ['-', '.']:
                                                                    input_text += event.unicode
                                                                else:
                                                                    if len(input_text) < 35:
                                                                        
                                                                        input_text += event.unicode    
                                                                input_surface = input_font.render(input_text, True, WHITE)
                                                            
                                                            
                                                                

                                                    
                                                    enter_button = pygame.Rect(300, 390, 100, 30)
                                                    enter_text = font_input.render("Enter", True, WHITE)
                                                    pygame.draw.rect(screen, input_color, enter_button, border_radius=10)
                                                    screen.blit(enter_text, (313, 390))

                                            
                                                    pygame.draw.rect(screen, BLUE, input_rect)
                                                    input_surface = input_font.render(input_text, True, WHITE)
                                                    # input_rect.width = max(input_surface.get_width() + 10, 100) 
                                                    screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

                                                    if input_surface.get_width() > input_rect.width - 10:
                                                        input_rect.x = WIDTH // 2 - input_rect.width // 2
                                                    else:
                                                        input_rect.center = (WIDTH // 2, HEIGHT // 2)
                                                    

                                                    pygame.display.flip()
                                                    clock.tick(60)

                                                


                                    
                                    
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
                                            
                                            if question_type == 'multiple':    
                                            
                                        
                                                if option1_rect.collidepoint(event.pos):
                                                    selected_answer = options[0]
                                                    
                                                elif option2_rect.collidepoint(event.pos):
                                                    selected_answer = options[1]
                                                    
                                                elif option3_rect.collidepoint(event.pos):
                                                    selected_answer = options[2]
                                                    
                                                elif option4_rect.collidepoint(event.pos):
                                                    selected_answer = options[3]

                                            

                                                                                    
                                                
                                            try:
                                                if selected_answer == correct_answer:
                                                    message = font_answer.render("Spravna odpoved!!!!", True, GREEN)
                                                    screen.fill(BLACK, (300, 500, message.get_width(), message.get_height()))
                                                    screen.blit(message, (300, 500))
                                                    correct_sound.play()
                                                    print("Spravna odpoved")
                                                    score += 10
                                                    score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                                    pygame.display.flip()
                                                else:
                                                    message = font_answer.render("Nespravna odpoved!", True, RED)
                                                    screen.fill(BLACK, (300, 500, message.get_width(), message.get_height()))
                                                    screen.blit(message, (300, 500))
                                                    wrong_sound.play()
                                                    print("Nespravna odpoved")
                                                    score_text = score_font.render("Score:" + str(score), True, YELLOW)
                                                    pygame.display.flip()
                                            except pygame.error as e:
                                                pass

                                    
                                    
                                        elif event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_SPACE:
                                                waiting = False
                                            
                                                pygame.display.flip() 
                                        
                            
                            
                    
                                           
                                            
                                except pygame.error as e:
                                    pass
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


# Quit Pygame
pygame.quit()


