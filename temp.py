from flask import Flask, Response
import requests

app = Flask(__name__)


def chat(message: str):
    url = "http://danto.cloud:12138/api/chat"
    headers = {"Content-Type": "application/json"}

    data = {
        'message': message,
        'apiKey': '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'
    }

    def generate():
        response = requests.post(url, headers=headers, json=data, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            yield chunk.decode()

    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    print(chat("hello"))
