""" Pet Adoption Agency """

from flask import Flask, request, redirect, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet, Specie, db_add_pet, db_edit_pet, db_get_species_list
from forms import AddPetForm, ViewEditPetForm

app = Flask(__name__)

# Flask and SQL Alchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoptions'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "The password is 'PassWord'!"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


#
# PETS!
#


@app.route("/")
def list_pets():
    """ List all Adoption Agency Pets """

    db_pets = Pet.query.all()

    return render_template("list_pets.html", pets=db_pets)


@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """ Form to add and process the add of a new pet. """

    # value returned from db_get_species_list() is a list of tuples NOT a
    #  list of sqlalchemy.engine.row.Row.
    species_list = db_get_species_list()

    form = AddPetForm()

    # dynamically set species choices
    form.species.choices = species_list

    if form.validate_on_submit():
        name = form.name.data
        species_id = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        msg = db_add_pet(name, species_id, photo_url, age, notes)

        flash(msg["text"], msg["severity"])

        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=["GET", "POST"])
def view_edit_pet(pet_id):
    """ Form to view pet details and process any changes about the pet. """

    db_pet = Pet.query.get_or_404(pet_id)

    form = ViewEditPetForm(obj=db_pet)

    # dynamically set species choices
    species_list = db_get_species_list()
    form.species_id.choices = species_list

    if form.validate_on_submit():
        name = form.name.data
        species_id = form.species_id.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        msg = db_edit_pet(pet_id, name, species_id,
                          photo_url, age, notes, available)

        flash(msg["text"], msg["severity"])

        return redirect('/')
    else:
        return render_template('view_edit_pet.html', form=form)
