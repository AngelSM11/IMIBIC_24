
import mysql.connector
from pymysql import Error

def get_Patients():

    try:
        conexion = mysql.connector.connect(
            host="94.247.183.227",
            user="User-hk3864t",
            password="Pd_43kc077Rt875#",
            database="Heartkethon_9376r"
        )
        cursor = conexion.cursor(buffered=True)

        sql = "SELECT nombre, apellidos, edad, nivel_riesgo FROM Pacientes"
        
        cursor.execute(sql)
        conexion.commit()

        patients = []
        for row in cursor.fetchall():
            patient = {
                'nombre': row[0],
                'apellidos': row[1],
                'edad': row[2],
                'nivel_de_peligro': row[3]
            }
            patients.append(patient)

        return patients

    except mysql.connector.Error as e:
        print(f"Error al buscar usuarios: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def select_PacientByDId(dni):

    try:
        conexion = mysql.connector.connect(
            host="94.247.183.227",
            user="User-hk3864t",
            password="Pd_43kc077Rt875#",
            database="Heartkethon_9376r"
        )
        cursor = conexion.cursor(buffered=True)

        sql = "SELECT * FROM Usuarios WHERE dni=%s"
        
        cursor.execute(sql, (dni,))
        conexion.commit()

        res = cursor.fetchone()

        return res
    except Error as e:
        print(f"Error al buscar usuario: {e}")
        return None
    
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def get_PacientsDNI():
    
    try:
        conexion = mysql.connector.connect(
            host="94.247.183.227",
            user="User-hk3864t",
            password="Pd_43kc077Rt875#",
            database="Heartkethon_9376r"
        )
        cursor = conexion.cursor(buffered=True)

        sql = "SELECT dni FROM Pacientes"
        
        cursor.execute(sql)

        dniList = cursor.fetchall()
        dniss = [res[0] for res in dniList]
            
        return dniss

    except Error as e:
        print(f"Error al obtener DNIs de pacientes: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def new_Patient(dni, name, surname, age, danger):
    
    try:

        conexion = mysql.connector.connect(
            host="94.247.183.227",
            user="User-hk3864t",
            password="Pd_43kc077Rt875#",
            database="Heartkethon_9376r"
        )
        cursor = conexion.cursor(buffered=True)

        data = (dni, name, surname, age, danger)
        sql = "INSERT INTO Pacientes (dni, nombre, apellidos, edad, nivel_riesgo) VALUES (%s, %s, %s, %s, %s)"
        
        cursor.execute(sql, (data,))
        conexion.commit()
        userData = (dni, "user", "user")
        sql = "INSERT INTO Usuarios (dni, passKey, userType) VALUES (%s, %s, %s)"
        
        cursor.execute(sql, (userData,))
        conexion.commit()

    except Error as e:
        print(f"Error al obtener DNIs de pacientes: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def modify_Patient(dni, name, surname, age, danger):
    
    try:
        conexion = mysql.connector.connect(
            host="94.247.183.227",
            user="User-hk3864t",
            password="Pd_43kc077Rt875#",
            database="Heartkethon_9376r"
        )
        cursor = conexion.cursor(buffered=True)

        sql = "UPDATE Pacientes SET nombre = %s, apellidos = %s, edad = %s, nivel_riesgo = %s WHERE dni = %s"
        cursor.execute(sql, (name, surname, age, danger, dni))
        conexion.commit()

        sql = "UPDATE Usuarios SET dni = %s WHERE dni = %s"
        cursor.execute(sql, (dni, dni))
        conexion.commit()

        return True

    except mysql.connector.Error as e:
        print(f"Error al modificar paciente: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def delete_Patient(dni):
    try:
        conexion = mysql.connector.connect(
            host="94.247.183.227",
            user="User-hk3864t",
            password="Pd_43kc077Rt875#",
            database="Heartkethon_9376r"
        )
        cursor = conexion.cursor(buffered=True)

        sql = "DELETE FROM Pacientes WHERE dni = %s"
        cursor.execute(sql, (dni,))
        conexion.commit()

        sql = "DELETE FROM Usuarios WHERE dni = %s"
        cursor.execute(sql, (dni,))
        conexion.commit()

        return True

    except mysql.connector.Error as e:
        print(f"Error al eliminar paciente: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()