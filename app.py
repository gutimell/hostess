from flask import Flask, render_template, request, redirect, url_for, session, Response
import qrcode
import base64
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_es_muy_importante'

# ==============================================================================
# ARCHIVO DE CONFIGURACIÓN FÁCIL DE EDITAR (TU VERSIÓN)
# ==============================================================================

HUESPEDES_VALIDOS = [
    {'depto': '1005', 'nombre': 'admin'},
{'depto': '1005', 'nombre': 'AX'},
{'depto': '1005', 'nombre': 'Jeremy'},
{'depto': '1005', 'nombre': 'Andres'},
{'depto': '1005', 'nombre': 'Cihara'},

    {'depto': '1006', 'nombre': 'admin'},
{'depto': '1006', 'nombre': 'Jeremy'},
{'depto': '1006', 'nombre': 'Natalia'},
{'depto': '1006', 'nombre': 'Giselle'},
]

mock_data = {
    'precioso': { # Perfil para depto 1005
        'id': 'precioso',
        'nombre_perfil': 'Perfil Precioso (Depto 1005)',
        'wifi': {'ssid': 'Gutimell', 'password': 'GM1001SL'},
        'panoramas': [
            {'id': 'p1', 'titulo': 'Cerro San Cristóbal', 'descripcion': 'Disfruta de vistas panorámicas de Santiago, sube en teleférico o funicular.', 'link': 'https://www.parquemet.cl/'},
            {'id': 'p2', 'titulo': 'Teleférico Santiago', 'descripcion': 'Las mejores vistas de la ciudad', 'link': 'https://turistik.com/cerro-san-cristobal/teleferico-santiago/'},
            {'id': 'p3', 'titulo': 'Funicular Santiago', 'descripcion': 'Un viaje en ascensor patrimonial', 'link': 'https://turistik.com/cerro-san-cristobal/funicular-santiago/'},
            {'id': 'p4', 'titulo': 'Barrio Italia', 'descripcion': 'Explora tiendas de diseño, anticuarios y acogedores cafés.', 'link': 'https://www.barrioitalia.com/'},
            {'id': 'p5', 'titulo': 'Plaza Ñuñoa', 'descripcion': 'Un lugar ideal para pasear, con cafés y restaurantes alrededor.', 'link': 'https://www.nunoa.cl/'},
            {'id': 'p6', 'titulo': 'Museo Nacional de Bellas Artes', 'descripcion': 'Descubre obras de arte chileno e internacional en un hermoso edificio.', 'link': 'https://www.mnba.cl/'},
            {'id': 'p7', 'titulo': 'Parque Bicentenario', 'descripcion': 'Amplias áreas verdes, lagunas y esculturas en Vitacura.', 'link': 'https://www.parquebicentenario.cl/'},
        ],
        'restaurantes': [
            {'id': 'r1', 'nombre': 'Bocanáriz', 'direccion': 'José Victorino Lastarria 276, Santiago', 'website': 'https://bocanariz.cl/', 'especialidad': 'Vinos chilenos y tapas'},
            {'id': 'r2', 'nombre': 'Peumayén Ancestral Food', 'direccion': 'Constitución 136, Providencia', 'website': 'https://peumayenchile.cl/', 'especialidad': 'Comida ancestral chilena'},
            {'id': 'r3', 'nombre': 'Como Agua Para Chocolate', 'direccion': 'Constitución 88, Providencia', 'website': 'https://comoaguaparachocolate.cl/', 'especialidad': 'Cocina chilena y latinoamericana'},
            {'id': 'r4', 'nombre': 'La Lucha Sanguchería Criolla', 'direccion': 'Jorge Washington 11, Ñuñoa (Plaza Ñuñoa)', 'website': 'https://lalucha.cl/', 'especialidad': 'Sándwiches peruanos'},
            {'id': 'r5', 'nombre': 'Silvestre Bistro', 'direccion': 'Caupolicán 511, Providencia (Barrio Italia)', 'website': 'https://www.instagram.com/silvestrebistro/', 'especialidad': 'Cocina de mercado y ambiente acogedor'},
            {'id': 'r6', 'nombre': 'Vurger Joint (Opción Vegana)', 'direccion': 'Av. Italia 1186, Providencia (Barrio Italia)', 'website': 'https://www.vurgerjoint.com/', 'especialidad': 'Hamburguesas y comida rápida vegana'},
            {'id': 'r7', 'nombre': 'La Tecla', 'direccion': 'Jorge Washington 57, Ñuñoa (Plaza Ñuñoa)', 'website': 'https://www.latecla.cl/', 'especialidad': 'Cocina chilena y fusión'},
            {'id': 'r8', 'nombre': 'CasaLuz', 'direccion': 'Av. Italia 805, Providencia (Barrio Italia)', 'website': 'https://www.casaluz.cl/', 'especialidad': 'Cocina de autor y coctelería'},
            {'id': 'r9', 'nombre': 'Fuente Suiza', 'direccion': 'Av. Irarrázaval 3361, Ñuñoa', 'website': 'https://fuentesuiza.cl/', 'especialidad': 'Sándwiches clásicos y crudos'},
        ],
        'host': {'telefono': '+56938607776', 'whatsapp': '56938607776'},
        'airbnb_link': 'https://airbnb.com/h/precioso-depto-en-nunoa'
    },
    'hermoso': { # Perfil para depto 1006
        'id': 'hermoso',
        'nombre_perfil': 'Perfil Hermoso (Depto 1006)',
        'wifi': {'ssid': 'Mellguti', 'password': 'GM1001SL'},
        'panoramas': [
            {'id': 'p1', 'titulo': 'Cerro San Cristóbal', 'descripcion': 'Disfruta de vistas panorámicas de Santiago, sube en teleférico o funicular.', 'link': 'https://www.parquemet.cl/'},
            {'id': 'p2', 'titulo': 'Teleférico Santiago', 'descripcion': 'Las mejores vistas de la ciudad', 'link': 'https://turistik.com/cerro-san-cristobal/teleferico-santiago/'},
            {'id': 'p3', 'titulo': 'Funicular Santiago', 'descripcion': 'Un viaje en ascensor patrimonial', 'link': 'https://turistik.com/cerro-san-cristobal/funicular-santiago/'},
            {'id': 'p4', 'titulo': 'Barrio Italia', 'descripcion': 'Explora tiendas de diseño, anticuarios y acogedores cafés.', 'link': 'https://www.barrioitalia.com/'},
            {'id': 'p5', 'titulo': 'Plaza Ñuñoa', 'descripcion': 'Un lugar ideal para pasear, con cafés y restaurantes alrededor.', 'link': 'https://www.nunoa.cl/'},
            {'id': 'p6', 'titulo': 'Museo Nacional de Bellas Artes', 'descripcion': 'Descubre obras de arte chileno e internacional en un hermoso edificio.', 'link': 'https://www.mnba.cl/'},
            {'id': 'p7', 'titulo': 'Parque Bicentenario', 'descripcion': 'Amplias áreas verdes, lagunas y esculturas en Vitacura.', 'link': 'https://www.parquebicentenario.cl/'},
        ],
        'restaurantes': [
            {'id': 'r1', 'nombre': 'Bocanáriz', 'direccion': 'José Victorino Lastarria 276, Santiago', 'website': 'https://bocanariz.cl/', 'especialidad': 'Vinos chilenos y tapas'},
            {'id': 'r2', 'nombre': 'Peumayén Ancestral Food', 'direccion': 'Constitución 136, Providencia', 'website': 'https://peumayenchile.cl/', 'especialidad': 'Comida ancestral chilena'},
            {'id': 'r3', 'nombre': 'Como Agua Para Chocolate', 'direccion': 'Constitución 88, Providencia', 'website': 'https://comoaguaparachocolate.cl/', 'especialidad': 'Cocina chilena y latinoamericana'},
            {'id': 'r4', 'nombre': 'La Lucha Sanguchería Criolla', 'direccion': 'Jorge Washington 11, Ñuñoa (Plaza Ñuñoa)', 'website': 'https://lalucha.cl/', 'especialidad': 'Sándwiches peruanos'},
            {'id': 'r5', 'nombre': 'Silvestre Bistro', 'direccion': 'Caupolicán 511, Providencia (Barrio Italia)', 'website': 'https://www.instagram.com/silvestrebistro/', 'especialidad': 'Cocina de mercado y ambiente acogedor'},
            {'id': 'r6', 'nombre': 'Vurger Joint (Opción Vegana)', 'direccion': 'Av. Italia 1186, Providencia (Barrio Italia)', 'website': 'https://www.vurgerjoint.com/', 'especialidad': 'Hamburguesas y comida rápida vegana'},
            {'id': 'r7', 'nombre': 'La Tecla', 'direccion': 'Jorge Washington 57, Ñuñoa (Plaza Ñuñoa)', 'website': 'https://www.latecla.cl/', 'especialidad': 'Cocina chilena y fusión'},
            {'id': 'r8', 'nombre': 'CasaLuz', 'direccion': 'Av. Italia 805, Providencia (Barrio Italia)', 'website': 'https://www.casaluz.cl/', 'especialidad': 'Cocina de autor y coctelería'},
            {'id': 'r9', 'nombre': 'Fuente Suiza', 'direccion': 'Av. Irarrázaval 3361, Ñuñoa', 'website': 'https://fuentesuiza.cl/', 'especialidad': 'Sándwiches clásicos y crudos'},
        ],
        'host': {'telefono': '+56938607776', 'whatsapp': '56938607776'},
        'airbnb_link': 'https://airbnb.com/h/hermoso-depto-en-nunoa'
    }
}

