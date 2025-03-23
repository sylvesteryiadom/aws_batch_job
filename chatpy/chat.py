import requests
import json
import os

def get_openai_api_key():
    """Retrieve the OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    return api_key

def send_message_to_chatgpt(prompt):
    """Send a message to the OpenAI ChatGPT API and return the response."""
    api_key = get_openai_api_key()
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",  # You can change this to the desired model
        "messages": [{"role": "developer", "content": prompt}],
        "max_completion_tokens": 3000,  # Adjust the response length as needed
        # "stream": True
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    
    return response.json()

def main():
    print("Welcome to the ChatGPT Interaction Script!")
    print("Type 'exit' to quit the program.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        try:
            response = send_message_to_chatgpt(user_input)
            chatgpt_response = response['choices'][0]['message']['content']
            highlighted_response = f"\033[1;32m{chatgpt_response}\033[0m"  # Green text
            # print(highlighted_response)
            print(f"ChatGPT: {highlighted_response}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


stKIHbZMjkpYXDTa6_B3taBuZgighNUuUOtoTDnkVcJfHTUOX9QC9QIF2Z7vOAVW3usMb26qT3BlbkFJyQGKN_nwBV-FHlEqsYcMf317rFbQ1XaIIHQJzOHzkQkxwC6Q_CrUU7zEErjvMr6LjUoB_yNh8A
