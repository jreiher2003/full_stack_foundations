from sqlalchemy import create_engine, Sequence, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Column(Integer, Sequence('user_id_seq'), primary_key=True)
# Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

# Base.metadata.create_all(engine)
ed_user = User(name='ed', fullname='Ed Jones', password='edpassword')
# Session.add(ed_user)