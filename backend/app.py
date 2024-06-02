try:
    # import generales
    from dotenv import load_dotenv
    from datetime import datetime, timedelta
    
    # import flask
    from flask import Flask, request, jsonify, g
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

    # import de las dependencias
    from werkzeug.security import generate_password_hash, check_password_hash
    import os

except ImportError as e:
    print(f"Error: {e}")
    print("Instalar dependencias con: pip install -r ./requirements.txt")
    exit()

# import de la base de datos y modelos
from sqlalchemy import and_
from sql.db import init_db, gaci_session, conbra_session
from sql.models.User import User
from sql.models.Parloc import Parloc
from sql.models.BackupLocal import BackupLocal

# inicializar la app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv('.env')

# configurar la app
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# inicializar la base de datos
init_db()

# middleware para seleccionar la base de datos
@app.before_request
def before_request():
    if request.path.startswith('/api_locales/parlocs'):
        g.db_session = gaci_session
    elif request.path.startswith('/api_locales/api'):
        g.db_session = conbra_session
    else:
        g.db_session = conbra_session

@app.teardown_request
def teardown_request(exception):
    db_session = getattr(g, 'db_session', None)
    if db_session is not None:
        db_session.remove()

# check if ADMIN_USER and ADMIN_PASS exists on .env
ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASS = os.getenv('ADMIN_PASSWORD')

# if not data, pass, else, search for the user, if not exists, create it
if ADMIN_USER and ADMIN_PASS:
    admin = g.db_session.query(User).filter_by(username=ADMIN_USER).first()
    if not admin:
        new_admin = User(username=ADMIN_USER, password=generate_password_hash(ADMIN_PASS), is_admin=True)
        g.db_session.add(new_admin)
        g.db_session.commit()


# inicializar el jwt
jwt = JWTManager(app)

def checkConnectionToDB():
    try:
        g.db_session.query(User).first()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/api_locales')
def index():
    if checkConnectionToDB() == True:
        return jsonify({
            'success': True,
            'message': 'Conexión exitosa a la base de datos y tablas creadas'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Error al conectar a la base de datos'
        })

@app.route('/api_locales/protected', methods=['GET'])
# @jwt_required()
def protected():
    return jsonify({
        'success': True,
        'message': 'Ruta protegida'
    })

def check_token(token):
    try:
        if token:
            return get_jwt_identity()
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def create_token(user):
    return create_access_token(identity=user)

@app.route('/api_locales/login', methods=['POST'])
def login():
    data = request.get_json()
    user = g.db_session.query(User).filter_by(username=data['username']).first()

    try:
        if user and check_password_hash(user.password, data['password']):
            return jsonify({
                'success': True,
                'message': f'Bienvenido {user.username} :)',
                'token': create_token(user.username)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Usuario o contraseña incorrectos'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al iniciar sesión: {e}'
        }), 500
    
@app.route('/api_locales/register', methods=['POST'])
def register():
    data = request.get_json()
    user = g.db_session.query(User).filter_by(username=data['username']).first()

    try:
        if user:
            return jsonify({
                'success': False,
                'message': 'El usuario ya existe'
            })
        else:
            new_user = User(username=data['username'], password=generate_password_hash(data['password']))
            g.db_session.add(new_user)
            g.db_session.commit()

            return jsonify({
                'success': True,
                'message': f'Usuario {new_user.username} creado correctamente'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al registrar usuario: {e}'
        }), 500
    
@app.route('/api_locales/users', methods=['GET'])
@jwt_required()
def users():
    token = request.headers.get('Authorization') # ...
    """
    Si usas postman o insomnia, debes enviar el token en el header
    Key: Authorization
    Value: Bearer <token>
    """
    user = check_token(token) # chequea si el token es válido

    try:
        if user:
            users = g.db_session.query(User).all()
            return jsonify({
                'success': True,
                'users': [user.serialize() for user in users]
            })
        else:
            return jsonify({
                'success': False,   
                'message': 'Token inválido'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener usuarios: {e}'
        }), 500
    
@app.route('/api_locales/parlocs', methods=['GET'])
# @jwt_required()
def parlocs():
    # token = request.headers.get('Authorization')
    # user = check_token(token)

    try:
        # if user:
            parlocs = g.db_session.query(Parloc).all()
            return jsonify({
                'success': True,
                'parlocs': [parloc.serialize() for parloc in parlocs]
            })
        # else:
            return jsonify({
                'success': False,
                'message': 'Token inválido'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener locales: {e}'
        }), 500
    
@app.route('/api_locales/api/post_backup', methods=['POST'])
def post_backup():
    """
    API que recibe un JSON de un servidor automatizado con la data de un backup
    """
    data = request.get_json()

    """
    CHEQUEAR QUE ESE RANDOM NO EXISTA EN LA BASE DE DATOS
    """
    try:
        # ver si existe el backup por rnd y local_id
        backup_exists = g.db_session.query(BackupLocal).filter(and_(BackupLocal.local_id == data['loc'], BackupLocal.rnd == data['rnd'])).first()

        if backup_exists:
            # modifica la fecha de fin y duracion
            backup_exists.fecha_fin_backup = datetime.now()
            backup_exists.duracion_backup = round((backup_exists.fecha_fin_backup - backup_exists.fecha_inicio_backup).total_seconds() / 60)

            # en caso de que exista datos adicionales, se actualiza
            backup_exists.datos_adicionales = data.get('datos', '')

            # si el estado es completado, se actualiza            
            backup_exists.estado = 'Completado'

            # guardar cambios
            g.db_session.commit()
            return jsonify({
                'success': True,
                'message': 'Backup actualizado correctamente'
            })
        else:
            # wget --post-data="EMP=1&LOC=13&TRABAJO=`BACKUP_GACI`&RND=`NUMERO DE TRABAJO RANDOM`&DATOS=`X` 
            backup = BackupLocal(
                empresa_id=data['emp'],
                local_id=data['loc'],
                trabajo=data['trabajo'],
                nombre_db=g.db_session.bind.url.database,
                ip_addr=request.remote_addr,
                rnd=data['rnd'],
                estado='En proceso',
                datos_adicionales=data.get('datos', ''),
                fecha_inicio_backup=datetime.now()
            )

            g.db_session.add(backup)
            g.db_session.commit()
            return jsonify({
                'success': True,
                'message': 'Backup creado correctamente'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al guardar backup: {e}'
        }), 500

    
@app.route('/api_locales/api/backups', methods=['GET'])
def get_backups():
    local_id = request.args.get('local_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        query = g.db_session.query(BackupLocal)

        if local_id:
            query = query.filter_by(local_id=local_id)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(BackupLocal.fecha_inicio_backup >= start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(BackupLocal.fecha_inicio_backup <= end_date)

        backups = query.all()

        return jsonify({
            'success': True,
            'backups': [backup.serialize() for backup in backups]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener backups: {e}'
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)