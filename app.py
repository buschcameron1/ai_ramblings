from flask import Flask, redirect, render_template, request
import json, requests
from markdown import markdown

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
    body = {
        "model": "llama3.2",
        "prompt": "List 4 randomly selected words comma seperated. Only return the 4 words no other content",
        "stream": False
    }

    links = requests.post("http://192.168.1.100:11434/api/generate", json=body)
    links = json.loads(links.content)
    links = links['response'].split(',')
    links = [x.strip(' ') for x in links]
        
    if not request.args.get('article'):
        title = "Welcome to the home page!"
        article = "Click a link above to begin diving into AI slop.<br>Just remember, all the content here is AI generated and almost guaranteed to be incorrect.<br>Also loading times will be long, please be patient."

    else:
        title = request.args.get('article')

        body["prompt"] = f"write a very short essay about {title} and list a few interesting facts about it."
        article = requests.post("http://192.168.1.100:11434/api/generate", json=body)
        article = json.loads(article.content)
   
    return render_template('/index.html', title=title, article=markdown(article['response']), links=links)

@app.route("/why", methods = ["GET"])
def why():
    return render_template('why.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9080)