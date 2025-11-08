#Script para llenar la base de datos con datos de prueba (semilla) para hacerlo mas rapido.

import os
import random
import shutil 
from datetime import datetime, timedelta
from app import app, db, AvisoAdopcion, Comuna, Region, ContactarPor, Foto, Comentario

def generate_seed_data():
    with app.app_context():
        
       
        image_dir = os.path.join(app.root_path, 'static', 'images')
        uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
        
        
        os.makedirs(uploads_dir, exist_ok=True)
        
        
        print("Eliminando datos existentes de la Base de Datos...")
        db.session.query(Comentario).delete()
        db.session.query(ContactarPor).delete()
        db.session.query(Foto).delete()
        db.session.query(AvisoAdopcion).delete()
        db.session.commit()
        print("Datos de la BD eliminados.")
        
        print(f"Limpiando carpeta de uploads: {uploads_dir}...")
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Error al eliminar {file_path}. Razón: {e}')
        print("Carpeta de uploads limpia.")

        
        comunas = Comuna.query.all()
        if not comunas:
            print("ERROR: No se encontraron comunas. Ejecuta 'region-comuna.sql'.")
            return

        available_images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if not available_images:
            print(f"ADVERTENCIA: No se encontraron imágenes en {image_dir}.")
            return

        nombres_animales = ["Max", "Luna", "Coco", "Simba", "Nala", "Rocky", "Bella", "Firulais", "Misha", "Duque"]
        tipos_animales = ["perro", "gato"]
        sectores_ejemplo = ["Centro", "Parque Forestal", "Plaza Ñuñoa", "Maipú Centro", "Cerca del Mall"]
        nombres_contacto = ["Ana", "Juan", "Maria", "Carlos", "Sebastian", "Valentina"]
        emails_ejemplo = ["contacto@mail.com", "adopta@mail.com", "info.pet@mail.com"]
        celulares_ejemplo = ["+56987654321", "+56912345678", "+56998877665"]
        
        
        tipos_contacto_ejemplo = ["whatsapp", "telegram", "instagram", "otra"] 

        print("Generando 20 nuevos avisos de adopción...")
        for i in range(20):
            tipo_animal = random.choice(tipos_animales)
            comuna_elegida = random.choice(comunas)
            fecha_ingreso = datetime.now() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))

            nuevo_aviso = AvisoAdopcion(
                fecha_ingreso=fecha_ingreso,
                comuna_id=comuna_elegida.id,
                sector=random.choice(sectores_ejemplo),
                nombre=random.choice(nombres_contacto),
                email=random.choice(emails_ejemplo),
                celular=random.choice(celulares_ejemplo),
                tipo=tipo_animal,
                cantidad=random.randint(1, 4),
                edad=random.randint(1, 10),
                unidad_medida=random.choice(["a", "m"]),
                fecha_entrega=fecha_ingreso + timedelta(days=random.randint(7, 30)),
                descripcion=f"Un adorable {tipo_animal} llamado {random.choice(nombres_animales)} busca hogar."
            )
            db.session.add(nuevo_aviso)
            db.session.flush() 

            
            db.session.add(ContactarPor(
                nombre=random.choice(tipos_contacto_ejemplo),
                identificador=f"@{nuevo_aviso.nombre.lower()}_{i}",
                aviso_id=nuevo_aviso.id
            ))

            
            num_fotos = random.randint(1, 3)
            fotos_seleccionadas = random.sample(available_images, min(num_fotos, len(available_images)))
            
            for img_name in fotos_seleccionadas:
                
                source_path = os.path.join(image_dir, img_name)
                
                
                unique_filename = f"{nuevo_aviso.id}_{datetime.now().timestamp()}_{img_name}"
                
                
                dest_path = os.path.join(uploads_dir, unique_filename)
                
                
                try:
                    shutil.copy2(source_path, dest_path)
                except FileNotFoundError:
                    print(f"Advertencia: No se encontró el archivo {source_path}. Saltando.")
                    continue
                
                
                db.session.add(Foto(
                    ruta_archivo='static/uploads',
                    nombre_archivo=unique_filename, 
                    aviso_id=nuevo_aviso.id
                ))

            
            num_comentarios = random.randint(0, 5)
            for j in range(num_comentarios):
                db.session.add(Comentario(
                    nombre=f"Usuario {j+1}",
                    texto=f"¡Qué lindo {tipo_animal}! ¿Sigue disponible?",
                    fecha=fecha_ingreso + timedelta(days=j),
                    aviso_id=nuevo_aviso.id
                ))

        db.session.commit()
        print("¡Datos semilla generados con éxito!")

if __name__ == "__main__":
    generate_seed_data()