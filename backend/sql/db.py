import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()   

gaci_engine = create_engine(os.getenv('GACI_DATABASE_URL'))
conbra_engine = create_engine(os.getenv('CONBRA_DATABASE_URL'))

gaci_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=gaci_engine))

conbra_session = scoped_session(sessionmaker(autocommit=False,
                                           autoflush=False,
                                           bind=conbra_engine))

def init_db():
    from sql.models import Parloc, BackupLocal, User
    Parloc.Base.metadata.create_all(bind=gaci_engine)

    BackupLocal.Base.metadata.create_all(bind=conbra_engine)
    User.Base.metadata.create_all(bind=conbra_engine)
