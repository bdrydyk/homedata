from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def run_app():
	return render_template('index.html')