from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sql.db import conbra_engine

Base = declarative_base()

class BackupLocal(Base):
    """
    Almacenara cada backup que se haga de la base de datos de cada local
    """
    __tablename__ = 'backups_locales'
    __table_args__ = {
        'schema': 'dbo',
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    local_id = Column(Integer, nullable=False)
    empresa_id = Column(Integer, nullable=True)
    nombre_db = Column(String(50), nullable=True)
    ip_addr = Column(String(16), nullable=True)
    puerto = Column(String(5), nullable=True)
    trabajo = Column(String(50), nullable=True)
    rnd = Column(String(50), nullable=True)
    estado = Column(String(20), nullable=True)
    datos_adicionales = Column(Text, nullable=True)
    fecha_inicio_backup = Column(DateTime, default=datetime.now())
    fecha_fin_backup = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    duracion_backup = Column(Integer, default=0)
    
    def __init__(self, local_id, empresa_id, nombre_db, ip_addr, trabajo, rnd, estado, datos_adicionales, fecha_inicio_backup):
        self.local_id = local_id
        self.empresa_id = empresa_id
        self.nombre_db = nombre_db
        self.ip_addr = ip_addr
        self.trabajo = trabajo
        self.rnd = rnd
        self.estado = estado
        self.datos_adicionales = datos_adicionales
        self.fecha_inicio_backup = fecha_inicio_backup

    def __repr__(self):
        return f'<BackupLocal {self.id}>'
    
    def __str__(self):
        return f'<BackupLocal {self.id}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'local_id': self.local_id,
            'nombre_db': self.nombre_db,
            'ip_addr': self.ip_addr,
            'puerto': self.puerto,
            'trabajo': self.trabajo,
            'rnd': self.rnd,
            'estado': self.estado,
            'datos_adicionales': self.datos_adicionales,
            'fecha_inicio_backup': self.fecha_inicio_backup,
            'fecha_fin_backup': self.fecha_fin_backup,
            'duracion_backup': self.duracion_backup
        }
    
Base.metadata.create_all(conbra_engine)