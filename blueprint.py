from flask import Blueprint, request, Response, abort
from schema.model import User, Car, Order
from schema.validation import UserSchema, CarSchema, OrderSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

api_blueprint = Blueprint('api', __name__)

engine = create_engine('mysql://root:Mcyura04@localhost/car_rental', echo=True)
create_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = create_session()


@api_blueprint.route('/car', methods=['POST'])
def create_car():
    car_schema = CarSchema()
    try:
        car = car_schema.load(request.json)
    except:
        abort(400)

    if session.query(Car).filter(Car.id == car.id).first() \
            or session.query(Car).filter(Car.model == car.model).first():
        abort(409)

    session.add(car)
    session.commit()
    return Response(status=201)


@api_blueprint.route('/car/<model>', methods=['GET'])
def get_car(model):
    car = session.query(Car).filter(Car.model == model).first()
    if car is None:
        abort(404)
    car_schema = CarSchema()
    return car_schema.dump(car)


@api_blueprint.route('/cars', methods=['GET'])
def get_all_cars():
    cars = session.query(Car).all()
    car_schema = CarSchema(many=True)
    return car_schema.dump(cars)


@api_blueprint.route('/car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = session.query(Car).filter(Car.id == car_id).first()
    if car is None:
        abort(404)
    car_schema = CarSchema()
    try:
        changed = car_schema.load(request.json)
    except:
        abort(400)

    if car.id != changed.id:
        abort(409)

    car.model = changed.model
    car.status = changed.status

    session.commit()
    return Response(status=200)


@api_blueprint.route('/car/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = session.query(Car).filter(Car.id == car_id).first()
    if car is None:
        abort(404)
    session.delete(car)
    session.commit()
    return Response(status=204)


@api_blueprint.route('/order', methods=['POST'])
def create_order():
    order_schema = OrderSchema()
    try:
        order = order_schema.load(request.json)
    except:
        abort(400)

    if session.query(User).filter(User.id == order.user_id).first() is None \
            or session.query(Car).filter(Car.id == order.car_id).first() is None:
        abort(409)

    if session.query(Order).filter(Order.id == order.id).first():
        abort(409)

    session.add(order)
    session.commit()
    return Response(status=201)


@api_blueprint.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    order_schema = OrderSchema()
    return order_schema.dump(order)


@api_blueprint.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    session.delete(order)
    session.commit()
    return Response(status=204)


@api_blueprint.route('/user', methods=['POST'])
def create_user():
    user_schema = UserSchema()
    try:
        user = user_schema.load(request.json)
    except:
        abort(400)
    if session.query(User).filter(User.id == user.id).first():
        abort(409)
    session.add(user)
    session.commit()
    return Response(status=201)


@api_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404)
    user_schema = UserSchema()
    return user_schema.dump(user)


@api_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404)
    user_schema = UserSchema()
    try:
        changed = user_schema.load(request.json)
    except:
        abort(400)

    if changed.id != user_id:
        abort(400)

    user.first_name = changed.first_name
    user.last_name = changed.last_name
    user.email = changed.email
    user.password = changed.password

    session.commit()
    return Response(status=204)


@api_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404)
    session.delete(user)
    session.commit()
    return Response(status=204)
