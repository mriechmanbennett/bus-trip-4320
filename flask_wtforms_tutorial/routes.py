from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *

# Check availability of seat

# Return seating chart as a dictionary of lists, one list per row
def SeatingChart():
    chartFile = open('reservations.txt','r')
    resLines = chartFile.readlines()
    seatDict = {}
    emptyRowList = ['O', 'O', 'O', 'O']
    # Create a seat dictionary that is empty
    for x in range(12):
        seatDict[x] = emptyRowList
    # Update filled seats
    for line in resLines:
        items = line.split(', ')
        print(items[1])
        print(items[2])
        #seatDict[items[1]][items[2]] = 'X'
    print(seatDict)
    return seatDict

# Returns true if the credentials are valid, false if not
def SecretCheck(userName, password):
    secretFile = open('passcodes.txt','r')
    credsList = secretFile.readlines()
    validCred = False
    for line in credsList:
        creds = line.split(', ')
        if (userName == creds[0]) and (password == creds[1].strip()):
            validCred = True

    return validCred


@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():

    form = AdminLoginForm()
    chartArray = False
    auth = False
    errorList = []
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        if SecretCheck(userName, password):
            chartArray = SeatingChart()
            auth = True
        else:
            errorList.append('Bad username or password')
            #return render_template("admin-error.html", form=form, errors=errorList, template="form-template")

    return render_template("admin.html", form=form, errorList=errorList, auth=auth, template="form-template", seatingChart=chartArray)

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()

    return render_template("reservations.html", form=form, template="form-template")

