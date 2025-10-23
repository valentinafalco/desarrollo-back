import logging
from main.extension import db
from main.dominios.genero.modelo_genero import Genero



# ----------------VALIDACION-----------------
# agregar mas validaciones

def validar_campos(data):
	# valida que los datos recibidos para crear o actualizar un genero sean validos
	if 'nombreGenero' not in data or not data['nombreGenero'].strip():
		raise ValueError("El campo 'nombreGenero' es obligatorio.")
	return data['nombreGenero'].strip()


# -------------CREAR GENERO-----------------

def crear_genero(data):
	try:
		nombre = validar_campos(data)
		nuevo_genero = Genero(nombreGenero=nombre)
		db.session.add(nuevo_genero)
		db.session.commit()
		return nuevo_genero
	
	except Exception as e:
		db.session.rollback()
		logging.exception("Error al crear el genero")
		raise e


# -------------ACTUALIZAR GENERO-----------------

def actualizar_genero(id, data):
	
	genero = Genero.query.get(id)
	if not genero:
		raise ValueError("Genero no encontrado.")

	try:
		nombre = validar_campos(data)
		genero.nombreGenero = nombre
		db.session.commit()
		return genero

	except Exception as e:
		db.session.rollback()
		logging.exception("Error al actualizar el genero")
		raise e


# -------------ELIMINAR GENERO-----------------

def eliminar_genero(id):
	
	genero = Genero.query.get(id)
	if not genero:
		raise ValueError("Genero no encontrado.")
	
	try:
		db.session.delete(genero)
		db.session.commit()
		return True
	
	except Exception as e:
		db.session.rollback()
		logging.exception("Error al eliminar el genero") 
		raise e


# -------------LISTAR GENERO-----------------

def listar_generos():
	
	try:
		generos = Genero.query.all()
		if not generos:
			raise ValueError("No hay generos registrados.") 
		return generos

	except Exception as e:
		logging.exception("Error al listar generos")
		raise e


# -------------OBTENER GENERO-----------------

def obtener_genero(id):
	
	genero = Genero.query.get(id)
	if not genero:
		raise ValueError("Genero no encontrado.")
	return genero
