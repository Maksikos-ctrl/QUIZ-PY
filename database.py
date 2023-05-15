import sqlite3
import os

def connect():
    conn = sqlite3.connect('questions.db')
    return conn


def insert_additional_questions(conn):
    sql = '''
    INSERT INTO questions (question, type, answer)
    VALUES 
        ('What is the name of the computer that played Jeopardy?', 'input', 'Watson'),
        ('What is the name of the first computer?', 'input', 'ENIAC'),
        ('What is the name of the first computer programmer?', 'input', 'Ada Lovelace'),
        ('What is the name of the first computer virus?', 'input', 'Creeper'),
        ('What is the name of the first microprocessor?', 'input', 'Intel 4004'),
        ('What is the name of the first computer mouse?', 'input', 'Xerox Alto'),
        ('What is the name of the first computer game?', 'input', 'Spacewar!'),
        ('What is the name of the first computer bug?', 'input', 'Moth'),
        ('What is the name of the first computer hard disk?', 'input', 'IBM 350'),
        ('What is the name of the first computer modem?', 'input', 'Bell 101'),
        ('What is the name of the first computer network?', 'input', 'ARPANET'),
        ('What is the name of the first computer programming language?', 'input', 'Fortran'),
        ('What is the name of the first computer spreadsheet?', 'input', 'VisiCalc'),
        ('What is the name of the first computer word processor?', 'input', 'WordStar'),
        ('What is the name of the first computer operating system?', 'input', 'CTSS')
        
        
    '''
    c = conn.cursor()
    c.executescript(sql)
    conn.commit()


# def delete_additional_questions(conn):
#     sql = '''
#     DELETE FROM questions
#     WHERE question IN (
#         'What is the name of the computer that played Jeopardy?',
#         'What is the name of the first computer?',
#         'What is the name of the first computer programmer?',
#         'What is the name of the first computer virus?',
#         'What is the name of the first microprocessor?',
#         'What is the name of the first computer mouse?',
#         'What is the name of the first computer game?',
#         'What is the name of the first computer bug?',
#         'What is the name of the first computer hard disk?',
#         'What is the name of the first computer modem?',
#         'What is the name of the first computer network?',
#         'What is the name of the first computer programming language?',
#         'What is the name of the first computer spreadsheet?',
#         'What is the name of the first computer word processor?',
#         'What is the name of the first computer operating system?'
#     )
#     '''
#     c = conn.cursor()
#     c.executescript(sql)
#     conn.commit()

        


def create_questions_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       question TEXT,
                       answer TEXT,
                       type TEXT,
                       options TEXT)''')
    conn = cursor.connection
    # insert_additional_questions(conn)
    # delete_additional_questions(conn)
   



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
        options = ','.join(options)
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


def clear_questions(conn):
    c = conn.cursor()
    c.execute('DELETE FROM questions')
    conn.commit()






def store_results(nickname, score):
    with open('results.txt', 'a') as f:
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










                