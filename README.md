
<strong>Mercor Textbase Hackathon</strong>
  </p>

<img src="https://drive.google.com/uc?export=view&id=1xNVxuJEd7UyIuy-8lwgbUV4GQRTTWQ2F" alt=" " width="1010" height="100">

<a name="readme-top"></a>
<!--
***  Textbase Tiatans

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/HarshHrs24/Team-cl_AI_mate"></a>

  <img src="https://drive.google.com/uc?export=view&id=1eISmQoJ9JYrpczM67SNHTP75aWQ5THT8" alt="Logo" width="110" height="110">

    
  <h3 align="center">XploreForU</h3>

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
     <li>
      <a href="#problem-statement">Problem Statement</a>
    </li>
      <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#features">Features</a></li>
     <li><a href="#screenshots">Screenshots</a></li>
    <li><a href="#our-approach">Our Approach</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#made-by">Made by</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>




# Problem Statement
<strong>Track 1: Chatbot Development & Deployment</strong>
<br>
Prompt – Construct a chatbot that fulfills real-user needs. In this hackathon, we urge participants to unleash their imagination to its fullest. Alongside leveraging features such as GPT's function calling to elevate your chatbot beyond typical conversation models, we've introduced a new deployment dashboard. This feature streamlines the process, allowing you to deploy your creations with ease. Push the boundaries of innovation and utility!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT THE PROJECT -->
# About The Project

Introducing XploreForU - Your Ultimate Companion and Guide

Have you ever wished for a trustworthy friend and guide to accompany you through life's twists and turns? Enter XploreForU, a groundbreaking platform that's here to transform your journey. We understand the challenges of navigating life's decisions, and our virtual assistant is your constant companion, offering personalized insights, jokes to brighten your day, and even the latest music, movies, and job openings tailored to your preferences. With real-time data from API services, we're always up-to-date, ensuring you have the support and information you need to thrive. Embrace a new way of living and explore endless possibilities with XploreForU.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Features -->
## Features
* <strong>Mental health assistant</strong>
  <br>
  Human-Like Conversations: No more robotic responses! XploreforU has been trained to speak like a human, with all the quirks and idiosyncrasies that come with it. It's not just about providing information;     it's about creating a genuine connection. We're talking laughter, banter, and even poking a little fun at you (in good spirits, of course) to brighten your day.
* <strong>Job search</strong>
  <br>
  Our chatbot is a game-changer when it comes to job hunting. By utilizing Rapid API(JSearch by By OpenWeb Ninja), it connects users to an extensive database of job listings from various sources. This means that job seekers can find the most up-to-date job opportunities in their desired field, ensuring they never miss out on promising career prospects.
* <strong>Song search</strong>
  <br>
  Music enthusiasts will appreciate our chatbot's ability to fetch the latest songs and lyrics. With Rapid API integration(Spotify by By Glavier), it pulls data from multiple music databases, including current charts, top tracks, and artist information. Users can enjoy the freshest tunes and discover new music as soon as it's released.
* <strong>Movie search</strong>
  <br>
  Movie buffs can rely on our chatbot for the most current information about films. Thanks to Rapid API(Streaming Availability by By Movie of the Night), our chatbot taps into a vast movie database to provide real-time details about the latest releases, showtimes, reviews, and more. Users can make informed decisions about what to watch, ensuring they stay in the cinematic loop.
* <strong>Twilio message system</strong>
  <br>
Our chatbot is not just about data retrieval; it also facilitates communication. With the Twilio message system integration, users can send and receive SMS messages directly through the chatbot. Whether it's sending notifications, reminders, or engaging in two-way conversations, your chatbot empowers users with a versatile communication tool.
  
    
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Installation
### 1. Clone the repository or download the zip file in your machine.
Make sure you have `python version >=3.9.0`, it's always good to follow the [docs](https://docs.textbase.ai/get-started/installation) 👈🏻
### 2. Through pip
```bash
pip install textbase-client
```

