from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from .config import C
eng=create_engine(C.DB_URL, future=True)
S=sessionmaker(bind=eng, expire_on_commit=False, future=True)
B=declarative_base()
class Rec(B):
    __tablename__="recipients"
    email=Column(String, primary_key=True)
    name=Column(String, nullable=True)
    active=Column(Boolean, default=True)
class Alm(B):
    __tablename__="alarms"
    id=Column(String, primary_key=True)
    sev=Column(String, index=True)
    typ=Column(String)
    elem=Column(String)
    msg=Column(Text)
    ts=Column(DateTime(timezone=True), index=True)
    src=Column(String, default="ndac")
class Notif(B):
    __tablename__="notifications"
    id=Column(Integer, primary_key=True, autoincrement=True)
    alarm_id=Column(String, index=True)
    to_e=Column(String, index=True)
    sent_at=Column(DateTime(timezone=True), server_default=func.now())
    status=Column(String)
class Kv(B):
    __tablename__="kv"
    k=Column(String, primary_key=True)
    v=Column(String)
def init_db():
    B.metadata.create_all(eng)
    with S() as s:
        c=s.query(Rec).count()
        if c==0:
            for e in C.STAKEHOLDERS:
                e=e.strip()
                if e:
                    s.merge(Rec(email=e,name=None,active=True))
            s.commit()