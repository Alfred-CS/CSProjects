from flask import Flask, flash, request, redirect, render_template, url_for, send_file, send_from_directory, abort, session
from flask_session import Session
import re
import mysql.connector
import os
import pymysql

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config.update({
    'SECRET_KEY': 'supersecretkey',
})

# mydb = mysql.connector.connect(
#   host="mysql",
#   database="db",
#   user="username",
#   password="password"
# )



@app.route("/", methods=['GET', 'POST']) 
# No Route Takes User to Login Page
def main():
    return redirect('/login')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect('/login')

@app.route("/home", methods=['GET', 'POST']) 
# Home Page
def home():
    if not session.get("name"):
        return redirect('/login')

        # if logged in, query database for user information and display on homepage


    # query database here, render template with username, lastName, firstName, address, phoneNumber, email, type,
    # certification, certExp, and status so page loads with user info
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST']) 
# Login Page
def login():

    #DB credentials
    if request.method == 'POST':
        ENDPOINT = "hospitaldatabase.c9us8upioch7.us-east-1.rds.amazonaws.com"
        PORT = "3306"
        USER = "ablevy96"
        REGION = "us-east-1"
        DBNAME = "HospitalDatabase"
        os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
        
        #Read from the front end
        doc = request.form.to_dict(flat=False)
        
        user = doc["username"][0]
        user_password = doc["password"][0]
        
        #connect to mysql
        db = pymysql.connect(
            host=ENDPOINT, user=USER,
            password="Learning613", port=3306, db = DBNAME)
        # Run sample query in the database to validate connection
        cursor = db.cursor()
        query = ("SELECT * FROM users")
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            for i in row:
                if i == user:
                    #LOG IN SUCCESS
                    session["name"] = user
                    return redirect('/home')
                
        # ALERT FOR FAILED LOGIN
        flash("Username and Password Do Not Match")
        db.close()
    return render_template('login.html')

@app.route("/newPatient", methods=['GET', 'POST']) 
# New Patient Page
def newPatient():
    if not session.get("name"):
        return redirect('/login')
    
    if request.method == 'POST':
        doc = request.form.to_dict(flat=False)
        firstName = doc['firstName'][0]
        lastName = doc['lastName'][0]
        ssn = doc['ssn'][0]
        insurance = doc['insurance'][0]
        address = doc['address'][0]
        physician = doc['physician'][0]
        admitDate = doc['admitDate'][0]
        status = doc['status'][0]

        # use checkLength function to check fields for massive lengths
    return render_template('newpatient.html')

@app.route("/newStaff", methods=['GET', 'POST'])
# New Staff Page
def newStaff():
    if not session.get("name"):
        return redirect('/login')

    if request.method == 'POST':
        doc = request.form.to_dict(flat=False)

        firstName = doc['firstName'][0]
        lastName = doc['lastName'][0]
        ssn = doc['ssn'][0]
        staffType = doc['type'][0]
        address = doc['address'][0]
        certification = doc['certification'][0]
        certExp = doc['certExp'][0]
        phoneNumber = doc['phone'][0]
        email = doc['email'][0]
        notes = doc['notes'][0]
        payroll = doc['payroll'][0]
        status = doc['status'][0]

        # these variables need to set a new login account
        username = doc['username'][0]
        password = doc['password'][0]

        # save username both with the password and with other staff info so the home page loads with all appropriate information

    return render_template('newstaff.html') 

@app.route("/newFile", methods=['GET', 'POST']) 
# New File Page
def newFile():
    if not session.get("name"):
        return redirect('/login')
    
    if request.method == 'POST':
        doc = request.form.to_dict(flat=False)
        patientName = doc['patientName'][0]
        visitDate = doc['visitDate'][0]
        bed = doc['bed'][0]
        diagnosis = doc['diagnosis'][0]
        treatment = doc['treatment'][0]
        medication = doc['medication'][0]
        notes = doc['notes'][0]
        billingAmount = doc['billingAmount'][0]
        
        checkboxList = request.form.getlist('my_checkbox')
        if len(checkboxList) == 0:
            ambulanceUsed = False
        else:
            ambulanceUsed = True
        # Add info to database here
   

    # query database here, render template with arrays of beds and lastNames so dropdowns populate
    return render_template('newfile.html')

@app.route("/search", methods=['GET', 'POST']) 
# Search Page
def search():
    if not session.get("name"):
        return redirect('/login')
    
    if request.method == 'POST':
        doc = request.form.to_dict(flat=False)
        searchType = doc['searchType'][0]
        firstName = doc['firstName'][0]
        lastName = doc['lastName'][0]

        # query based off the "searchtype" (search either the staff, patients, or records for the information matching the name)

        return redirect('/view') # send over query full results (do not include SSN on Staff) into function, also send over [staff, patient, record]


    return render_template('search.html')

@app.route('/view', methods=['GET', 'POST']) 
# View search results
def view():
    if not session.get("name"):
        return redirect('/login')
    # accept results here, then return them into the new page
    return render_template('view.html')

def checkLength(input):
    #checks the length of a field to make sure it is not too long
    valid = False
    if len(input) < 100: # can change this to a higher character value
        valid = True
    return valid

def checkNumber(input):
    #checks for a valid 0000000000 phone number
    r=re.fullmatch('[0-9][0-9]{9}',input) 
    if r!=None: 
        valid = True
    else:
        valid = False
    return valid    

app.run(debug=True)

