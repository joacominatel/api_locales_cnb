from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
from sql.db import gaci_engine

Base = declarative_base()

class Parloc(Base):
    __tablename__ = 'PARLOC'
    __table_args__ = {
        'schema': 'gacipv',
    }

    ParLocEmp = Column(SmallInteger, primary_key=True)
    ParLoc = Column(SmallInteger, primary_key=True)
    ParLocNom = Column(String(40), nullable=True)
    ParLocDir = Column(String(40), nullable=True)
    ParLocZipC = Column(Integer, nullable=True)
    ParLocPais = Column(SmallInteger, nullable=True)
    ParLocMail = Column(String(35), nullable=True)
    ParLocTel = Column(String(15), nullable=True)
    ParLocFax = Column(String(15), nullable=True)
    ParLocLugE = Column(String(40), nullable=True)
    ParLocFchI = Column(DateTime, nullable=True)
    ParLocMod = Column(SmallInteger, nullable=True)
    ParLocTrn = Column(SmallInteger, nullable=True)
    ParLocTrmC = Column(String(2), nullable=True)
    ParLocApeC = Column(String(1), nullable=True)
    ParLocApeT = Column(String(1), nullable=True)
    ParLocMonI = Column(SmallInteger, nullable=True)
    ParLocSucV = Column(SmallInteger, nullable=True)
    ParLocCodV = Column(SmallInteger, nullable=True)
    ParLocTpoV = Column(String(2), nullable=True)
    ParLocSucD = Column(SmallInteger, nullable=True)
    ParLocCodD = Column(String(5), nullable=True)
    ParLocCosM = Column(SmallInteger, nullable=True)
    ParLocCosT = Column(SmallInteger, nullable=True)
    ParLocTpoC = Column(String(1), nullable=True)
    ParLocMonC = Column(SmallInteger, nullable=True)
    ParLocFlgM = Column(String(1), nullable=True)
    ParLocFlgB = Column(String(1), nullable=True)
    ParLocFlgC = Column(String(1), nullable=True)
    ParLocCtaO = Column(String(1), nullable=True)
    ParLocCenC = Column(Integer, nullable=True)
    ParLocEntI = Column(Integer, nullable=True)
    ParLocCliE = Column(Integer, nullable=True)
    ParLocIdTp = Column(String(3), nullable=True)
    ParLocScta = Column(Integer, nullable=True)
    ParLocCasC = Column(String(1), nullable=True)
    ParLocActi = Column(String(1), nullable=True)
    ParLocAbiL = Column(String(1), nullable=True)
    ParLocAbiM = Column(String(1), nullable=True)
    ParLocAbiX = Column(String(1), nullable=True)
    ParLocAbiJ = Column(String(1), nullable=True)
    ParLocAbiV = Column(String(1), nullable=True)
    ParLocAbiS = Column(String(1), nullable=True)
    ParLocAbiD = Column(String(1), nullable=True)
    ParLocHorA = Column(String(5), nullable=True)
    ParLocHorC = Column(String(5), nullable=True)
    ParLocMx2 = Column(Numeric(8, 4), nullable=True)

    def __init__(self, ParLocEmp, ParLoc, ParLocNom, ParLocDir, ParLocZipC, ParLocPais, ParLocMail, ParLocTel, ParLocFax, ParLocLugE, ParLocFchI, ParLocMod, ParLocTrn, ParLocTrmC, ParLocApeC, ParLocApeT, ParLocMonI, ParLocSucV, ParLocCodV, ParLocTpoV, ParLocSucD, ParLocCodD, ParLocCosM, ParLocCosT, ParLocTpoC, ParLocMonC, ParLocFlgM, ParLocFlgB, ParLocFlgC, ParLocCtaO, ParLocCenC, ParLocEntI, ParLocCliE, ParLocIdTp, ParLocScta, ParLocCasC, ParLocActi, ParLocAbiL, ParLocAbiM, ParLocAbiX, ParLocAbiJ, ParLocAbiV, ParLocAbiS, ParLocAbiD, ParLocHorA, ParLocHorC, ParLocMx2):
        self.ParLocEmp = ParLocEmp
        self.ParLoc = ParLoc
        self.ParLocNom = ParLocNom
        self.ParLocDir = ParLocDir
        self.ParLocZipC = ParLocZipC
        self.ParLocPais = ParLocPais
        self.ParLocMail = ParLocMail
        self.ParLocTel = ParLocTel
        self.ParLocFax = ParLocFax
        self.ParLocLugE = ParLocLugE
        self.ParLocFchI = ParLocFchI
        self.ParLocMod = ParLocMod
        self.ParLocTrn = ParLocTrn
        self.ParLocTrmC = ParLocTrmC
        self.ParLocApeC = ParLocApeC
        self.ParLocApeT = ParLocApeT
        self.ParLocMonI = ParLocMonI
        self.ParLocSucV = ParLocSucV
        self.ParLocCodV = ParLocCodV
        self.ParLocTpoV = ParLocTpoV
        self.ParLocSucD = ParLocSucD
        self.ParLocCodD = ParLocCodD
        self.ParLocCosM = ParLocCosM
        self.ParLocCosT = ParLocCosT
        self.ParLocTpoC = ParLocTpoC
        self.ParLocMonC = ParLocMonC
        self.ParLocFlgM = ParLocFlgM
        self.ParLocFlgB = ParLocFlgB
        self.ParLocFlgC = ParLocFlgC
        self.ParLocCtaO = ParLocCtaO
        self.ParLocCenC = ParLocCenC
        self.ParLocEntI = ParLocEntI
        self.ParLocCliE = ParLocCliE
        self.ParLocIdTp = ParLocIdTp
        self.ParLocScta = ParLocScta
        self.ParLocCasC = ParLocCasC
        self.ParLocActi = ParLocActi
        self.ParLocAbiL = ParLocAbiL
        self.ParLocAbiM = ParLocAbiM
        self.ParLocAbiX = ParLocAbiX
        self.ParLocAbiJ = ParLocAbiJ
        self.ParLocAbiV = ParLocAbiV
        self.ParLocAbiS = ParLocAbiS
        self.ParLocAbiD = ParLocAbiD
        self.ParLocHorA = ParLocHorA
        self.ParLocHorC = ParLocHorC
        self.ParLocMx2 = ParLocMx2

    def __repr__(self):
        return '<Parloc %r>' % self.ParLocNom
    
    def serialize(self):
        return {
            'ParLocEmp': self.ParLocEmp,
            'ParLoc': self.ParLoc,
            'ParLocNom': self.ParLocNom,
            'ParLocDir': self.ParLocDir,
            'ParLocZipC': self.ParLocZipC,
            'ParLocPais': self.ParLocPais,
            'ParLocMail': self.ParLocMail,
            'ParLocTel': self.ParLocTel,
            'ParLocFax': self.ParLocFax,
            'ParLocLugE': self.ParLocLugE,
            'ParLocFchI': self.ParLocFchI,
            'ParLocMod': self.ParLocMod,
            'ParLocTrn': self.ParLocTrn,
            'ParLocTrmC': self.ParLocTrmC,
            'ParLocApeC': self.ParLocApeC,
            'ParLocApeT': self.ParLocApeT,
            'ParLocMonI': self.ParLocMonI,
            'ParLocSucV': self.ParLocSucV,
            'ParLocCodV': self.ParLocCodV,
            'ParLocTpoV': self.ParLocTpoV,
            'ParLocSucD': self.ParLocSucD,
            'ParLocCodD': self.ParLocCodD,
            'ParLocCosM': self.ParLocCosM,
            'ParLocCosT': self.ParLocCosT,
            'ParLocTpoC': self.ParLocTpoC,
            'ParLocMonC': self.ParLocMonC,
            'ParLocFlgM': self.ParLocFlgM,
            'ParLocFlgB': self.ParLocFlgB,
            'ParLocFlgC': self.ParLocFlgC,
            'ParLocCtaO': self.ParLocCtaO,
            'ParLocCenC': self.ParLocCenC,
            'ParLocEntI': self.ParLocEntI,
            'ParLocCliE': self.ParLocCliE,
            'ParLocIdTp': self.ParLocIdTp,
            'ParLocScta': self.ParLocScta,
            'ParLocCasC': self.ParLocCasC,
            'ParLocActi': self.ParLocActi,
            'ParLocAbiL': self.ParLocAbiL,
            'ParLocAbiM': self.ParLocAbiM,
            'ParLocAbiX': self.ParLocAbiX,
            'ParLocAbiJ': self.ParLocAbiJ,
            'ParLocAbiV': self.ParLocAbiV,
            'ParLocAbiS': self.ParLocAbiS,
            'ParLocAbiD': self.ParLocAbiD,
            'ParLocHorA': self.ParLocHorA,
            'ParLocHorC': self.ParLocHorC,
            'ParLocMx2': self.ParLocMx2
        }
    
    def serialize_list(self, list):
        return [m.serialize() for m in list]

Base.metadata.create_all(gaci_engine)