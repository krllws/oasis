from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100))
    owner = db.Column(db.String(100))

    def __repr__(self):
        return f'<Pet {self.name}>'

@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        owner = request.form['owner']

        new_pet = Pet(name=name, age=age, breed=breed, owner=owner)
        db.session.add(new_pet)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_pet.html')


@app.route('/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    if request.method == 'POST':
        pet_name = request.form['name']
        pet_age = request.form['age']
        pet_breed = request.form['breed']
        pet_owner = request.form['owner']

        db.session.commit()  # Подтверждаем изменения в базе данных
        return redirect(url_for('index'))

    return render_template('edit_pet.html', pet=pet)


@app.route('/delete/<int:pet_id>')
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for('index'))



with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/we')
def we():
    return render_template("we.html")


@app.route('/help_1')
def help_1():
    return render_template("help_1.html")

if __name__ == '__main__':
    app.run(debug=True)
