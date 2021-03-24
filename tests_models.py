from unittest import TestCase

from app import app
from models import db, Specie, Pet, change_occurred, db_get_species_list, db_add_pet, db_edit_pet

# Use test database is pet_adoptions_test
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoptions_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class ChangeOccurredTests(TestCase):
    def test_change_occurred(self):
        # with app.test_client() as client:
        self.assertEqual(False, change_occurred(
            [1, 'Taylor', 'cat'], [1, 'Taylor', 'cat']), "test of same values returns False")
        self.assertEqual(True, change_occurred(
            [1, "Taylor", "cat"], [2, "Taylor", "cat"]), "test of different values (pos 1) returns True")
        self.assertEqual(True, change_occurred(
            [1, "Taylor", "cat"], [1, "Taylr", "cat"]), "test of different values (pos 2) returns True")
        self.assertEqual(True, change_occurred(
            [1, "Taylor", "cat"], [1, "Taylor", "cutest cat"]), "test of different values (pos 3) returns True")
        self.assertEqual(True, change_occurred(
            [1, "Taylor"], [1, "Taylor", "cutest cat"]), "test of different length lists returns True")


class FunctionsThatTouchDBTests(TestCase):

    @classmethod
    def setUpClass(cls):
        db.session.rollback()

        Pet.query.delete()
        db.session.commit()
        Specie.query.delete()
        db.session.commit()

        cat = Specie(species="cat")
        dog = Specie(species="dog")
        por = Specie(species="porcupine")
        db.session.add_all([cat, dog, por])
        db.session.commit()

    def test_get_species_list(self):
        with app.test_client() as client:
            self.assertEqual([(1, 'cat'), (2, 'dog'), (3, 'porcupine')],
                             db_get_species_list(), "test of species list")

    def test_db_add_pet(self):
        msg = db_add_pet("Taylor", 4, "taylor.png", 6, "adoption information")
        self.assertEqual(
            msg["text"], 'An error occurred. Taylor was NOT created.', "test of failed inserrt + text message")
        self.assertEqual(
            msg["severity"], 'error', "test of failed inserrt + text message")

        msg = db_add_pet("Taylor", 1, "taylor.png", 6, "adoption information")
        self.assertEqual(
            msg["text"], 'Taylor (a cat) was created.',  "test of text message")
        newpet = Pet.query.get(2)
        self.assertEqual(False, change_occurred(
            [newpet.name, newpet.species_id,
                newpet.photo_url, newpet.age, newpet.notes],
            ["Taylor", 1, "taylor.png", 6, "adoption information"]),
            "quickest way to check all values")
        self.assertEqual(newpet.available, True,
                         "verify available defaulted to True")

    def test_db_edit_pet(self):
        msg = db_edit_pet(2, "Taylor", 1, "taylor.png",
                          6, "adoption information", True)
        self.assertEqual(
            msg["text"], 'There were no changes made to Taylor!', "test of edit with no changes")

        # change all fields and verify
        msg = db_edit_pet(2, "TaylorNowDog", 2, "taylorDog.png",
                          7, "misc rot", False)
        self.assertEqual(
            msg["text"], 'TaylorNowDog successfully updated.', "test of edit with changes")

        # verify changes
        chgpet = Pet.query.get(2)
        self.assertEqual(False, change_occurred(
            [chgpet.name, chgpet.species_id,
                chgpet.photo_url, chgpet.age, chgpet.notes, chgpet.available],
            ["TaylorNowDog", 2,
                "taylorDog.png", 7, "misc rot", False]),
            "quickest way to check all values")
