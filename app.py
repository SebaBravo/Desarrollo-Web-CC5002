import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from math import ceil
from sqlalchemy import func, extract 
from datetime import datetime

app = Flask(__name__)

# --- Configuración ---
app.secret_key = 'clave_secreta_tarea2_corregida'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# --- Modelos de Base de Datos (Corregidos) ---

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    comunas = db.relationship('Comuna', backref='region', lazy=True)

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

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
    descripcion = db.Column(db.Text(500))
    
    comuna = db.relationship('Comuna', backref='avisos')
    fotos = db.relationship('Foto', backref='aviso', lazy=True, cascade="all, delete-orphan")
    contactos = db.relationship('ContactarPor', backref='aviso', lazy=True, cascade="all, delete-orphan")
    # --- TAREA 3: AÑADIR ESTA LÍNEA ---
    comentarios = db.relationship('Comentario', backref='aviso', lazy=True, cascade="all, delete-orphan", order_by='Comentario.fecha.desc()')

class Foto(db.Model):
    __tablename__ = 'foto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    # CORRECCIÓN: Se debe llamar 'aviso_id' según tarea2.sql
    aviso_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)

class ContactarPor(db.Model):
    __tablename__ = 'contactar_por'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = db.Column(db.String(150), nullable=False)
    # CORRECCIÓN: Se debe llamar 'aviso_id' según tarea2.sql
    aviso_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)

# --- TAREA 3: AÑADIR ESTE NUEVO MODELO ---
class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    aviso_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)

# --- Funciones Auxiliares ---

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rutas de la Aplicación ---

@app.route('/')
def portada():
    """ Tarea 2: Portada - Muestra los últimos 5 avisos de la BD """
    avisos = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(5).all()
    return render_template('portada.html', avisos=avisos)

@app.route('/agregar_aviso', methods=['GET', 'POST'])
def agregar_aviso():
    """ Tarea 2: Agregar Aviso - Lógica de GET y POST """
    
    if request.method == 'POST':
        # --- 1. Validación de Servidor  ---
        errors = []
        
        # Datos del formulario
        comuna_id = request.form.get('comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        edad = request.form.get('edad')
        unidad_medida = request.form.get('unidad-edad')
        fecha_entrega = request.form.get('fecha-entrega')
        descripcion = request.form.get('descripcion')
        
        # Métodos de contacto (listas) [cite: 44]
        contactos_nombres = request.form.getlist('contactar-por')
        contactos_ids = request.form.getlist('contact-info')
        
        # Archivos (lista) [cite: 44]
        files = request.files.getlist('foto')

        # --- Revisión de reglas de negocio ---
        if not comuna_id: errors.append('La comuna es obligatoria.')
        if not nombre or len(nombre) < 3 or len(nombre) > 200: errors.append('El nombre debe tener entre 3 y 200 caracteres.')
        if not email: errors.append('El email es obligatorio.')
        if not tipo: errors.append('El tipo de mascota es obligatorio.')
        if not cantidad or int(cantidad) < 1: errors.append('La cantidad debe ser al menos 1.')
        if not edad or int(edad) < 1: errors.append('La edad debe ser al menos 1.')
        if not unidad_medida: errors.append('La unidad de medida de la edad es obligatoria.')
        if not fecha_entrega: errors.append('La fecha de entrega es obligatoria.')
        
        # Validación de fotos
        if not files or len(files) == 0:
            errors.append('Debe subir al menos 1 foto.')
        elif len(files) > 5:
            errors.append('No puede subir más de 5 fotos.')
        else:
            for file in files:
                if file.filename == '':
                    errors.append('Una de las fotos seleccionadas no tiene nombre.')
                elif not allowed_file(file.filename):
                    errors.append(f'El archivo {file.filename} no es una imagen permitida.')
        
        # Si hay errores, volver al formulario 
        if errors:
            for error in errors:
                flash(error, 'error')
            # Devolvemos los datos para "rellenar" el formulario (request.form)
            regiones = Region.query.order_by(Region.nombre).all()
            return render_template('agregar_aviso.html', regiones=regiones, form_data=request.form), 400

        # --- 2. Inserción en Base de Datos  ---
        try:
            # Crear AvisoAdopcion
            nuevo_aviso = AvisoAdopcion(
                comuna_id=int(comuna_id),
                sector=sector,
                nombre=nombre,
                email=email,
                celular=celular,
                tipo=tipo,
                cantidad=int(cantidad),
                edad=int(edad),
                unidad_medida=unidad_medida,
                fecha_entrega=datetime.fromisoformat(fecha_entrega),
                descripcion=descripcion
            )
            db.session.add(nuevo_aviso)
            db.session.flush() # Para obtener el 'id' del nuevo aviso

            # --- 3. Guardar Archivos y Fotos  ---
            for file in files:
                filename = secure_filename(file.filename)
                # Crear un nombre de archivo único para evitar colisiones
                unique_filename = f"{nuevo_aviso.id}_{datetime.utcnow().timestamp()}_{filename}"
                ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(ruta_completa)
                
                # Crear registro de Foto
                nueva_foto = Foto(
                    ruta_archivo=app.config['UPLOAD_FOLDER'],
                    nombre_archivo=unique_filename,
                    aviso_id=nuevo_aviso.id
                )
                db.session.add(nueva_foto)

            # --- 4. Guardar Contactos  ---
            for i, nombre_contacto in enumerate(contactos_nombres):
                if nombre_contacto and contactos_ids[i]:
                    nuevo_contacto = ContactarPor(
                        nombre=nombre_contacto,
                        identificador=contactos_ids[i],
                        aviso_id=nuevo_aviso.id
                    )
                    db.session.add(nuevo_contacto)

            db.session.commit()
            
            flash('¡Aviso de adopción agregado con éxito!', 'success')
            return redirect(url_for('portada')) # 

        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar en la base de datos: {str(e)}', 'error')
            regiones = Region.query.order_by(Region.nombre).all()
            return render_template('agregar_aviso.html', regiones=regiones, form_data=request.form), 500
    
    # --- Método GET ---
    # Cargar regiones para poblar el formulario
    regiones = Region.query.order_by(Region.nombre).all()
    return render_template('agregar_aviso.html', regiones=regiones)

@app.route('/listado_avisos')
def listado_avisos():
    """ Tarea 2: Listado de Avisos - Con paginación  """
    
    # Obtener el número de página, por defecto 1
    page = request.args.get('page', 1, type=int)
    
    # Consulta paginada: 5 avisos por página
    pagination = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()).paginate(
        page=page, per_page=5, error_out=False
    )
    
    # 'pagination.items' contiene los avisos de la página actual
    avisos = pagination.items
    
    return render_template('listado_avisos.html', avisos=avisos, pagination=pagination)

