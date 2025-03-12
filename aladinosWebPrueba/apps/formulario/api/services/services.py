import os
import gspread
import datetime
from typing import List

def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    return gspread.service_account_from_dict(get_credentials())

def get_credentials() -> dict:
    """
    Return gspread credentials.
    """
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),  # Corrige formato clave
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN")
    }

# Conectar con Google Sheets
SPREADSHEET_NAME ="formularioAladinas"
SPREAD_CLIENT = initialize_gspread()
SPREADSHEET = SPREAD_CLIENT.open(SPREADSHEET_NAME)

def mapear_campos(data):
    """
    Mapea los nombres de los campos en data a los nombres de las columnas en Google Sheets.
    """
    mapeo = {
        "saludo": "Saludo",
        "primer_canal_captacion": "Primer canal de captación",
        "canal_entrada": "Canal Entrada",
        "nombre": "Nombre",
        "apellidos": "Apellidos",
        "tipo_identificacion": "Tipo de identificación",
        "numero_identificacion": "N° identificación",
        "fecha_nacimiento": "Fecha Nacimiento",
        "via_principal": "Vía Principal",
        "cp_direccion": "CP de dirección principal",
        "ciudad_direccion": "Ciudad de dirección principal",
        "estado_provincia": "Estado/Provincia de dirección principal",
        "recibe_memoria": "Recibe Memoria",
        "recibe_correspondencia": "Recibe Correspondencia",
        "movil": "Móvil",
        "telefono_casa": "Teléfono Casa",
        "correo_electronico": "Correo Electrónico",
        "descripcion": "Descripción",
        "importe": "Importe",
        "periodicidad": "Periodicidad",
        "fecha_primer_pago":"Fecha primer pago",
        "dia_presentacion": "Día Presentación",
        "medio_pago": "Medio de pago",
        "tipo_pago": "Tipo de pago",
        "no_iban": "Número de cuenta",
        "concepto_recibo": "Concepto Recibo",
        "mandato": "Mandato",
        "nombre_autom": "Nombre (autom)",
        "persona_id": "Persona ID",
        "nombre_asterisco": "Nombre *",
        "fecha_alta": "Fecha Alta",
        "fundraiser_code": "Codigo Fundraiser",
        "fundraiser_name": "Nombre Fundraiser",
        "quiere_correspondencia": "Quiere Correspondencia",
        "nombre_titular": "Nombre Titular",
        "firma": "Firma",
        "explicacion_donacion_continua": "Explicación Donación Continua",
        "explicacion_no_programa_unico": "Explicación No Programa Único",
        "aceptacion_politica_privacidad": "Aceptación Política Privacidad",
        "aceptacion_socio": "Aceptación Socio",
        "tipo_relacion": "Tipo relación",
    }

    return {mapeo[campo]: valor for campo, valor in data.items() if campo in mapeo}

def encontrar_primera_fila_vacia(hoja):
    """
    Encuentra la primera fila vacía en la hoja de cálculo.
    """
    filas = hoja.get_all_values()  # Obtener todas las filas con datos
    for i, fila in enumerate(filas):
        if not any(fila):  # Si la fila está vacía
            return i + 1  # Las filas en gspread comienzan en 1
    return len(filas) + 1  # Si no hay filas vacías, devuelve la siguiente fila

def agregar_a_google_sheets(data):
    """
    Agrega datos a una hoja específica dentro del Google Sheet.
    Si la hoja del mes actual no existe, la crea con un encabezado.
    Utiliza nombres de columnas para mapear los datos, lo que permite
    que el script funcione incluso si las columnas se reordenan.
    """
    mes_actual = datetime.datetime.now().strftime("%Y-%m")  # Formato "YYYY-MM"

    # Verificar si la hoja del mes existe, si no, crearla
    try:
        hoja = SPREADSHEET.worksheet(mes_actual)
    except gspread.exceptions.WorksheetNotFound:
        hoja = SPREADSHEET.add_worksheet(title=mes_actual, rows="1000", cols="1000")
        # Agregar encabezado
        encabezado = [
            "Codigo Fundraiser", "Nombre Fundraiser", "Saludo", "Primer canal de captación", "Canal Entrada", "Nombre", "Apellidos",
            "Tipo de identificación", "N° identificación", "Fecha Nacimiento",
            "Vía Principal", "CP de dirección principal", "Ciudad de dirección principal", "Estado/Provincia de dirección principal",
            "Recibe Memoria", "Recibe Correspondencia", "Móvil", "Teléfono Casa",
            "Correo Electrónico", "Descripción", "Importe",
            "Periodicidad","Fecha primer pago","Día Presentación", "Medio de pago",
            "Tipo de pago", "Número de cuenta", "Concepto Recibo", "Mandato", "Nombre (autom)",
            "Persona ID", "Nombre *", "Fecha Alta","Tipo relación",
        ]
        hoja.append_row(encabezado)

    # Mapear los nombres de los campos en `data` a los nombres de las columnas en Google Sheets
    data_mapeado = mapear_campos(data)

    # Obtener los nombres de las columnas de la hoja
    encabezados = hoja.row_values(1)  # La primera fila contiene los nombres de las columnas

    # Depuración: Imprimir los encabezados y los datos mapeados
    print("Encabezados:", len(encabezados))
    print("Data Mapeado:", len(data_mapeado))

    # Verificar si faltan columnas en la hoja y añadirlas si es necesario
    columnas_faltantes = set(data_mapeado.keys()) - set(encabezados)
    if columnas_faltantes:
        # Añadir las columnas faltantes al final
        hoja.insert_cols(values=list(columnas_faltantes), col=len(encabezados) + 1)
        encabezados.extend(columnas_faltantes)  # Actualizar la lista de encabezados

    # Crear una lista para almacenar los valores de la fila
    fila = [""] * len(encabezados)  # Inicializar con valores vacíos

    # Mapear los datos a las columnas correctas usando los nombres de las columnas
    for columna, valor in data_mapeado.items():
        if columna in encabezados:
            indice = encabezados.index(columna)  # Obtener el índice de la columna
            fila[indice] = valor  # Asignar el valor a la posición correcta
        else:
            print(f"⚠️ Advertencia: La columna '{columna}' no existe en la hoja.")

    # Depuración: Imprimir la fila que se va a agregar
    print("Fila a agregar:", fila)

    # Encontrar la primera fila vacía
    primera_fila_vacia = encontrar_primera_fila_vacia(hoja)

    # Insertar la fila en la posición correcta
    hoja.insert_row(fila, primera_fila_vacia)