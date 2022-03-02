"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "shhhhhh"
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def index():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    return render_template('index.html')


# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************
@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON about ALL cupcakes.
    Respond with JSON like: 
        {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [cup.serialize() for cup in cupcakes] #list comprehension; for each todo, serialize()
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake.
    Respond with JSON like: 
        {cupcake: {id, flavor, size, rating, image}}
    """

    new_cupcake = Cupcake(
        flavor=request.json['flavor'], 
        size=request.json['size'], 
        rating=request.json['rating'],
        image=request.json['image'] or None) #find info coming in as JSON in the body
    
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcake=new_cupcake.serialize()), 201) #return tuple w/ status code (json, status)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake.
    Respond with JSON like: 
        {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(id) #so we don't have to set up a 404 redirect
    return jsonify(cupcake=cupcake.serialize()) #prints into a dictionary which JSONify can use


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL
    Respond with JSON of the newly-updated cupcake, like this: 
        {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake and return confirmation message.
    Respond with JSON like {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake) #delete in database
    db.session.commit()
    return jsonify(message="Deleted") #notify that something happened; doesn't actually show up in GET
