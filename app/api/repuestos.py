from app.api import bp
from flask import jsonify, url_for, request 
from app.models import Repuesto
from app import db
from app.api.errors import bad_request


@bp.route('/repuestos', methods=['GET'])
def get_repuestos():
	repuestos = Repuesto.query.all()
	return jsonify([repuesto.to_dict() 
		for repuesto in repuestos])