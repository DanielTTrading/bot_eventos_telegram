import psycopg2
import os
import time

DB_URL = os.getenv("DATABASE_URL")


def conectar(reintentos=5, espera=5):
    for intento in range(reintentos):
        try:
            return psycopg2.connect(DB_URL)
        except psycopg2.OperationalError:
            print(f"⚠️ DB no disponible (intento {intento + 1}/{reintentos})")
            time.sleep(espera)
    raise psycopg2.OperationalError("❌ No se pudo conectar a la base de datos tras varios intentos.")


def crear_tabla():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_telegram BIGINT PRIMARY KEY,
                nombre TEXT,
                telefono TEXT,
                correo TEXT,
                rol TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Tabla usuarios verificada/creada correctamente")
    except Exception as e:
        print(f"⚠️ No se pudo crear/verificar la tabla usuarios: {e}")


def guardar_usuario(id_telegram, nombre, telefono, correo, rol):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("""
            INSERT INTO usuarios (id_telegram, nombre, telefono, correo, rol)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_telegram) DO UPDATE SET
                nombre = EXCLUDED.nombre,
                telefono = EXCLUDED.telefono,
                correo = EXCLUDED.correo,
                rol = EXCLUDED.rol
        """, (id_telegram, nombre, telefono, correo, rol))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error guardando usuario {id_telegram}: {e}")


def obtener_usuarios_por_rol(rol):
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id_telegram FROM usuarios WHERE rol = %s", (rol,))
        usuarios = [row[0] for row in c.fetchall()]
        conn.close()
        return usuarios
    except Exception as e:
        print(f"⚠️ Error obteniendo usuarios por rol '{rol}': {e}")
        return []


def obtener_todos_los_usuarios():
    try:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id_telegram FROM usuarios")
        usuarios = [row[0] for row in c.fetchall()]
        conn.close()
        return usuarios
    except Exception as e:
        print(f"⚠️ Error obteniendo todos los usuarios: {e}")
        return []