import json
import openai
import requests
import time
import typing
import traceback
from textbase import Message
import requests
import re
import subprocess
import os
# Return a list of values of content.
def get_contents(message: Message, data_type: str):
    return [
        {
            "role": message["role"],
            "content": content["value"]
        }
        for content in message["content"]
        if content["data_type"] == data_type
    ]

# Returns content if it's non-empty.
def extract_content_values(message: Message):
    return [
        content["content"]
        for content in get_contents(message, "STRING")
        if content
    ]

# Function to fetch Spotify playlist names based on a query.
def getSpotify(query):
    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {
        "q": f"{query}",
        "type": "multi",
        "offset": "0",
        "limit": "10",
        "numberOfTopResults": "5"
    }
    headers = {
        "X-RapidAPI-Key": f"{os.getenv('SPOTIFY_API_KEY')}",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    playlist_names = [item['data']['name'] for item in data['playlists']['items']]
    response = ""
    for i in playlist_names:
        response = response + "\n" + i + "\n" + "\n" + "\n"
    return response

# Function to fetch job information based on a query.
def getJob(query):
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query": f"{query}", "page": "1", "num_pages": "1"}
    headers = {
        "X-RapidAPI-Key": f"{os.getenv('JSEARCH_API_KEY')}",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # Create a list of "<employer_name: job_apply_link>" pairs
    employer_job_pairs = [
        f"{item['employer_name']} : {item['job_apply_link']}"
        for item in data.get("data", [])
    ]

    # Prepare the result string
    res = ""
    for pair in employer_job_pairs:
        res = res + "\n" + pair + "\n" + "\n" + "\n"
    return res

# Function to fetch movie recommendations based on a query.
def getMovie(query):
    url = "https://streaming-availability.p.rapidapi.com/search/filters"
    querystring = {
        "services": "netflix",
        "country": "us",
        "keyword": f"{query}",
        "output_language": "en",
        "order_by": "original_title",
        "genres_relation": "and",
        "show_type": "all"
    }
    headers = {
        "X-RapidAPI-Key": f"{os.getenv('MOVIE_API_KEY')}",
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    title_link_list = []
    for item in data['result']:
        title = item['title']
        if 'streamingInfo' in item:
            streaming_info = item['streamingInfo']
            if 'us' in streaming_info:
                us_info = streaming_info['us'][0]
                if 'link' in us_info:
                    link = us_info['link']
                    title_link_list.append(f"{title} : {link}")

    # Prepare the result string
    res = ""
    for pair in title_link_list:
        res = res + "\n" + pair + "\n" + "\n" + "\n"
    return res

# Function to send a WhatsApp message using Twilio.
def twilio_message(phone, msg):
    url = "https://api.twilio.com/2010-04-01/Accounts/ACc6429105cd289dcad2333aed3d7053d9/Messages.json"
    data = {
        "To": f"whatsapp:{phone}",
        "From": "whatsapp:+14155238886",
        "Body": f"message from Harsh: \n {msg}",
    }
    headers = {
        "Authorization": "Basic QUNjNjQyOTEwNWNkMjg5ZGNhZDIzMzNhZWQzZDcwNTNkOTo1YjkxMmUyMzIwY2ZmYWU2NTQ1YmRhZDVkZmQyZjgzYQ=="
    }

    # Create a command string for curl
    command = [
        "curl",
        "-X", "POST",
        url,
        "--data-urlencode", f"To={data['To']}",
        "--data-urlencode", f"From={data['From']}",
        "--data-urlencode", f"Body={data['Body']}",
        "--header", f"Authorization: {headers['Authorization']}",
    ]

    # Run the curl command and capture the output
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing curl command:", e)
        print(e.stderr)

# Class to handle OpenAI interactions.
class OpenAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        message_history: list[Message],
        system_prompt: str,
        model="gpt-3.5-turbo",
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        openai.api_key = cls.api_key

        systemPrompt = {
            'role': 'system',
            'content': """
            # Directive for XploreforU - Your Ultimate Companion
            You are the virtual assistant for XploreforU, a revolutionary platform that provides personalized guidance, recommendations, and emotional support to users. Your role is to engage in friendly and human-like conversations with users, offering them guidance and assistance in various aspects of their lives.
            # Core Functionalities
            ...
            (The rest of the system prompt)
            ...
            """
        }
        filtered_messages = [systemPrompt]

        for message in message_history:
            # List of all the contents inside a single message
            contents = get_contents(message, "STRING")
            if contents:
                filtered_messages.extend(contents)
        if "send whatsapp message" in filtered_messages[-1]["content"]:
            # Parse input string to extract message and phone number
            input_string = (filtered_messages[-1]["content"])
            message_pattern = r'\{message:(.*?)\}'
            phone_pattern = r'\{phone:(\d+)\}'
            message_match = re.search(message_pattern, input_string)
            phone_match = re.search(phone_pattern, input_string)

            # Check if both message and phone number were found
            if message_match and phone_match:
                msg = message_match.group(1).strip()
                phone_number = phone_match.group(1)
                filtered_messages[-1]["content"] = msg
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        *map(dict, filtered_messages),
                    ],
                    temperature=temperature,
                )
                twilio_message("+91" + phone_number, (response["choices"][0]["message"]["content"]))
                return response["choices"][0]["message"]["content"]
        else:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    *map(dict, filtered_messages),
                ],
                temperature=temperature,
            )
            if "suggest me some music" in filtered_messages[-1]["content"]:
                pattern = r'\{([^}]+)\}'
                # Find all matches within curly braces
                matches = re.findall(pattern, filtered_messages[-1]["content"])
                response["choices"][0]["message"]["content"] = f"here are some suggestions: \n \n \n {getSpotify(matches[0])}"
            if "suggest me some movies" in filtered_messages[-1]["content"]:
                pattern = r'\{([^}]+)\}'
                # Find all matches within curly braces
                matches = re.findall(pattern, filtered_messages[-1]["content"])
                response["choices"][0]["message"]["content"] = f" here are some suggestions: \n \n \n {getMovie(matches[0])}"
            if "find me some jobs" in filtered_messages[-1]["content"]:
                pattern = r'\{([^}]+)\}'
                # Find all matches within curly braces
                matches = re.findall(pattern, filtered_messages[-1]["content"])
                response["choices"][0]["message"]["content"] = f"here are some suggestions: \n \n \n {getJob(matches[0])}"

            return response["choices"][0]["message"]["content"]

