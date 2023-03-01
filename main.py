from flask import Flask, render_template, redirect, request
from terra.base_client import Terra
from datetime import datetime
import keys

#terra setup
terra = Terra(api_key=keys.API_KEY, dev_id=keys.DEV_ID, secret=keys.SECRET)

#flask pages
app = Flask(__name__)

@app.route("/")
def home():
    api_response = terra.generate_authentication_url(resource="GOOGLE", auth_success_redirect_url="http://localhost:5000/success", auth_failure_redirect_url="http://localhost:5000/failure", reference_id="0001")
    return redirect(api_response.get_json()['auth_url'])

@app.route("/success")
def success():
    terra_user = terra.from_user_id(user_id=request.args.get("user_id"))
    daily = terra_user.get_daily(start_date= datetime.strptime('2023-02-24','%Y-%m-%d'), to_webhook= False)
    return f'calories: {daily.get_json()["data"][0]["calories_data"]["total_burned_calories"]}\n   \
            steps: {daily.get_json()["data"][0]["distance_data"]["steps"]} \
            distance: {daily.get_json()["data"][0]["distance_data"]["distance_meters"]}'    

#run the web application
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False,host="0.0.0.0")