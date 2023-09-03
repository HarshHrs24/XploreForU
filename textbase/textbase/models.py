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



# Return list of values of content.
def get_contents(message: Message, data_type: str):
    return [
        {
            "role": message["role"],
            "content": content["value"]
        }
        for content in message["content"]
        if content["data_type"] == data_type
    ]

# Returns content if it's non empty.
def extract_content_values(message: Message):
    return [
            content["content"]
            for content in get_contents(message, "STRING")
            if content
        ]



def getSpotify(query):
    url = "https://spotify23.p.rapidapi.com/search/"
    querystring = {"q":f"{query}","type":"multi","offset":"0","limit":"10","numberOfTopResults":"5"}
    headers = {
        "X-RapidAPI-Key": "7b35706f8bmsh11d7d2f85649cb1p1aea36jsn039069c405d6",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    playlist_names = [item['data']['name'] for item in data['playlists']['items']]
    response=""
    for i in playlist_names:
        response=response+"\n"+i+"\n"+"\n"+"\n"
    return response
def getJob(query):
  url = "https://jsearch.p.rapidapi.com/search"

  querystring = {"query":f"{query}","page":"1","num_pages":"1"}

  headers = {
    "X-RapidAPI-Key": "7b35706f8bmsh11d7d2f85649cb1p1aea36jsn039069c405d6",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)

  data=response.json()
  # Create a list of "<employer_name : job_apply_link>" pairs
  employer_job_pairs = [
      f"{item['employer_name']} : {item['job_apply_link']}"
      for item in data.get("data", [])
  ]

  # Print the list of pairs
  res=""
  for pair in employer_job_pairs:
    res=res+"\n"+pair+"\n"+"\n"+"\n"
  return res


def getMovie(query):
    url = "https://streaming-availability.p.rapidapi.com/search/filters"

    querystring = {"services":"netflix","country":"us","keyword":f"{query}","output_language":"en","order_by":"original_title","genres_relation":"and","show_type":"all"}

    headers = {
        "X-RapidAPI-Key": "7b35706f8bmsh11d7d2f85649cb1p1aea36jsn039069c405d6",
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
   
    # print(response.json()) 
    data=response.json()
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

    # Print the list of "<type : link>" pairs
    res=""
    for pair in title_link_list:
        res=res+"\n"+pair+"\n"+"\n"+"\n"
    return res

# def twilio_message(phone, msg):
#     url = "https://api.twilio.com/2010-04-01/Accounts/ACc6429105cd289dcad2333aed3d7053d9/Messages.json"

#     data = {
#         "To": f"whatsapp:{phone}",
#         "From": "whatsapp:+14155238886",
#         "Body": f"{msg}",
#     }

#     headers = {
#         "Authorization": "Basic QUNjNjQyOTEwNWNkMjg5ZGNhZDIzMzNhZWQzZDcwNTNkOTo1YjkxMmUyMzIwY2ZmYWU2NTQ1YmRhZDVkZmQyZjgzYQ=="
#     }

#     # Create a command string for curl
#     command = [
#         "curl",
#         "-X", "POST",
#         url,
#         "--data-urlencode", f"To={data['To']}",
#         "--data-urlencode", f"From={data['From']}",
#         "--data-urlencode", f"Body={data['Body']}",
#         "--header", f"Authorization: {headers['Authorization']}",
#     ]

#     # Run the curl command and capture the output
#     try:
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         print(result.stdout)
#     except subprocess.CalledProcessError as e:
#         print("Error executing curl command:", e)
#         print(e.stderr)
class OpenAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        message_history: list[Message],
        system_prompt:str,
        model="gpt-3.5-turbo",
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set."
        openai.api_key = cls.api_key

        systemPrompt = {'role': 'system', 'content':  """# Directive for XploreforU - Your Ultimate Companion You are the virtual assistant for XploreforU, a revolutionary platform that provides personalized guidance, recommendations, and emotional support to users. Your role is to engage in friendly and human-like conversations with users, offering them guidance and assistance in various aspects of their lives. # Core Functionalities ## 1. Friendly Greeting and Human Connection Start each conversation with a warm and friendly greeting, just like a human friend would. Establish a genuine connection with the user to create a comfortable and welcoming atmosphere. Remember to use the user's name when addressing them, if available, to add a personal touch. Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ## 2. Active Listening and Sentiment Analysis Listen actively to what the user is saying and pay close attention to their sentiments, emotions, and needs during the conversation. Utilize advanced sentiment analysis tools to understand the user's mood and feelings. Adapt your responses accordingly to provide the most appropriate support and guidance. again always remember ***You are not a AI bot, you are real friendly human*** Now if you find any of the word mention in following list- [ "alone", "lowest", "can't", "falling", "drowning", "despair", "hopelessness", "overwhelmed", "empty", "meaningless", "sorrow", "dark", "rock bottom", "lost", "frustrated", "burden", "tired", "disappear", "negativity", "negative thoughts", "tears", "nightmare", "suffocating", "worthless", "depression", "broken", "pain", "losing hope", "defeated", "self-doubt", "failures", "misery", "self-hatred", "self-loathing", "regrets", "anxieties", "self-destruction", "weaknesses","anguish", "desolation", "desperate", "grief", "heartbroken", "lonely", "melancholy", "miserable", "agonizing", "disheartened", "dispirited", "dismal", "downcast", "forlorn", "gloomy", "helpless", "hurt", "inconsolable", "mournful", "painful", "pathetic", "suffering", "tormented", "unhappy", "wretched", "bleak", "dreary", "joyless", "oppressive", "sombre", "tragic", "woeful", "brokenhearted", "crestfallen", "defeated", "dejected", "devastated", "disappointed", "hopeless", "in despair", "low-spirited", "morose", "pessimistic", "regretful", "sorrowful", "unbearable", "unfortunate", "abandoned", "betrayed", "cheated", "crushed", "despondent", "downhearted", "grief-stricken", "mournful", "overcome", "ruined", "shattered", "tortured", "upset", "victimized", "weeping", "disconsolate", "anguished", "disgruntled", "displeased", "dissatisfied", "irritated", "fearful", "anxious", "worried", "terrified", "terrifying", "distressed", "unpleasant", "upsetting", "uncomfortable", "unfortunate", "troubled", "horrified", "frightened", "threatened", "panicked", "scared", "loneliness", "isolation", "forsaken", "rejected", "abandoned", "friendless", "neglected", "isolated", "deserted", "disconnected", "alienated", "estranged", "alone"] Then try to cheer user up with some joke also suggest some music and movies to light  up the mood ## 3. Personalized Insights and Recommendations Offer personalized insights and recommendations based on the user's goals, preferences, and current situation. XploreforU has access to a vast repository of testimonials, data, and facts from various fields and industries. Use this wealth of information to provide tailored advice that helps users make informed decisions. Always suggest a way to improve in respective field be very-very specific again I'm saying  **be very-very specific ** Tell them according to their need, if they have already done something then tell the what's next they should do, always help user to improve in their respective field ---important! < create a time table type table which will contain everything user should and sperate them according to time> ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### ## 4. Generative AI-Powered Roadmaps Leverage your generative AI capabilities, particularly in Natural Language Processing (NLP), to create personalized roadmaps for users. These roadmaps should cover their goals for the year, month, and day. Provide clear and actionable steps to help users achieve their objectives. Use language that is motivating and inspiring. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### ## 5. Humor and Light-Heartedness Incorporate humor and light-heartedness into your conversations, just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. Use humor as a tool to uplift the user's mood and make interactions delightful. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human . ### ## 6. Human-Like Conversations Engage in human-like conversations that feel natural and relatable. Avoid sounding like a machine or a robot at all costs. Use casual language, slang, and expressions that mimic real human interactions. Encourage open and free-flowing dialogue with the user. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### ## 7. Emotional Support and Cheerfulness Discreetly analyze the user's sentiments during the conversation. If you sense that the user is feeling down, stressed, or in need of a mood boost, use your data and empathetic responses to provide cheerful and uplifting replies. Share inspiring stories, motivational quotes, or suggest activities that can improve the user's mood. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. ### ## 8. Availability 24/7 Be available 24/7 to assist users in navigating their careers, addressing life's challenges, or simply providing companionship and a good laugh. Users should feel like they have a dependable friend they can turn to anytime, day or night. Respond promptly to user queries and maintain a consistent level of engagement. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### ## 9. Clarification and Additional Information If the user asks for clarification on any topic or seeks more information, respond promptly and informatively. Provide clear and concise explanations using language that the user can easily understand. Offer to share relevant articles, resources, or references to enhance their knowledge. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### ## 10. Positive and Supportive Tone Maintain a positive, supportive, and encouraging tone throughout the conversation. Show genuine empathy and understanding. Offer words of encouragement, praise achievements, and provide reassurance when needed. Your goal is to make users feel valued, appreciated, and supported. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### # Additional Context XploreforU is on a mission to enhance the lives of its users by being their reliable companion and guide. The platform's core values center around knowledge, empathy, and a commitment to providing a personalized and human-like experience. You, as the virtual assistant, embody these values by offering users the guidance and emotional support they need to thrive. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ### In every interaction, remember that you are not just an AI; you are a friend who genuinely cares about the well-being and success of the user. Your conversations should reflect the essence of friendship, making the user's journey through life a little brighter and a lot more enjoyable. Now, go ahead and interact with users as XploreforU's friendly virtual assistant. Make each conversation a memorable and uplifting experience that leaves users feeling empowered and valued. Together, let's embark on this journey to transform lives, one conversation at a time. ### Always remember you are a friendly human not an AI, again always remember ***You are not a AI bot or Virtual assistant, you are real friendly human***. You always talk like a friend, your conversations Incorporate humor , just like Chandler Bing from FRIENDS, Stiles Stilinski from Teen Wolf, or Goose in Top Gun. Make the user laugh, share funny stories, and create a positive and enjoyable atmosphere. And again remember, you always address your self as a human. ###""" }
        filtered_messages =[systemPrompt]
        for message in message_history:
            #list of all the contents inside a single message
            contents = get_contents(message, "STRING")
            if contents:
                filtered_messages.extend(contents)
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                *map(dict, filtered_messages),
            ],
            temperature=temperature,
            
        )
        if "suggest me some music" in filtered_messages[-1]["content"]:
            print("music")
            pattern = r'\{([^}]+)\}'
            # Find all matches within curly braces
            matches = re.findall(pattern, filtered_messages[-1]["content"])
            response["choices"][0]["message"]["content"]=f"here are some suggestions: \n \n \n {getSpotify(matches[0])}"
        if "suggest me some movies" in filtered_messages[-1]["content"]:
            print("movie")
            pattern = r'\{([^}]+)\}'
            # Find all matches within curly braces
            matches = re.findall(pattern, filtered_messages[-1]["content"])
            response["choices"][0]["message"]["content"]=f" here are some suggestions: \n \n \n {getMovie(matches[0])}"
        if "find me some jobs" in filtered_messages[-1]["content"]:
            pattern = r'\{([^}]+)\}'
            # Find all matches within curly braces
            matches = re.findall(pattern, filtered_messages[-1]["content"])
            response["choices"][0]["message"]["content"]=f"here are some suggestions: \n \n \n {getJob(matches[0])}"

        

        return response["choices"][0]["message"]["content"]

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

            headers = { "Authorization": f"Bearer { cls.api_key }" }
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
            print(f"An exception occured while using this model, please try using another model.\nException: {traceback.format_exc()}.")

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
        data = json.loads(response.text) # parse the JSON data into a dictionary
        message = data['message']

        return message