### 3. Local installation
Clone the repository and install the dependencies using [Poetry](https://python-poetry.org/) (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

For proper details see [here]()

```bash
git clone https://github.com/cofactoryai/textbase
cd textbase
poetry shell
poetry install
```

### Start development server

> If you're using the default template, **remember to set the OpenAI API key** in `main.py and respective **Rapid API key** (mentioned in <a href="#features">Features</a> section) in model.py file.

Run the following command:
- if installed locally
    ```bash
    poetry run python textbase/textbase_cli.py test
    ```
- if installed through pip
    ```bash
    textbase-client test
    ```
Response:
```bash
Path to the main.py file: examples/openai-bot/main.py # You can create a main.py by yourself and add that path here. NOTE: The path should not be in quotes
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Screenshots 
## Your Friendly Chatbot/Mental Health Assistant
<img src="https://drive.google.com/uc?export=view&id=1T4R_xbzrX7jUPndjmiNUTNGyP8iiQSXV" alt="Click and Reload" width="400" height="200"><img src="https://drive.google.com/uc?export=view&id=1nh2uMTr0eqifTH8wIht1OQZD9jDq5Joq" alt="Click and Reload" width="400" height="200">

<img src="https://drive.google.com/uc?export=view&id=1ZJmE8g0tg-VFMpJw3iaKSLS3s7DOkh72" alt="Click and Reload" width="400" height="200">

## Job Search
<img src="https://drive.google.com/uc?export=view&id=1SJC8PwyaVX_1RcGDfyMn-RK9gsMm_Vzu" alt="Click and Reload" width="400" height="200">

## Movie Search
<img src="https://drive.google.com/uc?export=view&id=1o0Iego0lsAimp_R_bkPdpsoop4awshW0" alt="Click and Reload" width="400" height="200">

## Music Search
<img src="https://drive.google.com/uc?export=view&id=13HZasg2qIx79IkPJZpEavbyjnNmNTVBv" alt="Click and Reload" width="400" height="200">

## Twilio message system
<img src="https://github.com/HarshHrs24/XploreForU/assets/107180900/a95f89a7-21fc-4cce-a82b-e13f01ae8f53" alt="Click and Reload" width="400" height="200">


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Approach -->
## Our Approach

In our approach, we've leveraged the power of the Textbase framework to create a versatile and dynamic virtual assistant, powered by cutting-edge technologies and a user-centric design philosophy. This virtual companion, XploreForU, is more than just a digital assistant; it's your friend, guide, and source of constant support throughout your journey.

Our secret sauce lies in the integration of various APIs to provide real-time and up-to-date information. Whether you're looking for music recommendations, the latest movies, or job openings tailored to your role, XploreForU has got you covered. We leverage Spotify, streaming-availability, and jsearch APIs to ensure you always receive the most relevant and current suggestions.

But what truly sets us apart is our commitment to personalized interactions. With OpenAI's powerful language model at its core, XploreForU engages in friendly and human-like conversations, offering emotional support, guidance, and even the ability to send heartfelt messages to your friends via Twilio integration.

In a world filled with uncertainty, XploreForU is your constant companion, ready to assist you in making informed decisions and keeping you on the right track. Say goodbye to the "what ifs" in life, and embrace a brighter future with XploreForU by your side.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Features -->
## Features
* <strong>Mental health assistant</strong>
  <br>
  Human-Like Conversations: No more robotic responses! XploreforU has been trained to speak like a human, with all the quirks and idiosyncrasies that come with it. It's not just about providing information;     it's about creating a genuine connection. We're talking laughter, banter, and even poking a little fun at you (in good spirits, of course) to brighten your day.
* <strong>Job search</strong>
  <br>
  Our chatbot is a game-changer when it comes to job hunting. By utilizing Rapid API(JSearch by By OpenWeb Ninja), it connects users to an extensive database of job listings from various sources. This means that job seekers can find the most up-to-date job opportunities in their desired field, ensuring they never miss out on promising career prospects.
* <strong>Song search</strong>
  <br>
  Music enthusiasts will appreciate our chatbot's ability to fetch the latest songs and lyrics. With Rapid API integration(Spotify by By Glavier), it pulls data from multiple music databases, including current charts, top tracks, and artist information. Users can enjoy the freshest tunes and discover new music as soon as it's released.
* <strong>Movie search</strong>
  <br>
  Movie buffs can rely on our chatbot for the most current information about films. Thanks to Rapid API(Streaming Availability by By Movie of the Night), our chatbot taps into a vast movie database to provide real-time details about the latest releases, showtimes, reviews, and more. Users can make informed decisions about what to watch, ensuring they stay in the cinematic loop.
* <strong>Twilio message system</strong>
  <br>
Our chatbot is not just about data retrieval; it also facilitates communication. With the Twilio message system integration, users can send and receive SMS messages directly through the chatbot. Whether it's sending notifications, reminders, or engaging in two-way conversations, your chatbot empowers users with a versatile communication tool.
  
    
<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Built With

### Technology Used                                                                  
* Python
* Twilio
* Textbase
* OpenAI
* Rapid API
* GPT 3.5 Turbo
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Made by

[Harsh Soni](https://github.com/HarshHrs24)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
[Mercor](https://work.mercor.io/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>
