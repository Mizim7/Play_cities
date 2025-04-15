from flask import Flask, request, jsonify
import random

app = Flask(__name__)
cities = [
    {"name": "Москва", "image_id": "your_moscow_image_id"},
    {"name": "Нью-Йорк", "image_id": "your_ny_image_id"},
    {"name": "Париж", "image_id": "your_paris_image_id"}
]

# Состояния диалога
STATE_WELCOME = "welcome"
STATE_GUESS_CITY = "guess_city"


@app.route("/", methods=["POST"])
def main():
    data = request.json
    response = handle_request(data)
    return jsonify(response)


def handle_request(request):
    session_state = request.get("state", {}).get("session", {})
    state = session_state.get("state")
    if not state:
        return welcome_handler(request)
    elif state == STATE_WELCOME:
        return start_game_handler(request)
    elif state == STATE_GUESS_CITY:
        return guess_city_handler(request)


def welcome_handler(request):
    user_name = request["request"]["original_utterance"].lower()
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
    # Выбираем случайный город
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
                {"title": "Москва", "hide": True},
                {"title": "Нью-Йорк", "hide": True},
                {"title": "Париж", "hide": True},
                {"title": "Не знаю", "hide": True}
            ]
        },
        "session": {
            "session_state": session_state
        }
    }

    return response


def guess_city_handler(request):
    user_guess = request["request"]["original_utterance"].lower()
    correct_answer = request["state"]["session"]["selected_city"]
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
                {"title": "Да", "hide": True},
                {"title": "Нет", "hide": True}
            ]
        },
        "session": {
            "session_state": {}
        }
    }

    return response


if __name__ == "__main__":
    app.run(debug=True)