mock_sos = [
    {'nombre': 'Carabineros (Policía)', 'numero': '133'},
    {'nombre': 'Ambulancia (SAMU)', 'numero': '131'},
    {'nombre': 'Bomberos', 'numero': '132'},
    {'nombre': 'Seguridad Ciudadana Ñuñoa', 'numero': '1419'},
]

@app.context_processor
def inject_now():
    return {'now': datetime.now}

def validar_huesped(depto, nombre):
    for huesped in HUESPEDES_VALIDOS:
        if huesped['depto'] == depto and huesped['nombre'].strip().lower() == nombre.strip().lower():
            return True
    return False

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        depto = request.form.get('depto')
        nombre = request.form.get('nombre')
        
        if not depto or not nombre:
            return render_template('index.html', error="Debes ingresar ambos datos.")

        if validar_huesped(depto, nombre):
            session['guest_name'] = nombre.strip().title()
            session['depto'] = depto
            if depto == '1005':
                session['profile'] = 'precioso'
            elif depto == '1006':
                session['profile'] = 'hermoso'
            return redirect(url_for('menu'))
        else:
            return render_template('index.html', error="Datos incorrectos. Por favor, verifica tu número de depto y nombre.")
            
    return render_template('index.html')

def get_profile_data():
    profile_id = session.get('profile')
    if not profile_id:
        return None, None, None
    
    guest_name = session.get('guest_name')
    depto = session.get('depto')
    profile_data = mock_data.get(profile_id)
    return profile_data, guest_name, depto

