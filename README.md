# TripSEA - See your dream trip come alive (CS50 2020 Project - capstone)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

TripSEA is a trip planning website that focuses on curating personalised trips to Southeast Asian countries for users whilst taking account of their interests and budget.
## Distinctiveness and Complexity
There are a few trip planning websites out there but they often provide poor suggestions
for trips involving Southeast Asian countries. This is because their data largely focuses on Western countries,
thus ignoring the diversity and beauty that Southeast Asia has to offer. Also, all these websites do not consider the user's budget when planning the trip, thus, suggesting places which might not suit their budget.

As such, TripSEA is trying to tackle a few problems:
- Promote tourism in Southeast Asian countries by suggesting places that locals would visit (including hidden gems!), thus curating a more authentic itinerary
- Planning a trip based on the user's interests (i.e. nature, cultural, adventurous, food, shopping, relaxing, romantic) and budget (i.e. budget, normal, luxury). Maximise the user's budget by giving them the highest reward possible.

Based on the problems that TripSEA is trying to solve and its unique selling point, it is clear that this website is completely distinct and has a different use case compared to the other
cs50 web projects done in this course (e.g. not trying to sell anything and does not have any
social aspect at all).
### Planning Algorithm
TripSEA utilises reinforcement learning algorithm (Q-learning algorithm) when planning the trip for the user. The algorithm focuses on maximising the reward for the user and the reward is calculated based on the user's inputs (interests and budget) and distance between attractions.

For example, a user who has a low budget and is interested in a cultural type of trip will have a customised itinerary that contains lots of museums / cultural atractions that are free / low ticket price. The algorithm will also consider the distance between attractions when planning the trip because more time saved in travelling will result in a higher user reward. Lastly, the algorithm will also try to suggest a dine in venue for the user and this is usually a venue that is highly recommended by locals.

### Database for Attractions and Dine In Venues
Currently, TripSEA only allows the user to plan a trip for Singapore (starting country). This is because the database currently only contain data for Singapore. The database is curated by scraping travel websites online (e.g. Timeout, toursim singapore website, food blogger website) to ensure that the places suggested by TripSEA are worth visiting. Note that the scraping code is not included under this repository. Scraping was done using Selenium and Beautifulsoup.

In the future, the scraping code will be used to scrap for places in other countries to expand the database
### Sleek UI and Good User Experience
Utilising Javascript and Bootstrap, the website provides the user with a modern look and easy to navigate user experience. The website is also mobile responsive. With a few clicks, the user can start to plan and review their dream trip.

If the user signs up an account, they can also view all their planned trips under 'View Profile'. TripSEA is designed to allow people to share their planned itinerary with friends and family. As such, they can share the itinerary with others (not required to sign up) by sending the link to the itinerary to them.

## File Structure
File structure of repository. Note: only important files / files created are shown in the tree.
```
│   db.sqlite3          :-> Sqlite Database storing all Django models
│   manage.py
│   README.md           :-> This file
│   requirements.txt    :-> Contains information of all dependencies
│
├───capstone
│
└───trip
    │   admin.py        :-> Admin interface to manage site content
    │   apps.py
    │   models.py       :-> All model classes in sqlite database are defined here
    │   planner.py      :-> Planning algorithm for itinerary
    │   tests.py
    │   urls.py         :-> URLs and API routes for website
    │   views.py        :-> API calls and http response calls. Login and logout calls
    │   __init__.py
    │
    ├───static
    │   └───trip
    │       │   home.js         :-> JS called by index.html
    │       │   itinerary.js    :-> JS called by itinerary and profile HTML
    │       │   start.js        :-> JS called by start.html
    │       │   styles.css      :-> Contains all CSS rules used in HTML files
    │       │
    │       └───images          :-> Stores all images used by the webpages
    │
    ├───templates
    │   └───trip                :-> Contains all HTML files
    │           index.html
    │           itinerary.html
    │           layout.html
    │           profile.html
    │           start.html
    │
    └───templatetags
            extra_tags.py       :-> Contain tags used in Django HTML templates
```
## Installation

Create a virtual python enviroment in your working directory using the following command
```
python -m venv <VENV_DIR>
```
Activate the virtual environment using the following command
```
<VENV_DIR>\Scripts\activate.bat
```
Change directory of your command window to the directory where this README.md is located.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependencies.
```
pip install -r requirements.txt
```

## Usage
Always start by activating your python virtual environment.
```
<VENV_DIR>\Scripts\activate.bat
```

To run Django server locally, use the command below
```
python manage.py runserver
```
Go to your web browser and visit the link below. You should see the homepage for the website.
```
http://127.0.0.1:8000/
```
Any changes made to trip/models.py requires you to run the following commands for the changes to take effect.
```
python manage.py makemigrations
```
```
python manage.py migrate
```
Please update the requirements.txt file if you add a new dependency for the project using the following command
```
pip freeze > requirements.txt
```

## Future Improvements
1. Move from Q-learning to Deep Q-learning. Currently, the algorithm is taking quite a bit of time to compute each itinerary. This is because it needs to re-train model due to changes in user variables. By moving to a deep q-learning algorithm, a few trained models might be sufficient (only need to be done once) and this will increase the efficiency. Furthermore, the suggested itinerary might be improved due to the better trained model,
2. Expand the database by including more countries.
3. Move from pure Javascript to React/ Node JS framework to build quality user interfaces.
4. Currently, the user tells the website their interests by selecting binary "Yes" or "No" options. Moving from boolean to a scoring system (1-10) will improve the planned trip. This also means using machine learning models to analyse each attraction for better classification. For example, a museum might have a very high 'cultural' score and also include some level of 'relaxing' score (as opposed to just yes or no).
5. As the user increases their utilisation of the website, the website can build a personalised profile based on their interests and trip preferences, thus creating a highly-curated trip based on collected data.