@app.route('/detalle_aviso/<int:aviso_id>')
def detalle_aviso(aviso_id):
    """ Tarea 2: Detalle de Aviso - Obtener info desde BD  """
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    return render_template('detalle_aviso.html', aviso=aviso)

@app.route('/estadisticas')
def estadisticas():
    """ Tarea 1 y 2: Estadísticas (estático) """
    return render_template('estadisticas.html')

# --- API para el formulario ---
@app.route('/api/comunas/<int:region_id>')
def get_comunas(region_id):
    """ API para obtener comunas de una región """
    comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
    lista_comunas = [{"id": c.id, "nombre": c.nombre} for c in comunas]
    return jsonify({"comunas": lista_comunas})
# --- TAREA 3: API DE COMENTARIOS ---

@app.route('/api/comentarios/<int:aviso_id>', methods=['GET'])
def get_comentarios(aviso_id):
    """ Tarea 3: Obtener todos los comentarios para un aviso (GET) """
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    
    # Gracias al 'order_by' en la relación, los comentarios ya vienen ordenados
    # del más nuevo al más viejo.
    
    lista_comentarios = []
    for c in aviso.comentarios:
        lista_comentarios.append({
            'id': c.id,
            'nombre': c.nombre,
            'texto': c.texto,
            'fecha': c.fecha.strftime('%Y-%m-%d %H:%M') # Formateamos la fecha
        })
        
    return jsonify(lista_comentarios)