@app.route('/menu')
def menu():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    return render_template('menu.html', profile=profile_data, guest_name=guest_name)
    
@app.route('/vcard')
def vcard():
    profile_data, _, _ = get_profile_data()
    if not profile_data or not profile_data.get('host'):
        return "Host data not found", 404

    host_phone = profile_data['host']['telefono'].replace('+', '').replace(' ', '')
    host_name = "Alojamientos Gutimell"

    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{host_name}
TEL;TYPE=CELL:{host_phone}
END:VCARD"""

    return Response(
        vcard_content,
        mimetype="text/vcard",
        headers={"Content-disposition":
                 "attachment; filename=Gutimell_Host.vcf"})

@app.route('/referidos')
def referidos():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))

    fecha_hoy = datetime.now().strftime('%d%m%y')
    nombre_codigo = guest_name.split(' ')[0].upper()
    codigo_referido = f"{nombre_codigo}{fecha_hoy}"

    try:
        with open('referidos.txt', 'a') as f:
            fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{fecha_registro},{depto},{guest_name},{codigo_referido}\n")
    except Exception as e:
        print(f"Error al escribir en referidos.txt: {e}")

    airbnb_link = profile_data.get('airbnb_link', '')
    
    mensaje_wsp = (f"¡Hola! Te recomiendo este Airbnb en Ñuñoa. "
                   f"Usa mi código *{codigo_referido}* para un descuento. "
                   f"Link: {airbnb_link}").replace(" ", "%20")
    
    wsp_share_link = f"https://wa.me/?text={mensaje_wsp}"

    qr_airbnb_str = None
    if airbnb_link:
        try:
            qr_img = qrcode.make(airbnb_link)
            qr_img = qr_img.resize((250, 250))
            img_final = Image.new('RGB', (300, 400), color='white')
            img_final.paste(qr_img, (25, 120))
            draw = ImageDraw.Draw(img_final)
            try:
                font_titulo = ImageFont.truetype("arial.ttf", 20)
                font_codigo = ImageFont.truetype("arialbd.ttf", 24)
                font_pie = ImageFont.truetype("arial.ttf", 14)
            except IOError:
                font_titulo = ImageFont.load_default()
                font_codigo = ImageFont.load_default()
                font_pie = ImageFont.load_default()

            draw.text((50, 20), "¡Gana un 5% DCTO!", fill='black', font=font_titulo)
            draw.text((50, 50), "Código de Referido:", fill='black', font=font_titulo)
            draw.text((70, 80), codigo_referido, fill='blue', font=font_codigo)
            draw.text((60, 375), "Escanea para ir al Airbnb", fill='gray', font=font_pie)

            buffered = BytesIO()
            img_final.save(buffered, format="PNG")
            qr_airbnb_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            print(f"Error generando imagen de QR con Pillow: {e}")

    return render_template('referidos.html', 
                           profile=profile_data, 
                           guest_name=guest_name,
                           codigo=codigo_referido, 
                           qr_airbnb=qr_airbnb_str,
                           wsp_share_link=wsp_share_link)

# (El resto de las rutas, como /wifi, /panoramas, etc., se mantienen igual que en la versión anterior)

@app.route('/wifi')
def wifi():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    wifi_data = profile_data.get('wifi')
    if not wifi_data or not wifi_data.get('ssid') or not wifi_data.get('password'):
        error_msg = "La información del WiFi no está configurada para este perfil."
        return render_template('wifi.html', profile=profile_data, guest_name=guest_name, wifi_data=None, qr_image=None, error=error_msg)
    try:
        wifi_string = f"WIFI:S:{wifi_data['ssid']};T:WPA;P:{wifi_data['password']};;"
        img = qrcode.make(wifi_string)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return render_template('wifi.html', profile=profile_data, guest_name=guest_name, wifi_data=wifi_data, qr_image=img_str, error=None)
    except Exception as e:
        print(f"Error al generar el código QR: {e}")
        error_msg = "Ocurrió un error al generar el código QR."
        return render_template('wifi.html', profile=profile_data, guest_name=guest_name, wifi_data=wifi_data, qr_image=None, error=error_msg)

@app.route('/panoramas')
def panoramas():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    items = profile_data.get('panoramas', [])
    return render_template('lista_items.html', profile=profile_data, guest_name=guest_name, items=items, titulo="Panoramas")

@app.route('/restaurantes')
def restaurantes():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    items = profile_data.get('restaurantes', [])
    return render_template('lista_items.html', profile=profile_data, guest_name=guest_name, items=items, titulo="Restaurantes")

@app.route('/sos')
def sos():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    return render_template('sos.html', profile=profile_data, guest_name=guest_name, numeros=mock_sos)

@app.route('/clima')
def clima():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    mock_clima_data = {
        'actual': {'temp': 18, 'desc': 'Parcialmente nublado', 'icon': '04d'},
        'pronostico': [
            {'dia': 'Jue', 'temp_max': 20, 'temp_min': 9, 'icon': '02d'},
            {'dia': 'Vie', 'temp_max': 22, 'temp_min': 10, 'icon': '01d'},
        ]
    }
    return render_template('clima.html', profile=profile_data, guest_name=guest_name, clima=mock_clima_data)

@app.route('/eventos')
def eventos():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    mock_eventos_data = [
        {'nombre': 'Festival de Jazz de Providencia', 'lugar': 'Parque de las Esculturas', 'fecha': 'Próximo Fin de Semana'},
        {'nombre': 'Cine bajo las estrellas', 'lugar': 'Plaza Ñuñoa', 'fecha': 'Todos los viernes'},
    ]
    return render_template('eventos.html', profile=profile_data, guest_name=guest_name, eventos=mock_eventos_data)

@app.route('/contacto')
def contacto():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    return render_template('contacto.html', profile=profile_data, guest_name=guest_name, depto=depto)

# --- NUEVA RUTA PARA PÁGINA EN CONSTRUCCIÓN ---
@app.route('/en_construccion')
def en_construccion():
    profile_data, guest_name, depto = get_profile_data()
    # No necesitamos verificar si hay profile_data, ya que esta página es genérica
    return render_template('en_construccion.html', guest_name=guest_name)

@app.route('/checkout')
def checkout():
    profile_data, guest_name, depto = get_profile_data()
    if not profile_data:
        return redirect(url_for('index'))
    return render_template('checkout.html', profile=profile_data, guest_name=guest_name, depto=depto)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('referidos.txt'):
        with open('referidos.txt', 'w') as f:
            f.write("Fecha,Depto,Nombre,CodigoReferido\n")
    app.run(debug=True)