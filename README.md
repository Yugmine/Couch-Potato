# Hackathon info
Team name - Potato.io
Challenge - Terra API
Member Names + K-Numbers:
    - George Taylor 22028968
    - Hui Teo 22023030
    - Lewis Kai Ho Wong 22027157
    - Carlos De La Puente 21091485
Mentor Name + K-Number - N/A
Presentation - https://docs.google.com/presentation/d/1Yc3w6gsZ6pbFRRadhGciIVJqKOX11ST0yheup0g6eNA/edit?usp=sharing
Description - below

# Couch Potato
Project is a flask web server.

Web-based game where you grow potatoes with the calories you burn on Google Fit.
e.g. You get a potato that needs 180 kcal. If you burn that many calories, you harvest the potato.

To play the game:
 - Choose a username and write it in the text box. To access your game data in future you need to re-enter this username.
 - Click "Sign in with Google" and sign in.
 - You will get redirected to the game :)
 - The stats for a day are updated the next day (so running the game today will use calorie data from yesterday).

To run on your machine:
 - Locally create a keys.py file with API_KEY, DEV_ID and SECRET for Terra API.
 - flask and terra-python packages need to be installed with pip3.
 - Run main.py and connect to localhost:5000 in your web browser.

Requires Python 3