@app.route('/api/comentarios/<int:aviso_id>', methods=['POST'])
def agregar_comentario(aviso_id):
    """ Tarea 3: Agregar un nuevo comentario (POST) """
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    
    # Obtener datos del JSON enviado por el cliente
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se recibieron datos.'}), 400
        
    nombre = data.get('nombre')
    texto = data.get('texto')

    # --- Tarea 3: Validación del lado del servidor ---
    errors = []
    if not nombre:
        errors.append('El nombre es obligatorio.')
    elif len(nombre) < 3:
        errors.append('El nombre debe tener al menos 3 caracteres.')
    elif len(nombre) > 80:
        errors.append('El nombre no puede tener más de 80 caracteres.')
        
    if not texto:
        errors.append('El texto del comentario es obligatorio.')
    elif len(texto) < 5:
        errors.append('El comentario debe tener al menos 5 caracteres.')
    elif len(texto) > 300:
        errors.append('El comentario no puede tener más de 300 caracteres.')

    if errors:
        # Si hay errores de validación, devolverlos
        return jsonify({'errors': errors}), 400

    # --- Si todo es válido, crear y guardar el comentario ---
    try:
        nuevo_comentario = Comentario(
            nombre=nombre,
            texto=texto,
            aviso_id=aviso.id
        )
        
        db.session.add(nuevo_comentario)
        db.session.commit()
        
        # Devolver el comentario recién creado con un estado 201 (Creado)
        return jsonify({
            'id': nuevo_comentario.id,
            'nombre': nuevo_comentario.nombre,
            'texto': nuevo_comentario.texto,
            'fecha': nuevo_comentario.fecha.strftime('%Y-%m-%d %H:%M')
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al guardar en la base de datos: {str(e)}'}), 500
    # --- TAREA 3: API DE ESTADÍSTICAS ---

@app.route('/api/stats/avisos_por_dia')
def stats_avisos_por_dia():
    """ Tarea 3 - Gráfico 1: Cantidad de avisos de adopción por día (últimos 30 días) """
    
    # Consulta para agrupar por fecha y contar avisos
    # Se usa func.date() para ignorar la hora, solo agrupar por día
    query = db.session.query(
        func.date(AvisoAdopcion.fecha_ingreso).label('fecha'),
        func.count(AvisoAdopcion.id).label('cantidad')
    ).group_by('fecha').order_by('fecha')
    
    # Filtramos para obtener solo los últimos 30 días (opcional, pero bueno para el gráfico)
    # thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    # query = query.filter(AvisoAdopcion.fecha_ingreso >= thirty_days_ago)
    
    resultados = query.all()
    
    # Formatear para el gráfico (ej. [ [timestamp, cantidad], [timestamp, cantidad] ])
    # Usamos timestamp (milisegundos) que es lo que Highcharts prefiere
    data_para_grafico = []
    for r in resultados:
        # Convertir la fecha a timestamp en milisegundos (Highcharts)
        timestamp_ms = int(datetime(r.fecha.year, r.fecha.month, r.fecha.day).timestamp() * 1000)
        data_para_grafico.append([timestamp_ms, r.cantidad])
        
    return jsonify(data_para_grafico)


@app.route('/api/stats/total_por_tipo')
def stats_total_por_tipo():
    """ Tarea 3 - Gráfico 2: Total de avisos por tipo de mascota (torta) """
    
    query = db.session.query(
        AvisoAdopcion.tipo,
        func.count(AvisoAdopcion.id).label('cantidad')
    ).group_by(AvisoAdopcion.tipo).all()
    
    # Formatear para el gráfico de torta (ej. [ {'name': 'Gato', 'y': 10}, {'name': 'Perro', 'y': 5} ])
    data_para_grafico = []
    for r in query:
        data_para_grafico.append({
            'name': r.tipo.capitalize(), # 'Gato' o 'Perro'
            'y': r.cantidad
        })
        
    return jsonify(data_para_grafico)


@app.route('/api/stats/avisos_por_mes')
def stats_avisos_por_mes():
    """ Tarea 3 - Gráfico 3: Total de avisos por mes, separado por tipo (barras) """
    
    # Consulta para agrupar por mes Y por tipo
    query = db.session.query(
        extract('month', AvisoAdopcion.fecha_ingreso).label('mes'),
        AvisoAdopcion.tipo,
        func.count(AvisoAdopcion.id).label('cantidad')
    ).group_by('mes', AvisoAdopcion.tipo).order_by('mes', AvisoAdopcion.tipo).all()
    
    # Formatear para el gráfico de barras
    # Necesitamos 3 series:
    # 1. Categorías (eje X): ['Ene', 'Feb', 'Mar', ...]
    # 2. Datos Gatos: [10, 5, 8, ...]
    # 3. Datos Perros: [12, 6, 7, ...]
    
    meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    # Inicializar datos con ceros para los 12 meses
    datos_gatos = [0] * 12
    datos_perros = [0] * 12
    
    for r in query:
        mes_index = int(r.mes) - 1 # Mes (1=Ene) a índice (0=Ene)
        if r.tipo == 'gato':
            datos_gatos[mes_index] = r.cantidad
        elif r.tipo == 'perro':
            datos_perros[mes_index] = r.cantidad
            
    data_para_grafico = {
        'categorias': meses_nombres,
        'series': [
            {
                'name': 'Gatos',
                'data': datos_gatos
            },
            {
                'name': 'Perros',
                'data': datos_perros
            }
        ]
    }
    
    return jsonify(data_para_grafico)

# --- Fin API Tarea 3 ---

# --- Ejecución ---
if __name__ == '__main__':
    # Crear carpeta de uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Nota: La base de datos y las tablas deben ser creadas ejecutando
    # los scripts 'tarea2.sql' y 'region-comuna.sql' directamente en MySQL.
    # No usaremos db.create_all() para asegurar que la estructura sea 100% la del profesor.
    
    print("=" * 50)
    print("Servidor Flask iniciado.")
    print("Asegúrate de haber ejecutado 'tarea2.sql' y 'region-comuna.sql' en tu MySQL.")
    print("Accede a: http://127.0.0.1:5000")
    print("=" * 50)
    
    app.run(debug=True)