import sqlite3
import os
# import psycopg2
# from psycopg2.extras import RealDictCursor

def connect():
    conn = sqlite3.connect('questions.db')
    return conn


def create_questions_table(cursor):
     cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       question TEXT,
                       answer TEXT,
                       type TEXT,
                       options TEXT)''')
     

def create_scores_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nickname TEXT,
                       score INTEGER)''')


def add_questions(conn, question, correct_answer, *options):
    c = conn.cursor()
    if options:
        options = list(options)
        options.append(correct_answer)
        options = ','.join(options + [correct_answer])
    else:
        options = ''
    c.execute('''INSERT INTO questions
                (question, answer, type, options)
                VALUES (?, ?, ?, ?)''',
            (question, correct_answer, 'multiple', options))
    conn.commit()


def add_score(conn, nickname, score):
    c = conn.cursor()
    c.execute('''INSERT INTO scores
                (nickname, score)
                VALUES (?, ?)''',
            (nickname, score))
    conn.commit()    


def get_questions(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    rows = c.fetchall()
    questions = []
    for row in rows:
        q = {'id': row[0], 'question': row[1], 'answer': row[2], 'type': row[3]}
        if row[4]:
            q['options'] = row[4].split(',')
        else:
            q['options'] = []
        questions.append(q)
    return questions


def get_random_question(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    row = c.fetchone()
    if row:
        q = {'id': row[0], 'question': row[1], 'answer': row[2], 'type': row[3]}
        if row[4]:
            q['options'] = row[4].split(',')
        else:
            q['options'] = []
        return q
    else:
        return None
    

def clear_questions(conn):
    c = conn.cursor()
    c.execute('DELETE FROM questions')
    conn.commit()


def store_results(nickname, score):
    with open ('results.txt', 'a') as f:
        f.write(f'Nickname: {nickname}, has earned: {score}\n')  


def update_results(nickname, score):
    file_exists = os.path.isfile('results.txt')
    
    if not file_exists:
        store_results(nickname, score)
        return

    with open('results.txt', 'r') as file:
        lines = file.readlines()

    found = False
    with open('results.txt', 'w') as file:
        for line in lines:
            if f'Nickname: {nickname},' in line:
                line = f'Nickname: {nickname}, has earned: {score}\n'
                found = True
            file.write(line)

    if not found:
        store_results(nickname, score)






# PostgreSQL database functions

# def connect_postgresql():
#     conn = psycopg2.connect(
#         host="",
#         database="your_database",
#         user="your_username",
#         password="maksikos973"
#     )
#     return conn

# def create_scores_table(cursor):
#     cursor.execute('''CREATE TABLE IF NOT EXISTS scores
#                       (id SERIAL PRIMARY KEY,
#                        name TEXT,
#                        score INTEGER)''')

# def add_score_postgresql(conn, name, score):
#     c = conn.cursor(cursor_factory=RealDictCursor)
#     c.execute('''INSERT INTO scores
#                 (name, score)
#                 VALUES (%s, %s)''',
#               (name, score))
#     conn.commit()


# def get_top_scores_postgresql(conn, limit=10):
#     c = conn.cursor(cursor_factory=RealDictCursor)
#     c.execute('SELECT name, score FROM scores ORDER BY score DESC LIMIT %s', (limit,))
#     return c.fetchall()





                