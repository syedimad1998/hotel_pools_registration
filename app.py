from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text



now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pool.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    # content = db.Column(db.String(200),nullable=False)
    name = db.Column(db.String(200),nullable=False)
    slot = db.Column(db.String(200),nullable=False)
    room_no = db.Column(db.Integer,nullable=False)
    no_adults = db.Column(db.Integer,nullable=False)
    children = db.Column(db.Integer,nullable=False)
    #date_created = db.Column(db.DateTime, default = datetime.utcnow)
    time_created = db.Column(db.DateTime, default=datetime.now)
    time_updated = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        slot = request.form['slot']
        room_no = request.form['room_no']
        no_adults = request.form['no_adults']
        children = request.form['children']
        new_task = Todo(name=name,slot=slot,room_no=room_no,no_adults=no_adults,children=children)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        slots1 = Todo.query.filter_by(slot='Slot1').all()
        slots2 = Todo.query.filter_by(slot='Slot2').all()
        slots3 = Todo.query.filter_by(slot='Slot3').all()
        slots4 = Todo.query.filter_by(slot='Slot4').all()
        slots5 = Todo.query.filter_by(slot='Slot5').all()
        sum_slot1=0
        sum_slot2=0
        sum_slot3=0
        sum_slot4=0
        sum_slot5=0
        for slot in slots1:
            sum_slot1= sum_slot1 + slot.no_adults + slot.children
        for slot in slots2:
            sum_slot2= sum_slot2 + slot.no_adults + slot.children
        for slot in slots3:
            sum_slot3= sum_slot3 + slot.no_adults + slot.children
        for slot in slots4:
            sum_slot4= sum_slot4 + slot.no_adults + slot.children
        for slot in slots5:
            sum_slot5= sum_slot5 + slot.no_adults + slot.children
        tasks = Todo.query.order_by(Todo.time_created).all()
        return render_template('index.html', tasks=tasks,sum_slot1=sum_slot1,sum_slot2=sum_slot2,sum_slot3=sum_slot3,sum_slot4=sum_slot4,sum_slot5=sum_slot5)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.name = request.form['name']
        # task.slot = request.form['slot']
        task.room_no = request.form['room_no']
        task.no_adults = request.form['no_adults']
        task.children = request.form['children']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/slot1', methods=['GET', 'POST'])
def slot1():
    # task = Todo.query.filter(Todo.slot == 'Slot1')
    # tasks = Todo.query.order_by(Todo.time_created).all()
    tasks = Todo.query.filter_by(slot='Slot1').all()
    return render_template('slot1.html', tasks=tasks)
    # task = Todo.query.filter_by(slot='Slot1').all()
    # task = Todo.query.get_or_404(id)
    # return render_template('slot1.html', task=task)

@app.route('/slot2', methods=['GET', 'POST'])
def slot2():
    tasks = Todo.query.filter_by(slot='Slot2').all()
    return render_template('slot1.html', tasks=tasks)

@app.route('/slot3', methods=['GET', 'POST'])
def slot3():
    tasks = Todo.query.filter_by(slot='Slot3').all()
    return render_template('slot1.html', tasks=tasks)

@app.route('/slot4', methods=['GET', 'POST'])
def slot4():
    tasks = Todo.query.filter_by(slot='Slot4').all()
    return render_template('slot1.html', tasks=tasks)

@app.route('/slot5', methods=['GET', 'POST'])
def slot5():
    tasks = Todo.query.filter_by(slot='Slot5').all()
    return render_template('slot1.html', tasks=tasks)

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)


def display_slot(condition):
    # if session.get("email"):
    #     curl = mysql.connection.cursor()
    #     curl.execute("SELECT * FROM freelancers WHERE domain LIKE %s", [condition])
    #     data = curl.fetchall()
    #     curl.close()
    #     return render_template(
    #         "find_artist.html",
    #         freelancers=data)
    # else:
    #     return redirect(url_for('login'))
    sql = text('select name from TODO')
    result = db.engine.execute(sql)
    names = [row[0] for row in result]
    print(names)
    return result


# @app.route('/Slot1',methods=['POST'])
# def slot1():
#     return display_slot('Slot1')


if __name__ == "__main__":
    app.run(debug=True)
