import requests

def ask_ollama(question):
    url = 'http://localhost:11434/api/generate'

    data = {
        "model": "llama3",
        "prompt": question,
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Anfrage:", e)
        return None

if __name__ == "__main__":
    question = "Why is the sky blue?"
    answer = ask_ollama(question)
    if answer:
        print("Antwort:", answer['response'])
    else:
        print("Es gab ein Problem bei der Abfrage der Antwort.")
