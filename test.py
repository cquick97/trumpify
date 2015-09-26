from flask import Flask
from flask import request
from flask import render_template
import trumpify as t
import urllib

app = Flask(__name__)
model = t.make_model()

@app.route('/')
def my_form():
    return render_template("test.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    output = t.trumpify(text.lower(), model)

    return render_template("test.html", input=text.lower(), output=output, url=urllib.quote_plus(output))

@app.route('/trumpified/')
def my_test():

 #   text = request.form['text']
 	text = request.args.get('text')
	return(t.trumpify(text.lower(), model))
   # return render_template("test.html", output=output)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
