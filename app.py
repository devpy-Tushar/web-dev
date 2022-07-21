from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFIATIONS'] = False
db = SQLAlchemy(app)

class Project(db.Model):
    Sno = db.Column(db.Integer, primary_key = True)
    Emailid = db.Column(db.String(320), unique = True)
    Password = db.Column(db.String(50), nullable = False)
    Creation_Date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.Emailid}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        email = request.form['Emailid']
        pas = request.form['Password']
        project = Project(Emailid=email, Password=pas)
        db.session.add(project)
        db.session.commit()
    allaccounts = Project.query.all()
    return render_template('index.html', allaccounts = allaccounts)
    # return "<p>Hello, World!</p>"

@app.route("/show")
def products():
    allaccounts = Project.query.all()
    print(allaccounts)
    return "This is Products page"

@app.route("/update/<int:Sno>", methods=['GET', 'POST'])
def update(Sno):
    if request.method == 'POST':
        email = request.form['Emailid']
        pas = request.form['Password']
        account = Project.query.filter_by(Sno=Sno).first()
        account.Emailid = email
        account.Password = pas
        db.session.add(account)
        db.session.commit()
        return redirect("/")
    account = Project.query.filter_by(Sno=Sno).first()
    return render_template('update.html', account = account)

@app.route("/delete/<int:Sno>")
def delete(Sno):
    account = Project.query.filter_by(Sno=Sno).first()
    db.session.delete(account)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)