from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_secreta_tarea2'

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

db = SQLAlchemy(app)

# Modelos actualizados según tarea2.sql
class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)
    comunas = db.relationship('Comuna', backref='region', lazy=True)

class AvisoAdopcion(db.Model):
    __tablename__ = 'aviso_adopcion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'), nullable=False)
    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    tipo = db.Column(db.Enum('gato', 'perro'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.Enum('a', 'm'), nullable=False)
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text)
    
    comuna = db.relationship('Comuna', backref='avisos')
    fotos = db.relationship('Foto', backref='aviso', lazy=True)
    contactos = db.relationship('ContactarPor', backref='aviso', lazy=True)

class Foto(db.Model):
    __tablename__ = 'foto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)

class ContactarPor(db.Model):
    __tablename__ = 'contactar_por'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = db.Column(db.String(150), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)

# Cargar tu HTML original
with open('tarea1_original.html', 'r', encoding='utf-8') as f:
    HTML_ORIGINAL = f.read()

@app.route('/')
def portada():
    try:
        # Obtener últimos 5 avisos de la base de datos
        avisos = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(5).all()
        
        # Si no hay avisos en la BD, mostrar HTML original sin modificaciones
        if not avisos:
            return HTML_ORIGINAL
        
        # Crear tabla HTML con datos reales
        tabla_avisos = """<table>
    <thead>
        <tr>
            <th>Fecha publicación</th>
            <th>Comuna</th>
            <th>Sector</th>
            <th>Cantidad Tipo edad</th>
            <th>Foto</th>
        </tr>
    </thead>
    <tbody>
"""
        
        for aviso in avisos:
            # Obtener la primera foto del aviso (usando actividad_id)
            primera_foto = Foto.query.filter_by(actividad_id=aviso.id).first()
            foto_src = f"/static/uploads/{primera_foto.nombre_archivo}" if primera_foto else "/static/images/default-pet.jpg"
            
            unidad = 'meses' if aviso.unidad_medida == 'm' else 'años'
            
            tabla_avisos += f"""        <tr onclick="mostrarDetalle({aviso.id})" style="cursor: pointer;">
            <td>{aviso.fecha_ingreso.strftime('%Y-%m-%d %H:%M')}</td>
            <td>{aviso.comuna.nombre if aviso.comuna else 'No especificada'}</td>
            <td>{aviso.sector or 'No especificado'}</td>
            <td>{aviso.cantidad} {aviso.tipo} {aviso.edad} {unidad}</td>
            <td><img src="{foto_src}" alt="{aviso.tipo} en adopción" width="100" height="100"></td>
        </tr>
"""
        
        tabla_avisos += """    </tbody>
</table>"""
        
        # Cadena exacta de la tabla estática en tu HTML original
        tabla_estatica = """<table>
    <thead>
        <tr>
            <th>Fecha publicación</th>
            <th>Comuna</th>
            <th>Sector</th>
            <th>Cantidad Tipo edad</th>
            <th>Foto</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>2025-08-18 12:00</td>
            <td>Santiago</td>
            <td>Beauchef 850, terraza</td>
            <td>1 gato 2 meses</td>
            <td><img src="gato1.jpg" alt="Gato en adopción" width="100" height="100"></td>
        </tr>
        <tr>
            <td>2025-08-17 19:00</td>
            <td>Ñuñoa</td>
            <td>Plaza</td>
            <td>3 perros 2 meses</td>
            <td><img src="perro2.jpg" alt="Perro en adopción" width="100" height="100"></td>
        </tr>
        <tr>
            <td>2025-08-17 18:00</td>
            <td>Santiago</td>
            <td>Parque O'higgins</td>
            <td>2 gatos 1 mes</td>
            <td><img src="gato3.jpg" alt="Gato en adopción" width="100" height="100"></td>
        </tr>
        <tr>
            <td>2025-08-16 15:30</td>
            <td>Providencia</td>
            <td>Parque de las Esculturas</td>
            <td>1 perro 3 años</td>
            <td><img src="perro4.jpg" alt="Perro en adopción" width="100" height="100"></td>
        </tr>
        <tr>
            <td>2025-08-15 11:45</td>
            <td>Las Condes</td>
            <td>Plaza San Enrique</td>
            <td>2 gatos 6 meses</td>
            <td><img src="gato5.jpg" alt="Gato en adopción" width="100" height="100"></td>
        </tr>
    </tbody>
</table>"""
        
        # Reemplazar la tabla estática por la dinámica
        html_modificado = HTML_ORIGINAL.replace(tabla_estatica, tabla_avisos)
        
        return html_modificado
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        # Si hay error, mostrar HTML original
        return HTML_ORIGINAL

# API para obtener regiones y comunas desde la base de datos
@app.route('/api/regiones')
def get_regiones():
    """Retorna todas las regiones con sus comunas"""
    try:
        regiones = Region.query.order_by(Region.nombre).all()
        resultado = {
            "regiones": []
        }
        
        for region in regiones:
            comunas_ordenadas = sorted(region.comunas, key=lambda c: c.nombre)
            resultado["regiones"].append({
                "nombre": region.nombre,
                "comunas": [{"nombre": c.nombre} for c in comunas_ordenadas]
            })
        
        return jsonify(resultado)
    except Exception as e:
        print(f"Error en /api/regiones: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/agregar_aviso', methods=['GET', 'POST'])
def agregar_aviso():
    if request.method == 'POST':
        # Aquí irá la lógica para procesar el formulario
        # Por ahora solo retornamos el HTML
        pass
    return HTML_ORIGINAL

@app.route('/listado_avisos')
def listado_avisos():
    return HTML_ORIGINAL

@app.route('/estadisticas')
def estadisticas():
    return HTML_ORIGINAL

@app.route('/detalle_aviso/<int:id>')
def detalle_aviso(id):
    return HTML_ORIGINAL

# Servir imágenes desde la raíz del proyecto (solo para desarrollo)
from flask import send_from_directory

@app.route('/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos desde la raíz del proyecto"""
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return send_from_directory('.', filename)
    return '', 404

if __name__ == '__main__':
    # Crear carpetas necesarias
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    
    # Inicializar la base de datos si es necesario
    with app.app_context():
        db.create_all()
    
    print("=" * 50)
    print("Servidor Flask iniciado correctamente")
    print("Accede a: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True)
    