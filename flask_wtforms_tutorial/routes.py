from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *

# Returns true if the credentials are valid, false if not
def SecretCheck(userName, password):
    return True


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
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        if SecretCheck(userName, password):
            return render_template("admin-reservations.html", form=form, template="form-template")


    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()

    return render_template("reservations.html", form=form, template="form-template")

