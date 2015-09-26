from flask import Flask
from flask import request
from flask import render_template
import trumpify as t

app = Flask(__name__)
model = t.make_model()

@app.route('/')
def my_form():
    return render_template("test.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    #change this to trumpify
    #processed_text = text.upper()
    #return processed_text
    return t.trumpify(text, model)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
