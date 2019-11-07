from app.api import bp
from flask import jsonify, url_for, request 
from app.models import Repuesto
from app import db
from app.api.errors import bad_request

@bp.route('/repuestos/<int:id>', methods=['GET'])
def get_repuesto(id):
	return jsonify(Repuesto.query.get_or_404(id).to_dict())

@bp.route('/repuestos', methods=['GET'])
def get_repuestos():
	repuestos = Repuesto.query.all()
	return jsonify([repuesto.to_dict() 
		for repuesto in repuestos])

@bp.route('/repuestos', methods=['POST'])
def create_repuesto():
	data = request.get_json() or {}
	if 'marca' not in data or 'nombre' not in data or 'precio' not in data:
		return bad_request('Registrar todos los datos requeridos en el formulario')
	repuesto = Repuesto()
	repuesto.marca = data['marca']
	repuesto.nombre = data['nombre']
	repuesto.precio = data['precio']
	db.session.add(repuesto)
	db.session.commit()
	response = jsonify(repuesto.to_dict())
	response.status_code = 201
	response.headers['Location'] = url_for('api.get_repuesto', id=repuesto.id)
	return response