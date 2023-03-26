import requests

def get_questions_from_api(amount=10, category=None, difficulty=None, type=None):
    url = 'https://opentdb.com/api.php?'
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
        return data['results']
    else:
        print('Error fetching questions from API')
        return []
