from datetime import date
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
@app.route('/index.html')
def home():
   date_today = date.today()
   return render_template('index.html', today=date_today)

@app.route("/p2.html")
def page2():
    return render_template("p2.html")

@app.route("/p3.html")
def page3():
    return render_template("p3.html")

if __name__ == '__main__':
   app.run(debug = True)

   
