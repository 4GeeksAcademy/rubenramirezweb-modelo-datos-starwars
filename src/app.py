"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtiene los personajes registrados
@app.route('/people', methods=['GET'])
def handle_people():
    try:
        people_list = []
        # Muestra una lista de objetos People.
        people = db.session.execute(db.select(People)).scalars().all()
        for ppl in people:
            people_list.append(ppl.serialize())
        
        return jsonify({"result": people_list})
    except Exception as e:
        return jsonify({"error": str("e")}), 500

# Obtiene los personajes registrados por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def handle_person_by_id(people_id):
    try:
        # Busca un personaje específico por ID
        people = db.session.execute(db.select(People).filter_by(id=people_id)).scalar_one_or_none()
        # Si no se encuentra, devuelve un error 404
        if people is None:
            return jsonify({"error": "Person not found"}), 404
        
        # Si se encuentra, devuelve su información
        return jsonify({"result": people.serialize()})
    except Exception as e:
        return jsonify({"error": str("e")}), 500



@app.route('/user', methods=['GET'])
def handle_user():
    try:
        user_list = []
        user= db.session.execute(db.select(User)).scalars().all()
        for u in user:
            user_list.append(u.serialize())
        
        return jsonify({"result": user_list})
    except Exception as e:
        return jsonify({"error": str("e")}), 500


# Obtiene los planetas registrados    
@app.route('/planets', methods=['GET'])
def handle_planets():
    try:
        planets_list = []
        planet= db.session.execute(db.select(Planet)).scalars().all()
        for p in planet:
            planets_list.append(p.serialize())
        
        return jsonify({"result": planets_list})
    except Exception as e:
        return jsonify({"error": str("e")}), 500
    
# Obtiene los personajes registrados por ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_by_id(planet_id):
    try:
        # Busca un personaje específico por ID
        planet = db.session.execute(db.select(Planet).filter_by(id=planet_id)).scalar_one_or_none()
        # Si no se encuentra, devuelve un error 404
        if planet is None:
            return jsonify({"error": "Planet not found"}), 404
        
        # Si se encuentra, devuelve su información
        return jsonify({"result": planet.serialize()})
    except Exception as e:
        return jsonify({"error": str("e")}), 500



@app.route('/user/favorites', methods=['GET'])
def get_all_users_favorites():
    try:
        favorites_list = []
        # Trae todos los registros de favoritos
        favorites = db.session.execute(db.select(Favorite)).scalars().all()
        
        for fav in favorites:
            favorites_list.append({
                "id": fav.id,
                "user_id": fav.user_id,
                "people": fav.people_name if fav.people else None,
                "planet": fav.planet.name if fav.planet else None,
                "vehicle": fav.vehicle.name if fav.vehicle else None
            })
        
        return jsonify({"favorites": favorites_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Validar si el planeta existe
        planet = db.session.get(Planet, planet_id)
        if not planet:
            return jsonify({"error": f"Planet with id {planet_id} does not exist"}), 404

        new_fav = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_fav)
        db.session.commit()

        return jsonify({"message": "Planet added to favorites"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
