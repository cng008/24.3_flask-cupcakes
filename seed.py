from app import app
from models import db, Cupcake


db.drop_all()
db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

c3 = Cupcake(
    flavor="guava",
    size="small",
    rating=1,
    image="https://www.thespruceeats.com/thmb/ZMzLXr7yMQncU4xGz33dnnPF6qg=/450x0/filters:no_upscale():max_bytes(150000):strip_icc()/guavacupcake-57bb7ea45f9b58cdfd61be46.jpg"
)

db.session.add_all([c1, c2, c3])
db.session.commit()