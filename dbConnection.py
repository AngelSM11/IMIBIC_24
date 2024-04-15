
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Carga las credenciales desde el archivo JSON
cred = credentials.Certificate('heartkathon-e2709-firebase-adminsdk-gfnjn-6e6659f6f1.json')

# Inicializa la aplicación de Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://heartkathon-e2709-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Obtén una referencia a la base de datos en tiempo real
ref = db.reference()

def get_Patients():

    try:
        pacientes = []
        pacientes_ref = ref.child('pacientes').get()
        if pacientes_ref:
            for dni, paciente_data in pacientes_ref.items():
                paciente = {
                    'dni': dni,
                    'nombre': paciente_data.get('nombre', ''),
                    'apellidos': paciente_data.get('apellidos', ''),
                    'edad': paciente_data.get('edad', 0),
                    'nivel_riesgo': paciente_data.get('nivel_riesgo', '')
                }
                pacientes.append(paciente)
        return pacientes
    except Exception as e:
        print("Error al obtener todos los pacientes:", e)
        return []

def select_PacientByDId(dni):

    try:
        paciente_ref = ref.child('pacientes').child(dni).get()
        return paciente_ref is not None
    except Exception as e:
        print("Error al verificar la existencia del paciente:", e)
        return False

def get_PacientsDNI():
    
    try:
        dnis = []
        pacientes_ref = ref.child('pacientes').get()
        if pacientes_ref:
            for dni in pacientes_ref.keys():
                dnis.append(dni)
        return dnis
    except Exception as e:
        print("Error al obtener los DNIs de los pacientes:", e)
        return []

def new_Patient(dni, name, surname, age, danger):
    try:
        ref.child('pacientes').child(dni).set({
            'nombre': name,
            'apellidos': surname,
            'edad': age,
            'nivel_riesgo': danger
        })
        print("Paciente agregado correctamente.")
        return True
    except Exception as e:
        print("Error al agregar paciente:", e)
        return False

def modify_Patient(dni, name, surname, age, danger):
    try:
        ref.child('pacientes').child(dni).update({
            'nombre': name,
            'apellidos': surname,
            'edad': age,
            'nivel_riesgo': danger
        })
        print("Información del paciente modificada correctamente.")
        return True
    except Exception as e:
        print("Error al modificar la información del paciente:", e)
        return False

def delete_Patient(dni):
    try:
        ref.child('pacientes').child(dni).delete()
        print("Paciente eliminado correctamente.")
        return True
    except Exception as e:
        print("Error al eliminar el paciente:", e)
        return False