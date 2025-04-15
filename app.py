import random

cities = [
    {"name": "Москва", "image_id": "1656841/c3c7c3d3ede5671fc7a8"},
    {"name": "Нью-Йорк", "image_id": "213044/c44387cecccecad7a422"},
    {"name": "Париж", "image_id": "213044/ea67dc347261060c471c"}
]

STATE_WELCOME = "welcome"
STATE_GUESS_CITY = "guess_city"


def handle_request(request):
    state = request["state"]["session_state"]
    if not state:
        return welcome_handler(request)
    elif state == STATE_WELCOME:
        return start_game_handler(request)
    elif state == STATE_GUESS_CITY:
        return guess_city_handler(request)


def welcome_handler(request):
    user_name = request["original_utterance"].lower()

    session_state = {
        "user_name": user_name,
        "state": STATE_WELCOME
    }

    response = {
        "response": {
            "text": f"Привет, {user_name}! Давай сыграем в игру «Угадай город». Я покажу фотографию города, "
                    f"а ты должен(а) угадать, какой это город.",
            "tts": f"Привет, {user_name}. Давай сыграем в игру «Угадай город». Я покажу фотографию города, "
                   f"а ты должен(а) угадать, какой это город."
        },
        "session": {
            "session_state": session_state
        }
    }

    return response


def start_game_handler(request):
    selected_city = random.choice(cities)
    session_state = {
        "selected_city": selected_city["name"],
        "image_id": selected_city["image_id"],
        "state": STATE_GUESS_CITY
    }

    response = {
        "response": {
            "text": "Вот фотография города. Какой это город?",
            "card": {
                "type": "BigImage",
                "image_id": selected_city["image_id"],
                "title": "Какой это город?"
            },
            "buttons": [
                "Москва",
                "Нью-Йорк",
                "Париж",
                "Не знаю"
            ]
        },
        "session": {
            "session_state": session_state
        }
    }

    return response


def guess_city_handler(request):
    user_guess = request["request"]["original_utterance"].lower()
    correct_answer = request["state"]["session_state"]["selected_city"]
    if user_guess in correct_answer.lower():
        response_text = f"Правильно! Это действительно {correct_answer}. Хочешь сыграть ещё раз?"
        tts_text = f"Правильно! Это действительно {correct_answer}. Хочешь сыграть ещё раз?"
    else:
        response_text = f"Неправильно. Это был {correct_answer}. Хочешь сыграть ещё раз?"
        tts_text = f"Неправильно. Это был {correct_answer}. Хочешь сыграть ещё раз?"

    response = {
        "response": {
            "text": response_text,
            "tts": tts_text,
            "buttons": [
                "Да",
                "Нет"
            ]
        },
        "session": {
            "session_state": {}
        }
    }

    return response


def main():
    import json
    import sys

    request = json.loads(sys.stdin.read())
    response = handle_request(request)
    print(json.dumps(response))


if __name__ == "__main__":
    main()
