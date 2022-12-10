from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *


def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

# Returns integer value for total sales
def TotalSales():
    total = 0
    seatDict = SeatingChart()
    costMatrix = get_cost_matrix()
    for x in range(12):
        for y in range(4):
            if seatDict[x][y] == 'X':
                total += costMatrix[x][y]
    return total

# Check availability of seat

# Return seating chart as a dictionary of lists, one list per row
def SeatingChart():
    chartFile = open('reservations.txt','r')
    resLines = chartFile.readlines()
    seatDict = {}
    # Create a seat dictionary that is empty
    for x in range(12):
        seatDict[x] = ['O', 'O', 'O', 'O']
    # Update filled seats
    for line in resLines:
        items = line.split(', ')
        print(items[1])
        print(items[2])
        seatDict[int(items[1])][int(items[2])] = 'X'
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
    sales = 0
    errorList = []
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        if SecretCheck(userName, password):
            chartArray = SeatingChart()
            sales = TotalSales()
            auth = True
        else:
            errorList.append('Bad username or password')
            #return render_template("admin-error.html", form=form, errors=errorList, template="form-template")

    return render_template("admin.html", form=form, sales=sales, errorList=errorList, auth=auth, template="form-template", seatingChart=chartArray)

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()

    return render_template("reservations.html", form=form, template="form-template")

