from flask import Flask, jsonify
import requests
import threading
import json

app = Flask(__name__)
window_size = 10
window = []
lock = threading.Lock()

test_server_url = 'http://20.244.56.144/test/'  
auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIxMTM4Njc5LCJpYXQiOjE3MjExMzgzNzksImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjA4ZTBmMjZhLTg2NTUtNDBhMS1hYjdlLWJhZmI4NGZhM2JjZCIsInN1YiI6IjEyNTE1ODA0NUBzYXN0cmEuYWMuaW4ifSwiY29tcGFueU5hbWUiOiJTQVNUUkEiLCJjbGllbnRJRCI6IjA4ZTBmMjZhLTg2NTUtNDBhMS1hYjdlLWJhZmI4NGZhM2JjZCIsImNsaWVudFNlY3JldCI6IkFFb0NuRHNvd2lya1dCQU4iLCJvd25lck5hbWUiOiJQcmFkaHl1bW5hIiwib3duZXJFbWFpbCI6IjEyNTE1ODA0NUBzYXN0cmEuYWMuaW4iLCJyb2xsTm8iOiIxMjUxNTgwNDUifQ.saSBVehwjfTiqRnUCZpaevYP6RB7H281DSgZc312XhI"

headers = {
    "Authorization": f"Bearer {auth_token}"
}
auth_json={
    "companyName": "SASTRA",
    "clientID": "08e0f26a-8655-40a1-ab7e-bafb84fa3bcd",
    "clientSecret": "AEoCnDsowirkWBAN",
    "ownerName": "Pradhyumna",
    "ownerEmail": "125158045@sastra.ac.in",
    "rollNo": "125158045"
}


def fetch_numbers_from_server(number_id):
    try:
        
        response = requests.get(f'{test_server_url}{number_id}', headers=headers, timeout=0.5)
        response.raise_for_status()
        print(response)
        numbers=response.json()
        return numbers['numbers']
    except requests.RequestException:
        return []

def update_window(new_numbers):
    global window
    with lock:
        window.extend(new_numbers)
        window = list(set(window))  
        if len(window) > window_size:
            window = window[-window_size:]

@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    valid_ids = ['p', 'f', 'e', 'r']
    valid_url={'p':'primes','f':'fibo','e':'even','r':'random'}
    if number_id not in valid_ids:
        return jsonify({"error": "Invalid number ID"}), 400

    new_numbers = fetch_numbers_from_server(valid_url[number_id])
    prev_state = list(window)
    update_window(new_numbers)
    curr_state = list(window)
    print(curr_state)
    print(prev_state)
    avg = sum(curr_state) / len(curr_state) if curr_state else 0

    response = {
        "numbers": new_numbers,
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "avg": round(avg, 2)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876,debug=True, threaded=True)
