import requests
import random

def get_questions_from_api(amount=50, category=None, difficulty=None, type="multiple"):
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
        
        for result in results:
            result['question'] = result['question'].replace('&quot;', '"').replace('&#039;', "'")
            if result['type'] == 'multiple':
                # Multiple Choice Question
               
                options = [option.replace('&quot;', '"').replace('&#039;', "'") for option in result['incorrect_answers']]
                options.append(result['correct_answer'].replace('&quot;', '"').replace('&#039;', "'"))
                random.shuffle(options)
                result['options'] = options
                result['correct_index'] = options.index(result['correct_answer'].replace('&quot;', '"').replace('&#039;', "'"))
            elif result['type'] == 'boolean':
                # True/False Question
               
                result['options'] = ['True', 'False']
                result['correct_index'] = 0 if result['correct_answer'] == 'True' else 1
            elif result['type'] == 'input':
                # Input Question

                result['options'] = []
                result['correct_index'] = 0
            else:
                print('Unknown question type')
               
        return results
    else:
        print('Error fetching questions from API')
        return []