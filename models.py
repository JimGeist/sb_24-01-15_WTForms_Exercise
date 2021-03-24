"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy, time
# from sqlalchemy.exc import IntegrityError


db = SQLAlchemy()


def connect_db(app):
    """ Associate the flask application app with SQL Alchemy and
        initialize SQL Alchemy
    """
    db.app = app
    db.init_app(app)


# MODELS

class Specie(db.Model):
    """ Specie model for species table. """

    __tablename__ = 'species'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    species = db.Column(db.String(32),
                        unique=True,
                        nullable=False)

    def __repr__(self):
        """Show species information """

        return f"<Specie id:{self.id} {self.species} >"


class Pet(db.Model):
    """ Pet model for pets table. """

    __tablename__ = 'pets'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(64),
                     nullable=False)

    species_id = db.Column(db.Integer,
                           db.ForeignKey('species.id'),
                           nullable=False)

    photo_url = db.Column(db.Text,
                          nullable=True)

    age = db.Column(db.Integer,
                    nullable=True)

    notes = db.Column(db.Text,
                      nullable=True)

    available = db.Column(db.Boolean,
                          nullable=False, default=True)

    species = db.relationship('Specie', backref='pets')

    def __repr__(self):
        """Show pet information """

        return f"<Pet id:{self.id} - {self.name} species: {self.species_id} age: {self.age} available: {self.available} >"


def change_occurred(from_vals, to_vals):
    """ compares lists of from and to values to ensure a change occurred """

    if (len(from_vals) == len(to_vals)):
        for fr, to in zip(from_vals, to_vals):
            if (fr != to):
                return True
        # all from and to values matched. NO change occurred
        return False
    else:
        # The lengths of the lists should match.
        # For now, return True
        return True


def db_get_species_list():
    """ Function returns a tuple of species id and species for every row in the 
        species table.
    """

    species_list = [(specie.id, specie.species)
                    for specie in db.session.query(Specie.id, Specie.species).all()]

    return species_list


def db_add_pet(name, species, photo_url, age, notes):
    """ adds a pet to the pets table """

    new_pet = Pet(name=name, species_id=species,
                  photo_url=photo_url, age=age, notes=notes)

    try:
        db.session.add(new_pet)
        db.session.commit()

        msg = {
            "text": f"{new_pet.name} (a {new_pet.species.species}) was created."}
        msg["severity"] = "okay"

    except:
        msg = {
            "text": f"An error occurred. {new_pet.name} was NOT created."}
        msg["severity"] = "error"

        db.session.rollback()

    return msg


def db_edit_pet(id, name, species_id, photo_url, age, notes, available):
    """ Updates the user when changes have occurred """

    db_pet = Pet.query.get_or_404(id)

    msg = {}

    if (change_occurred([db_pet.name, db_pet.species_id, db_pet.photo_url, db_pet.age, db_pet.notes, db_pet.available],
                        [name, species_id, photo_url, age, notes, available])):

        db_pet.name = name
        db_pet.species_id = species_id
        db_pet.photo_url = photo_url
        db_pet.age = age
        db_pet.notes = notes
        db_pet.available = available

        db.session.commit()

        msg["text"] = f"{db_pet.name} successfully updated."
        msg["severity"] = "okay"

    else:
        msg["text"] = f"There were no changes made to {db_pet.name}!"
        msg["severity"] = "warning"

    return msg
