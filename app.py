from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #thing needed for database functions in Flask. 
from datetime import datetime

app = Flask(__name__) #reference to the file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # triple / shows that we're using the relative path, four /s would mean absolute path., test.db is the database file we'll be using 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #not compulsory
db = SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_created= db.Column(db.DateTime, default=datetime.now)
    content=db.Column(db.String(200), nullable=False)
    deadline= db.Column(db.Date, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id #every time we create a new element this function will just return "Task" with ID. 


#31/12/24
class Done(db.Model):
    id2=db.Column(db.Integer, primary_key=True)
    date_created2=db.Column(db.DateTime, default=datetime.now)
    contents2=db.Column(db.String(200), nullable=False)
    deadline2=db.Column(db.Date, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id2 


with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET']) #index route so that website doesn't 404 Error when we go to the URL.; POST --> sends data to database, GET --> gets data from database.
def index():
    if request.method=='POST': #condition is fulfilled when data entered into the website (basically when you type stuff into the text box and enter)
        task_content=request.form['content'] #takes the data from the html file
        task_deadline=request.form['deadline']
        task_deadlines = datetime.strptime(task_deadline, '%Y-%m-%d').date() 
        new_task=Todo(content=task_content, deadline=task_deadlines) #creates the data to be entered
        try:
            db.session.add(new_task) #enters the data
            db.session.commit() #commits changes 
            return redirect('/') #back to the home page. 
        except:
            return "There was an issue adding your task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        tasks2 = Done.query.order_by(Done.date_created2).all()
        return render_template("index.html", tasks=tasks, tasks2=tasks2)


@app.route('/delete/<int:id>') #changes the url from something like xyz.com to xyz/delete/1 , no need to write methods = .... because it is only doing GET which is default method.
def delete(id):
    deleted_task = Todo.query.get_or_404(id) #command to get the row, basically like select from table
    new_task=Done(contents2=deleted_task.content, deadline2=deleted_task.deadline) ###
    db.session.add(new_task) ###
    try:
        db.session.delete(deleted_task) 
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        task.deadline=request.form['deadline']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue."
    else:
        return render_template('update.html', task=task)




if __name__ =="__main__":
    app.run(debug=True, port=8000) #specify port number, default runs on 5000.

#To run the program, type python3 main.py in terminal below, copy the link it gives you. 
