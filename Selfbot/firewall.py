from flask import Flask, request
from flask_cors import CORS

import requests
import time

app = Flask(__name__)
CORS(app)
headers = {"cookie": "tk=673e0bd8-5c83-4e20-bc00-96710135c5ee"}
url = "https://i-find.org/consultar/Telefone/"

oldTime=0

@app.route("/consultar/Telefone/", methods=["POST"])
def receber_dados():
    global oldTime
    if 10 < time.time()-oldTime:
        oldTime = time.time()
        data = request.form
        data = dict(data)
        session = requests.session()
        response = session.post(url, headers=headers, data=data)
        return response.text
    else:
        return "Espere que consultaram a pouco!"

def firewall():
  app.run(host="0.0.0.0", port=1337)

