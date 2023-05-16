# Trivia-titans

## Introduction

Trivia-titans is a trivia game built with Python. It allows multiple players to compete against each other by answering questions and earning points. The game includes various question types such as multiple-choice and true/false.

## Prerequisites

To use the program, you'll need to have Python 3.x installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

## Installation

1. Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/Maksikos-ctrl/SemestralnaPracaPython.git

2. Install the required packages using the command:

```bash
pip3 install -r requirements.txt
```


## Usage

To start the program, run the following command from the project directory in console:
```bash
python3 main.py
```

In a separate console window, run the following command to start the server:

```bash
python3 server.py
```


## Architecture
The Trivia-titans game is built with Python 3.x and utilizes the following files:

+ `server.py`: This is the module that contains the server class, which is responsible for running the server

+ `client.py`: This is the module that contains the client class, which is responsible for running the client

+ `database.py`: This is the module that contains the database class, which is responsible for connecting to the database and executing queries

+ `main.py`: This is the main module that contains the GamePlay class, which is responsible for running the program
+ `fonts.py`: This is the module that contains the fonts class, which is responsible for loading fonts

+ `colors.py`: This is the module that contains the colors class, which is responsible for loading colors

+ `questions.py`: This is the module that contains the questions class, which is responsible for loading questions from [Open TRIVIA API](https://opentdb.com/)

## How it looks like


![Screenshot 2023-05-16 124852](https://github.com/Maksikos-ctrl/SemestralnaPracaPython/assets/69985852/643f8117-8656-40c3-bd34-732f231bccdc)




## Conclusion
That's it! You now have a basic understanding of the Trivia-API codebase and how to contribute to the project.
