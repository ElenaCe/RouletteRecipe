from flask import Flask, render_template, request

import requests
import os
from dotenv import load_dotenv

app = Flask("MyApp")
@app.route("/")
def open_page():
    #render_template() to tell Flask what HTML page to display
    return render_template("ingpage.html")

@app.route("/search", methods=["POST"])
def submiting():


    ing = request.form['ing']

    load_dotenv()
    rec_api_key = os.getenv("REC_API_KEY")
    rec_api_id = os.getenv("REC_ID")
    
    endpoint = "https://api.edamam.com/search"
   
    payload = {"q":ing, "app_id":rec_api_id, "app_key":rec_api_key}
    
    response = requests.get(endpoint, params=payload)
    result=response.json()

    print(result)
    print(result['hits'][0]['recipe']['url'])
    rec=result['hits'][0]['recipe']['url']
    return render_template('ingpage.html', value=rec)

app.run(debug=True) 






# print(result['hits'][0]['recipe']['url'])
 #   rec=result['hits'][0]['recipe']['url']