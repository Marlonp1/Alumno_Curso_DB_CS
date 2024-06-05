from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()

curso_alumno = Table('curso_alumno', Base.metadata,
                     Column('curso_id', Integer, ForeignKey('curso.id')),
                     Column('alumno_id', Integer, ForeignKey('alumno.id'))
                     )

class Curso(Base):
    __tablename__ = 'curso'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    alumnos = relationship("Alumno", secondary=curso_alumno, back_populates="cursos")

class Alumno(Base):
    __tablename__ = 'alumno'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    fecha_nacimiento = Column(Date)
    cursos = relationship("Curso", secondary=curso_alumno, back_populates="alumnos")

def crear_base_datos():
    engine = create_engine('sqlite:///escuela.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    curso1 = Curso(nombre='Matemáticas', descripcion='Curso de matemáticas básicas',
                   fecha_inicio=datetime.date(2023, 6, 1), fecha_fin=datetime.date(2023, 12, 1))
    curso2 = Curso(nombre='Historia', descripcion='Curso de historia mundial', fecha_inicio=datetime.date(2023, 7, 1),
                   fecha_fin=datetime.date(2023, 12, 15))

    alumno1 = Alumno(nombre='Juan Pérez', fecha_nacimiento=datetime.date(2000, 5, 10))
    alumno2 = Alumno(nombre='María López', fecha_nacimiento=datetime.date(1998, 11, 22))

    curso1.alumnos.append(alumno1)
    curso2.alumnos.append(alumno1)
    curso2.alumnos.append(alumno2)

    session.add(curso1)
    session.add(curso2)
    session.add(alumno1)
    session.add(alumno2)

    session.commit()
    session.close()

if __name__ == '__main__':
    crear_base_datos()
    print("Datos insertados correctamente")
