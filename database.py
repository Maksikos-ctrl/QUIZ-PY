import sqlite3

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
    q = {'id': row[0], 'question': row[1], 'answer': row[2], 'type': row[3]}
    if row[4]:
        q['options'] = row[4].split(',')
    else:
        q['options'] = []
    return q




                