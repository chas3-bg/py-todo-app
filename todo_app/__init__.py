from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    db.init_app(app)
    
    from .models import Task
    with app.app_context():
        db.create_all()
    return app
    



app = create_app()


def get_tasks():
    from .models import Task
    tasks = []
    for i in range(len(Task.query.order_by(Task.id).all())):
        tasks.append(Task.query.order_by(Task.id).all()[i])
    
    return tasks



@app.route('/')
def index(): 
    return render_template('index.html', tasks = get_tasks())


@app.route('/task/add', methods=['POST'])
def add_task():
    from .models import Task
    try:
        new_task = Task(title=request.form['newTask'])
        if new_task.title.strip() == "":
            raise Exception("Empty task name")
        db.session.add(new_task)
        db.session.commit()  
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return redirect(url_for('index'))

@app.route('/task/delete', methods=['POST'])
def delete_task():
    from .models import Task
    task = Task.query.filter_by(id=request.form['task_id']).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/task/complete', methods=['POST'])
def complete_task():
    from .models import Task
    task = Task.query.filter_by(id=request.form['task_id']).first()
    task.status = False if task.status == True else True
    db.session.commit()
    return redirect(url_for('index'))

