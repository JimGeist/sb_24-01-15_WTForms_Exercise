from unittest import TestCase

from app import app
from models import db, Pet, Specie

# Use test database is pet_adoptions_test
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoptions_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Do not use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Disable Cross-Site Request Forgery for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class HomePageTests(TestCase):
    """Tests for views for Snacks."""

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

        pet1 = Pet(name="Woofly", species_id=2,
                   photo_url="http://127.0.0.1:5000/static/images/woofly.png", age=1,
                   notes="woofly-notes")
        pet2 = Pet(name="Taylor", species_id=1,
                   photo_url="http://127.0.0.1:5000/static/images/taylor.jpg", age=8,
                   notes="A truly lovable, friendly cat!! Any adoptee will be lucky to have her.",
                   available=False)

        db.session.add(pet1)
        db.session.commit()
        db.session.add(pet2)
        db.session.commit()

    def setUp(self):
        """ Get the records added by SetUpClass """

        # self.pet1_avail_id = Pet.query.filter_by(name='Woofly').all() does now work
        # and it seems backwards to hardcode the number instead of getting it via a
        # query.
        pet1 = Pet.query.get(1)
        self.pet1_avail_id = pet1.id
        self.pet1_avail = pet1

        pet2 = Pet.query.get(2)
        self.pet2_notavail_id = pet2.id
        self.pet2_notavail = pet2

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            #pet1 is available
            self.assertIn(
                f'class="avail-True" src="{self.pet1_avail.photo_url}"', html)

            #pet2 is not available
            self.assertIn(
                f'class="avail-False" src="{self.pet2_notavail.photo_url}"', html)

            # Add a Pet button is on page
            self.assertIn('Add a Pet</button>', html)

    def test_add_pet_page(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            # Verify fields exist
            self.assertIn('<h1>Add a Pet</h1>', html)
            self.assertIn('name="name"', html)
            self.assertIn('name="species"', html)
            self.assertIn('name="photo_url"', html)
            self.assertIn('name="age"', html)
            self.assertIn('name="notes"', html)

            # Verify dropdown values for species exist
            self.assertIn('value="1">cat', html)
            self.assertIn('value="2">dog', html)
            self.assertIn('value="3">porcupine', html)

            # Add Pet button is on page
            self.assertIn('Add Pet</button>', html)

    def test_VIEW_view_edit_pet_page(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet1_avail_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            # Verify fields exist
            self.assertIn('<h1>View a Pet</h1>', html)
            self.assertIn('name="name"', html)
            self.assertIn(f'value="{self.pet1_avail.name}"', html)
            self.assertIn('name="species_id"', html)
            self.assertIn(
                f'selected value="{self.pet1_avail.species_id}', html)
            self.assertIn('name="photo_url"', html)
            self.assertIn(f'value="{self.pet1_avail.photo_url}"', html)
            self.assertIn('name="age"', html)
            self.assertIn(f'value="{self.pet1_avail.age}"', html)
            self.assertIn('name="available"', html)
            self.assertIn(f'value="y"', html)
            self.assertIn('name="notes"', html)
            self.assertIn(self.pet1_avail.notes, html)

            # Verify dropdown values for species exist
            self.assertIn('value="1">cat', html)
            self.assertIn('value="2">dog', html)
            self.assertIn('value="3">porcupine', html)

            # Save Changes button is on page
            self.assertIn('Save Changes</button>', html)

    def test_nochanges_view_edit_pet_page(self):
        with app.test_client() as client:
            resp = client.post(f"/{self.pet1_avail_id}",
                               data={'name': self.pet1_avail.name,
                                     'species_id': self.pet1_avail.species_id,
                                     'photo_url': self.pet1_avail.photo_url,
                                     'age': self.pet1_avail.age,
                                     'available': 'y',
                                     'notes': self.pet1_avail.notes
                                     },
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            # No data was updated. Make sure no update message appears
            self.assertIn(
                f"There were no changes made to {self.pet1_avail.name}!", html)

    def test_changes_view_edit_pet_page(self):
        with app.test_client() as client:
            resp = client.post(f"/{self.pet1_avail_id}",
                               data={'name': f"{self.pet1_avail.name}New",
                                     'species_id': self.pet1_avail.species_id,
                                     'photo_url': f"{self.pet1_avail.photo_url}New",
                                     'age': self.pet1_avail.age,
                                     'available': 'y',
                                     'notes': self.pet1_avail.notes
                                     },
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            # Name and url were updated.
            # updates to available (true/false; yes/no) were not working
            self.assertIn(
                f"{self.pet1_avail.name} successfully updated", html)
            self.assertIn(
                f'class="avail-True" src="{self.pet1_avail.photo_url}"', html)
            # Verify fields exist

    def test_validators_view_edit_pet_page(self):
        with app.test_client() as client:
            resp = client.post(f"/{self.pet1_avail_id}",
                               data={'name': f"{self.pet1_avail.name}New",
                                     'species_id': self.pet1_avail.species_id,
                                     'photo_url': "invalid__email_url",
                                     'age': 31,
                                     'available': 'y',
                                     'notes': self.pet1_avail.notes
                                     },
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)

            # email url and age are invalid. Edit does not occur, view version
            #  of updatable form rendered
            self.assertNotIn(
                f"{self.pet1_avail.name} successfully updated", html)
            self.assertIn(
                'Formatting is invalid for a web address.', html)
            self.assertIn(
                'Age should be a whole number (no decimals) bewteen 0 and 30', html)
