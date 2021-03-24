from app import db
from models import Specie, Pet

db.drop_all()
db.create_all()

cat = Specie(species="cat")
dog = Specie(species="dog")
por = Specie(species="porcupine")
db.session.add_all([cat, dog, por])
db.session.commit()

woof = Pet(name="Woofly", species_id=2,
           photo_url="/static/images/woofly.png", age=1)
tay = Pet(name="Taylor", species_id=1,
          photo_url="/static/images/taylor.jpg", age=8,
          notes="A truly lovable, friendly cat!! Any adoptee will be lucky to have her.",
          available=False)
porc = Pet(name="Porchetta", species_id=3,
           photo_url="/static/images/porchetta.png", age=1, available=True)
snar = Pet(name="Snargle", species_id=1,
           photo_url="/static/images/snargle.png", age=2, available=True)

db.session.add_all([woof, tay, porc, snar])
db.session.commit()
