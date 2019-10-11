from app import db
from datetime import datetime


cambio_partes = db.Table('cambio_partes', 
	db.Column('mantenimiento_id', db.Integer, db.ForeignKey('mantenimiento.id')),
	db.Column('repuesto_id', db.Integer, db.ForeignKey('repuesto.id'))
)

class Mantenimiento(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	kilometraje = db.Column(db.Integer, index=True)
	observaciones = db.Column(db.String(500))
	valor_mano_obra = db.Column(db.Integer)
	fecha_hora = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	repuesto = db.relationship('Repuesto', secondary=cambio_partes)

	def __repr__(self):
		return '<Mantenimiento {}>'.format(self.kilometraje)

	def to_dict(self):
		data = {
			'id':self.id,
			'kilometraje':self.kilometraje,
			'observaciones':self.observaciones,
			'valor_mano_obra':self.valor_mano_obra,
			'fecha':self.fecha_hora,
			'repuestos': [repuesto.to_dict() for repuesto in self.repuesto]
			}
		return data

class Repuesto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	marca = db.Column(db.String(120), index=True)
	nombre = db.Column(db.String(200), index=True)
	precio = db.Column(db.Integer)
	fecha_hora = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	
	def __repr__(self):
		return '<Repuesto {}>'.format(self.nombre)

	def to_dict(self):
		data = {
			'id':self.id,
			'marca':self.marca,
			'nombre':self.nombre,
			'precio':self.precio,
			'fecha':self.fecha_hora
		}
		return data