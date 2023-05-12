import sqlite3
import os

def connect():
    conn = sqlite3.connect('questions.db')
    return conn


def insert_additional_questions(conn):
    sql = '''
    INSERT INTO questions (question, type, answer)
    VALUES 
        ('What does CPU stand for?', 'input', 'Central Processing Unit'),
        ('What does GPU stand for?', 'input', 'Graphics Processing Unit'),
        ('What does RAM stand for?', 'input', 'Random Access Memory'),
        ('What does PSU stand for?', 'input', 'Power Supply Unit'),
        ('What does HDD stand for?', 'input', 'Hard Disk Drive'),
        ('What does SSD stand for?', 'input', 'Solid State Drive'),
        ('What does VRAM stand for?', 'input', 'Video Random Access Memory'),
        ('What does USB stand for?', 'input', 'Universal Serial Bus'),
        ('What does HDMI stand for?', 'input', 'High-Definition Multimedia Interface'),
        ('What does DVI stand for?', 'input', 'Digital Visual Interface'),
        ('What does VGA stand for?', 'input', 'Video Graphics Array'),
        ('What does PCI stand for?', 'input', 'Peripheral Component Interconnect'),
        ('What does PCIe stand for?', 'input', 'Peripheral Component Interconnect Express'),
        ('What does SATA stand for?', 'input', 'Serial Advanced Technology Attachment'),
        ('What does ATX stand for?', 'input', 'Advanced Technology eXtended'),
        ('What does ITX stand for?', 'input', 'Information Technology eXtended'),
        ('What does BTX stand for?', 'input', 'Balanced Technology eXtended'),
        ('What does MATX stand for?', 'input', 'Micro Advanced Technology eXtended'),
        ('What does ATX stand for?', 'input', 'Advanced Technology eXtended'),
        ('What does ITX stand for?', 'input', 'Information Technology eXtended')
        
    '''
    c = conn.cursor()
    c.executescript(sql)
    conn.commit()


        


def create_questions_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       question TEXT,
                       answer TEXT,
                       type TEXT,
                       options TEXT)''')
    conn = cursor.connection
    # insert_additional_questions(conn)
    # clear_questions(conn)
   



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






                