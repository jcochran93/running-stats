from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/authorization')
def auth():
    return redirect("https://www.strava.com/oauth/authorize")

if __name__ == '__main__':
    app.run()