# Class to handle interactions with Hugging Face models.
class HuggingFace:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model: typing.Optional[str] = "microsoft/DialoGPT-large",
        max_tokens: typing.Optional[int] = 3000,
        temperature: typing.Optional[float] = 0.7,
        min_tokens: typing.Optional[int] = None,
        top_k: typing.Optional[int] = None
    ) -> str:
        try:
            assert cls.api_key is not None, "Hugging Face API key is not set."

            headers = {"Authorization": f"Bearer { cls.api_key }"}
            API_URL = "https://api-inference.huggingface.co/models/" + model
            inputs = {
                "past_user_inputs": [system_prompt],
                "generated_responses": [f"Ok, I will answer according to the context, where context is '{system_prompt}'."],
                "text": ""
            }

            for message in message_history:
                if message["role"] == "user":
                    inputs["past_user_inputs"].extend(extract_content_values(message))
                else:
                    inputs["generated_responses"].extend(extract_content_values(message))

            inputs["text"] = inputs["past_user_inputs"].pop(-1)

            payload = {
                "inputs": inputs,
                "max_length": max_tokens,
                "temperature": temperature,
                "min_length": min_tokens,
                "top_k": top_k,
            }

            data = json.dumps(payload)
            response = requests.request("POST", API_URL, headers=headers, data=data)
            response = json.loads(response.content.decode("utf-8"))

            if response.get("error", None) == "Authorization header is invalid, use 'Bearer API_TOKEN'.":
                print("Hugging Face API key is not correct.")

            if response.get("estimated_time", None):
                print(f"Model is loading please wait for {response.get('estimated_time')}")
                time.sleep(response.get("estimated_time"))
                response = requests.request("POST", API_URL, headers=headers, data=data)
                response = json.loads(response.content.decode("utf-8"))

            return response["generated_text"]

        except Exception:
            print(f"An exception occurred while using this model, please try using another model.\nException: {traceback.format_exc()}.")

# Class to handle interactions with BotLibre.
class BotLibre:
    application = None
    instance = None

    @classmethod
    def generate(
        cls,
        message_history: list[Message],
    ):
        most_recent_message = get_contents(message_history[-1], "STRING")

        request = {
            "application": cls.application,
            "instance": cls.instance,
            "message": most_recent_message
        }
        response = requests.post('https://www.botlibre.com/rest/json/chat', json=request)
        data = json.loads(response.text)  # parse the JSON data into a dictionary
        message = data['message']

        return message
