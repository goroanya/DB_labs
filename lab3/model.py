from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgres://goroanya:goroanya99@localhost:5432/db_lab3')
Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager = Column(String)

    workers = relationship('Worker')

    def __init__(self, name=None, number_of_workers=None, manager=None):
        self.name = name
        self.number_of_workers = number_of_workers
        self.manager = manager


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    budget = Column(BigInteger)
    deadline = Column(Date)

    tasks = relationship('Task')

    def __init__(self, name=None, budget=None, deadline=None):
        self.name = name
        self.budget = budget
        self.deadline = deadline


class Worker(Base):
    __tablename__ = 'worker'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    age = Column(Integer)
    position = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))

    worker_tasks = relationship('WorkerTask')

    def __init__(self, full_name=None, age=None, position=None, department_id=None):
        self.full_name = full_name
        self.age = age
        self.position = position
        self.department_id = department_id


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    deadline = Column(Date)
    description = Column(String)
    project_id = Column(Integer, ForeignKey('project.id'))

    worker_tasks = relationship('WorkerTask')

    def __init__(self, name=None, deadline=None, description=None, project_id=None):
        self.name = name
        self.deadline = deadline
        self.description = description
        self.project_id = project_id


class WorkerTask(Base):
    __tablename__ = 'worker_task'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'))
    worker_id = Column(Integer, ForeignKey('worker.id'))

    def __init__(self, task_id=None, worker_id=None):
        self.task_id = task_id
        self.worker_id = worker_id


session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'worker': Worker, 'task': Task, 'department': Department, 'project': Project, 'worker_task': WorkerTask}


class Model:
    def pairs_from_str(self, string):
        lines = string.split(',')
        pairs = {}
        for line in lines:
            key, value = line.split('=')
            pairs[key.strip()] = value.strip()
        return pairs

    def filter_by_pairs(self, objects, pairs, cls):
        for key, value in pairs.items():
            field = getattr(cls, key)
            objects = objects.filter(field == value)
        return objects

    def insert(self, tname, columns, values):
        columns = [c.strip() for c in columns.split(',')]
        values = [v.strip() for v in values.split(',')]

        pairs = dict(zip(columns, values))
        object_class = TABLES[tname]
        obj = object_class(**pairs)
        session.add(obj)

    def commit(self):
        session.commit()

    def delete(self, tname, condition):
        pairs = self.pairs_from_str(condition)
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        objects.delete()

    def update(self, tname, condition, statement):
        pairs = self.pairs_from_str(condition)
        new_values = self.pairs_from_str(statement)
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        for obj in objects:
            for field_name, value in new_values.items():
                setattr(obj, field_name, value)

    def fill_task_by_random_data(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomDepartments()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 10000;
                INSERT INTO department (name, manager)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 15)
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomDepartments();
        """
        try:
            session.execute(sql)
        finally:
            session.commit()
