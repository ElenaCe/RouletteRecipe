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

#Recipe elements from API
    #Recipe url (url)
    rec=result['hits'][0]['recipe']['url']
    #Recipe title (label)
    rectitle=result['hits'][0]['recipe']['label']
    #Recipe image URL (image)
    recimage=result['hits'][0]['recipe']['image']   

    rec1=result['hits'][1]['recipe']['url']
    rectitle1=result['hits'][1]['recipe']['label']
    recimage1=result['hits'][1]['recipe']['image']

    rec2=result['hits'][2]['recipe']['url']
    rectitle2=result['hits'][2]['recipe']['label']
    recimage2=result['hits'][2]['recipe']['image']
  

    return render_template('./recipe.html',recurl=rec,rectitle=rectitle,recimage=recimage,recurl1=rec1,rectitle1=rectitle1,recimage1=recimage1,recurl2=rec2,rectitle2=rectitle2,recimage2=recimage2)

app.run(debug=True) 