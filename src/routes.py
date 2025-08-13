from flask import Blueprint , jsonify, request
from models import Character, Akatsuki ,User, db

api_bp=Blueprint("api",__name__)


########## Character
@api_bp.route("/people", methods=["GET"])
def get_characters():
    characters= Character.query.all()
    return jsonify([c.serialize() for c in characters]),200
#Traemos todo "all" query llamada a base de datos (solo lectura)
#        uno get

@api_bp.route("/people/<int:people_id>", methods=["GET"])
def  get_character(people_id):
    character = Character.query.get(people_id)
    if character:
        return jsonify(character.serialize()),200
    return jsonify({"msg":"No existe"}),404


########### Akatsuki
@api_bp.route("/planets", methods=["GET"])
def get_akatsukis():
    akatsukis = Akatsuki.query.all()
    return jsonify([a.selialize()for a in akatsukis ]),200

@api_bp.route("/planets/<int:planet_id>", methods=["GET"])
def get_akatsuki(people_id):
    akatsuki = Akatsuki.query.get(people_id)
    if akatsuki:
        return jsonify(akatsuki.serializer()),200
    return jsonify({"msg":"No existe"}),400


############# User
@api_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([a.selialize()for a in users ]),200

@api_bp.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_userFavorites(user_id):
    user = User.query.get(user_id)
    if not user:
         return jsonify({"msg":"No existe"}),400
    favorites_total = {
        "characters": user.serialize()["favorites_characters"],
        "akatsuki": user.serialize()["favorites_akatsuki"],
        "tailed_beast":user.serialize()["favortes_tailed_beast"]
    }
    if not favorites_total:
         return jsonify({"msg":"Nada"}),400
    
    return jsonify( favorites_total ),200


@api_bp.route("/users/<int:user_id>/favorite/planet/<int:planet_id>", methods=["POST"])
def post_akatsukiFavorites(user_id, planet_id):
    user = db.session.get(User,user_id)
    akatsuki= Akatsuki.query.get(planet_id)

    if not user or not akatsuki:
         return jsonify({"msg":"No existe"}),400
    user.akatsuki.append(akatsuki)
    
    db.session.commit()
    return jsonify(user.serialize())

@api_bp.route("/users/<int:user_id>/favorite/people/<int:people_id>", methods=["POST"])
def post_characteriFavorites(user_id, people_id):
    user = db.session.get(User,user_id)
    character= Character.query.get(people_id)
    
    if not user or not character:
         return jsonify({"msg":"No existe"}),400
    user.characters.append(character)
    
    db.session.commit()
    return jsonify(user.serialize())

@api_bp.route("/users/<int:user_id>/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_akatsukiFavorites(user_id, planet_id):
    user= db.session.get(User,user_id)
    akatsuki =Akatsuki.query.get(planet_id)

    if not user or not akatsuki:
        return jsonify({"msg":"Datos no encontrados"}),400
    
    if akatsuki in user.akatsuki:
        user.akatsuki.remove(akatsuki)
        db.session.commit()
        return jsonify(user.serialize())
    
@api_bp.route("/users/<int:user_id>/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_characteriFavorites(user_id, people_id):
    user= db.session.get(User,user_id)
    character= Character.query.get(people_id)

    if not user or not character:
        return jsonify({"msg":"Datos no encontrados"}),400
    
    if character in user.character:
        user.characters.remove(character)
        db.session.commit()
        return jsonify(user.serialize())


# A vos, que con osadía impía arrebatásteme mi creación, fruto de mi ingenio y sudor.
# Sepáis que esta obra lleva mi impronta, no la ajena. Si acaso os pareciera poseerla,
# sabed bien, y tal convendría entender, que no sois de tal entendimiento que podáis
# comprenderlo... 
# No hay huevos!!!