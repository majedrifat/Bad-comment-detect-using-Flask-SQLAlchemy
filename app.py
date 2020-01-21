from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Comments.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Comments(db.Model):
   id = db.Column('Comment_id', db.Integer, primary_key = True)

   addr = db.Column(db.String(140),unique=True,nullable=False) 
 

def __init__(self, addr):
   
   self.addr = addr
  

@app.route('/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        if  len(request.form['addr'])>140:
            flash('Please enter max 140 characters in the fields', 'error')
        else:

            Comment= Comments(addr=request.form['addr'])
            #bad comment checking

          
            with open('badword.txt', 'r', encoding='utf-8') as f:
                badwords = f.read().strip().split("\n")
            tokenized = re.sub('([,!?।‘’“”`()])', r' \1 ', request.form['addr'])
            tokenized = re.sub('\s{2,}', ' ', tokenized)
            words = tokenized.split()
            flag = False
            for word in words:
                if word.lower() in badwords:
                    flag = True
              #checking unique post
            if flag:
                flash('Post contains bad words!')
            else:
                a =bool(Comments.query.filter_by(addr=request.form['addr']).first())
                if a:
                    flash('Post has already been added ')
                else:
                    db.session.add(Comment)
                    db.session.commit()
                    flash('Post was successfully added')
                    return redirect(url_for('new'))
    return render_template('new.html', Comments = Comments.query.all())

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)





