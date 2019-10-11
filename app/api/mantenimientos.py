from app.api import bp
from flask import jsonify, url_for, request 
from app.models import Mantenimiento, Repuesto
from app import db
from app.api.errors import bad_request


@bp.route('/mantenimientos/<int:id>', methods=['GET'])
def get_mantenimiento(id):
	return jsonify(Mantenimiento.query.get_or_404(id).to_dict())

@bp.route('/mantenimientos', methods=['GET'])
def get_mantenimientos():
	mantenimientos = Mantenimiento.query.order_by(Mantenimiento.id.desc()).all()
	return jsonify([mantenimiento.to_dict() 
		for mantenimiento in mantenimientos])

@bp.route('/mantenimientos', methods=['POST'])
def create_mantenimiento():
	data = request.get_json() or {}
	if 'kilometraje' not in data:
		return bad_request('Registrar kilometraje en el mantenimiento')
	mantenimiento = Mantenimiento()
	mantenimiento.kilometraje = data['kilometraje']
	mantenimiento.observaciones = data['observaciones']
	mantenimiento.valor_mano_obra = data['valor_mano_obra']
	db.session.add(mantenimiento)
	db.session.commit()	

	for repuesto in data['repuestos']:
		repuesto = Repuesto.query.get(repuesto['id'])
		mantenimiento.repuesto.append(repuesto)

	db.session.commit()
	response = jsonify(mantenimiento.to_dict())
	response.status_code = 201
	response.headers['Location'] = url_for('api.get_mantenimiento', id=mantenimiento.id)
	return response

@bp.route('/mantenimientos/<int:id>', methods=['PUT'])
def update_mantenimiento(id):
	mantenimiento = Mantenimiento.query.get_or_404(id)
	data = request.get_json() or {}
	if 'kilometraje' not in data:
		return bad_request('Registrar kilometraje en el mantenimiento')
	mantenimiento.kilometraje = data['kilometraje']
	mantenimiento.observaciones = data['observaciones']
	mantenimiento.valor_mano_obra = data['valor_mano_obra']
	mantenimiento.repuesto = []
	db.session.add(mantenimiento)
	db.session.commit()

	for repuesto in data['repuestos']:
		repuesto = Repuesto.query.get(repuesto['id'])
		mantenimiento.repuesto.append(repuesto)

	db.session.commit()
	return jsonify(mantenimiento.to_dict())