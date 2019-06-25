from flask import Flask, render_template, request

import requests
import os
from dotenv import load_dotenv

app = Flask("MyApp")
@app.route("/")
def open_page():
    #render_template() to tell Flask what HTML page to display
    return render_template("index.html")

@app.route("/formpage", methods=["GET"])
def open_formpage():
    return render_template("formpage.html")

@app.route("/aboutus", methods=["GET"])
def open_aboutus():
    return render_template("aboutus.html")

@app.route("/formpage", methods=["POST"])
def submitrecipe():
    form_data = request.form
    email = form_data["email"]
    name = form_data["name"]
    lname = form_data["lname"]
    recipetitle = form_data["recipetitle"]
    ingredients = form_data["ingredients"]
    recipe = form_data["recipe"]
    fileToUpload = request.files["fileToUpload"]
    fullname= name + " " + lname
    
    print(fileToUpload)

    #finds the dotenv file and sets it off 
    load_dotenv()
    #assign variables, asks the to get the mailgun_api and call it api_key
    api_key = os.getenv("MAILGUN_API_KEY")
    api_domain = os.getenv("MAILGUN_DOMAIN")

    #post - sends info to the server
    response = requests.post(
            "https://api.mailgun.net/v3/{}/messages".format(api_domain),
            auth=("api", api_key),
            #in data we're def different variables from, to, subj,..
            #files=[("attachment", (namefile.jpg, fileToUpload))],
            files=[("attachment", (fileToUpload.filename, fileToUpload))],
            data={"from": "Recipe Roulette team <mailgun@{}>".format(api_domain),
                "to": email,
                "subject": "{}! Your submitted recipe for Recipe Roulette".format(name),
                "text": "Hi {} \n \n Thank you! We have successfully received your recipe! \n \n {} \n \n Ingredients: \n {} \n \n Recipe: \n {} \n \n Thank you from the Recipe Roulette team".format(name,recipetitle,ingredients,recipe)})
    print(response.json())
    thankyoumsg= " Thank you " + fullname.title() + " for sending your recipe! "
    return render_template('formpage.html', value=thankyoumsg)
    


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
