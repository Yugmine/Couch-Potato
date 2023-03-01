from flask import Flask, render_template, redirect, request, session
from terra.base_client import Terra
from datetime import timedelta, date, datetime
import keys
import random
import json


#terra setup
terra = Terra(api_key=keys.API_KEY, dev_id=keys.DEV_ID, secret=keys.SECRET)

with open('user_potatoes.json') as f:
    user_potatoes = json.load(f)
# {
#   username: {
#       potatoes: [126, 180],
#       current_potato: 161,
#       current_progress: 80,
#       potatoes_harvested: 43,
#       last_upload: datetime
#   }
# }

#flask pages
app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    api_response = terra.generate_authentication_url(resource="GOOGLE", auth_success_redirect_url="http://localhost:5000/home", auth_failure_redirect_url="http://localhost:5000/login_fail", reference_id=username)
    return redirect(api_response.get_json()['auth_url'])

@app.route("/home")
def home():
    user_id = request.args.get("user_id")
    username = request.args.get("reference_id")
    
    yesterday = datetime.combine(date.today(), datetime.min.time()) - timedelta(days = 1)

    terra_user = terra.from_user_id(user_id=user_id)
    daily = terra_user.get_daily(start_date= yesterday, to_webhook= False)

    if username not in user_potatoes.keys():
        user_potatoes.update({username: {
            "potatoes": [],
            "current_potato": random.randint(140, 200),
            "current_progress": 0,
            "potatoes_harvested": 0,
            "last_upload": "2023-01-01 00:00:00" #placeholder value, just has to be earlier than the present day
        }})
    
    calories = round(daily.get_json()["data"][0]["calories_data"]["total_burned_calories"])
    
    if (datetime.strptime(user_potatoes[username]['last_upload'], '%Y-%m-%d %H:%M:%S') != yesterday):
        total = calories
        while total >= 0:
            potato_cals = random.randint(140, 200)
            total -= potato_cals
            if total >= 0:
                user_potatoes[username]["potatoes"].append(potato_cals)
                user_potatoes[username]["potatoes_harvested"] += 1
            else:
                user_potatoes[username]["current_potato"] = potato_cals
                user_potatoes[username]["current_progress"] = total+potato_cals
        user_potatoes[username]['last_upload'] = str(yesterday)
        with open("user_potatoes.json", "w") as f:
            json.dump(user_potatoes, f, ensure_ascii=False, indent=4)
    
    return render_template("home.html", 
                           calories=calories,
                           steps=daily.get_json()["data"][0]["distance_data"]["steps"],
                           distance=int(daily.get_json()["data"][0]["distance_data"]["distance_meters"]),
                            user_id=user_id,
                            current_progress=user_potatoes[username]["current_progress"],
                            current_potato=user_potatoes[username]["current_potato"],
                            harvested=user_potatoes[username]["potatoes_harvested"])

@app.route("/logout", methods=["POST"])
def logout():
    terra_user = terra.from_user_id(user_id=request.args.get("user_id"))
    terra.deauthenticate_user(terra_user)
    return render_template("logout.html")


#run the web application
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False,host="0.0.0.0")

