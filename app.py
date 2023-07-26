import replicate
import os
from flask import Flask, render_template, request
import time
import json
import requests

# model1 = pyttsx3.init()
#
# with sr.Microphone() as source:
#     sr.Recognizer().adjust_for_ambient_noise(source, duration=2)
#     print("waiting for you to speak:")
#     print("please say something you want to draw:")
#     model1.say("please please say something you want to draw")
#     model1.runAndWait()
#     au2 = sr.Recognizer().listen(source)
# try:
#     r1 = sr.Recognizer().recognize_google(au2)
#     r2 = "You have just said " + r1 + " Please wait for a few seconds"
#     print(r2)
#     model1.say(r2)
#     model1.runAndWait()
# except:
#     print("please retry")

# 调用Midjourney接口
os.environ["REPLICATE_API_TOKEN"] = "r8_WSx5lXsc9lsiBG6xZwX7B3FYDvVqKBL2wNGyn"


model = replicate.models.get("tstramer/midjourney-diffusion")
version = model.versions.get("436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b")

# img = Image.open(requests.get(r[0], stream=True).raw)
# img.show()

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        q = request.form.get("question")
        body = json.dumps({"version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf", "input": { "prompt": q } })
        headers = {'Authorization': 'Token r8_WSx5lXsc9lsiBG6xZwX7B3FYDvVqKBL2wNGyn','Content-Type': 'application/json'}
        output = requests.post('https://api.replicate.com/v1/predictions',data=body,headers=headers)
        time.sleep(10)
        get_url = output.json()['urls']['get']
        r = requests.post(get_url, headers=headers).json()['output']
        return (render_template("index.html", result=r[0]))
    else:
        return (render_template("index.html", result="Waiting......"))

if __name__ == "__main__":
    app.run()