from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
meta = MetaData()


class Artifacts(Base):
    __tablename__ = 'artifacts'
    artifact_id = Column(Integer, primary_key=True, autoincrement=True)
    artifact_num = Column('artifact_num', String(100), nullable=False)
    artifact_date_id = Column(Integer, ForeignKey('a_dates.date_id'), nullable=False)
    artifact_type_id = Column(Integer, ForeignKey('a_types.type_id'))
    artifact_rev_num_id = Column(Integer, ForeignKey('review.review_id'))
    artifact_ir_id = Column(Integer, ForeignKey('Ir.ir_id'))
    artifact_author_id = Column(Integer, ForeignKey('people.people_id'))
    artifact_moderator_id = Column(Integer, ForeignKey('people.people_id'))
    artifact_scan_tool_id = Column(Integer, ForeignKey('scanTool.scantool_id'))
    artifact_comments_id = Column(Integer, ForeignKey('comments.comments_id'))
    artifact_location_id = Column(Integer, ForeignKey('location.location_id'))
    artifact_filename_id = Column(Integer, ForeignKey('filename.filename_id'))
    artifact_wherefound_id = Column(Integer, ForeignKey('whereFound.wherefound_id'))

    def __init__(self, artifact_num, artifact_date_id, artifact_type_id, artifact_rev_num_id,
                 artifact_ir_id, artifact_author_id, artifact_scan_tool_id, artifact_comments_id,
                 artifact_location_id, artifact_filename_id, artifact_moderator_id, artifact_wherefound_id):
        self.artifact_num = artifact_num
        self.artifact_date_id = artifact_date_id
        self.artifact_type_id = artifact_type_id
        self.artifact_rev_num_id = artifact_rev_num_id
        self.artifact_ir_id = artifact_ir_id
        self.artifact_author_id = artifact_author_id
        self.artifact_scan_tool_id = artifact_scan_tool_id
        self.artifact_comments_id = artifact_comments_id
        self.artifact_location_id = artifact_location_id
        self.artifact_filename_id = artifact_filename_id
        self.artifact_moderator_id = artifact_moderator_id
        self.artifact_wherefound_id = artifact_wherefound_id


class Date(Base):
    __tablename__ = 'a_dates'
    date_id = Column(Integer, primary_key=True, autoincrement=True)
    a_date = Column('a_date', String(100), nullable=False)

    def __init__(self, a_date):
        self.a_date = a_date


class Type(Base):
    __tablename__ = 'a_types'
    type_id = Column(Integer, primary_key=True, autoincrement=True)
    a_type = Column('a_type', String(100), nullable=False)

    def __init__(self, a_type):
        self.a_type = a_type


class Review(Base):
    __tablename__ = 'review'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    review_num = Column('review_num', Integer, nullable=False)

    def __init__(self, review_num):
        self.review_num = review_num


class Ir(Base):
    __tablename__ = 'Ir'
    ir_id = Column(Integer, primary_key=True, autoincrement=True)
    ir_name = Column('ir_name', String(100))

    def __init__(self, ir_name):
        self.ir_name = ir_name


class People(Base):
    __tablename__ = 'people'
    people_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column('author_name', String(100))
    moderator_name = Column('moderator_name', String(100))

    def __init__(self, author_name, moderator_name):
        self.author_name = author_name
        self.moderator_name = moderator_name


class WhereFound(Base):
    __tablename__ = 'whereFound'
    wherefound_id = Column(Integer, primary_key=True, autoincrement=True)
    where_found = Column('where_found', String(100), nullable=False)

    def __init__(self, where_found):
        self.where_found = where_found


class ScanTool(Base):
    __tablename__ = 'scanTool'
    scantool_id = Column(Integer, primary_key=True, autoincrement=True)
    scan_tool = Column('scan_tool', String(100), nullable=False)

    def __init__(self, scan_tool):
        self.scan_tool = scan_tool


class Location(Base):
    __tablename__ = 'location'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    location_name = Column('location_name', String(100), nullable=False)

    def __init__(self, location_name):
        self.location_name = location_name


class Filename(Base):
    __tablename__ = 'filename'
    filename_id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(String(100), nullable=False)

    def __init__(self, filename):
        self.filename = filename


class Comments(Base):
    __tablename__ = 'comments'
    comments_id = Column(Integer, primary_key=True, nullable=False)
    comments = Column(String(100), nullable=False)

    def __init__(self, comments):
        self.comments = comments