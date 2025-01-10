from flask import Flask, render_template, request
import json, requests, random
from markdown import markdown

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
    links = requests.get("https://random-word-api.herokuapp.com/word?number=4")
    links = json.loads(links.content)
    comments = {}
    usernames = {}
        
    if not request.args.get('article'):
        title = "Welcome to AI Slop!"
        article = "Click a link above to begin diving into AI slop.<br>Just remember, all the content here is AI generated and almost guaranteed to be incorrect.<br>Also loading times will be long, please be patient.<br><br>Above you will find 4 randomly generated words selected by an LLM, clicking on one of them will prompt the LLM to write a short essay and list a few fun facts about the selected word."

    else:
        title = request.args.get('article')
        if " " in title:
            title = "Nice try"
            article = "you're welcome to do that just keep it to one word.<br>Something something input rejection."
        else:
            body = {
                "model": "llama3.2",
                "prompt": f"write a short essay about {title} and list a few interesting facts about it.",
                "stream": False
            }
            article = requests.post("http://192.168.1.103:11434/api/generate", json=body)
            article = json.loads(article.content)
            article = markdown(article['response'])

            commentNum = random.randrange(1, 15)
            body["prompt"] = f"generate {commentNum} random innternet usernames. Return only usernames, comma separated."
            usernames = requests.post("http://192.168.1.103:11434/api/generate", json=body)
            usernames = json.loads(usernames.content)
            usernames = usernames['response'].split(", ")

            body["prompt"] = f"{commentNum} ragebait incorrect comment about the following article. Return only comments, comma seperated. article: {article}"

            comments = requests.post("http://http://192.168.1.103:11434/api/generate", json=body)
            comments = json.loads(comments.content)
            comments = comments['response'].split(", ")

            comments = dict(zip(usernames, comments))


   
    return render_template('/index.html', title=title, article=article, links=links, comments=comments)

@app.route("/why", methods = ["GET"])
def why():
    return render_template('why.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9080)