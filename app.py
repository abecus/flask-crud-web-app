from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task self.id>'

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        taskContent = request.form["content"]
        task = Todo(content=taskContent)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')

        except:
            return "Error While Adding Task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return "Could Not Delete"

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Could Not Update"
    else:
        return render_template('update.html', task=task)




if __name__ == "__main__":
    app.run(debug=1)