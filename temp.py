import requests

def chat(message: str):
    url = "http://danto.cloud:12138/api/chat"
    headers = {"Content-Type": "application/json"}

    data = {
        'message': message,
        'apiKey': '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'
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    # return response.raw.read(), response.status_code, response.headers.items()
    
    print(response.json())
    
    return data


if __name__ == '__main__':
    chat('hello')