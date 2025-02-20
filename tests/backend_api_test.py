import requests
import json
import uuid
import time


def test_send_message_to_chat():
    url = "https://chat.autofaq.ai/api/webhooks/widget/6c24eb52-b1ab-4d78-8463-8556d4ee04b3/messages"

    # Заголовки из curl
    headers = {
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://autofaq.ai",
        "Referer": "https://autofaq.ai/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "session-id": str(uuid.uuid4())
    }

    message_data = {
        "id": str(uuid.uuid4()),
        "ts": int(time.time() * 1000),
        "text": "Привет мир"
    }

    files = {
        'payload': (None, json.dumps(message_data), 'application/json')
    }

    try:
        response = requests.post(url, headers=headers, files=files)

        print(f"Статус код: {response.status_code}")
        print(f"Тело ответа: {response.text}")

        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

        response_data = response.json()
        print(f"JSON: {response_data}")

        return "Test passed successfully"

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return f"Test failed: {e}"
    except AssertionError as e:
        print(f"Assertion failed: {e}")
        return f"Test failed: {e}"


if __name__ == "__main__":
    result = test_send_message_to_chat()
    print(result)