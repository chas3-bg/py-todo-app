# style: в целия файл новите редове не са колкото трябва където трябва, препоръчвам линтер, или ако ползваш pycharm:
# Ctrl + Alt + L за автоматично форматиране на кода
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
    # tasks = []
    # for i in range(len(Task.query.order_by(Task.id).all())):
    #     tasks.append(Task.query.order_by(Task.id).all()[i])
    #
    # return tasks

    return Task.query.order_by(Task.id).all()  # експериментирай! много от популярните библиотеки са достатъчно умни,
    # че да може да се използват по най-очевидния питонджийски начин (с минимум допълнителен код)
    # и в двата варианта обаче този код е доста проблемен ако имаш 10 милиона задачи, гуглирай "sqlalchemy result
    # pagination"


@app.route('/')
def index():
    task_names = [i.title for i in get_tasks()]  # безсмислен list comprehension, не правиш нищо с променливата
    return render_template('index.html', tasks = get_tasks())  # не слагай интервали около = когато подаваш аргументи на функция


@app.route('/add_task', methods=['POST'])
def add_task():
    from .models import Task  # избягвай локални импорти освен ако не са напълно необходими. Ако импортиране в
    # началото на файла предизвиква проблеми, примерно circular imports, тогава преструктурирай проекта вместо да го
    # правиш така
    new_task = Task(title=request.form['newTask'])

    # никаква валидация - мога да създам таск със същото име, като съществуващ, или без име изобщо (ако редактирам
    # ХТМЛ-а локално и махна required атрибута от елемента)
    db.session.add(new_task)

    # няма проверка за грешки при записване на таска в базата, поне една генерална Oops! страница би било добре да
    # има :)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task', methods=['POST'])
def delete_task():
    from .models import Task
    # виж заб. 1
    task = Task.query.filter_by(title=request.form['task_name']).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete_task', methods=['POST'])
def complete_task():
    from .models import Task
    # виж заб. 1
    task = Task.query.filter_by(title=request.form['task_name']).first()
    task.status = False if task.status == True else True
    db.session.commit()
    return redirect(url_for('index'))

# заб. 1: понеже нямаш нито валидация, нито database constraint че имената на тасковете трябва да са уникални,
# complete и delete функциите ти стават много интересни, ако има повече от 1 таск с едно и също име.
# Пусни сървиса, отвори го в браузъра, създай няколко таска с едно и също име, и след това започни да кликаш
# чекбоксите до тях и гледай внимателно какво и как се маркира :)
# стандартната практика при CRUD API и/или уеб страници е ID-то на всеки обект да се слага в страницата (понякога
# скрито), и да се подава на бекенда с всяка операция. Оттам нататък примерно изтриването ще бъде Task.query.get(id)
# и със сигурност знаеш, че манипулираш правилният обект. Допълнителният бонус е, че така можеш например да провериш
# дали този таск наистина принадлежи на този юзър и съответно дали той има право да го трие. преди наистина да го
# изтриеш.
