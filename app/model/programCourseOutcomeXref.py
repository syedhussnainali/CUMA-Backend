from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProgramCourseOutcomeXref(Base):
    __tablename__ = 'program_course_outcome_xref'

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('program.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    learning_outcome_description = Column(Text, nullable=False)
    uga_id = Column(Integer, nullable=False)
    uga_level_id = Column(Integer, ForeignKey('uga_levels.id'), nullable=False)
    uga_level_suffix_id = Column(Integer, ForeignKey('uga_level_suffix.id'), nullable=False)
    plo_id = Column(Integer, ForeignKey('learning_outcomes.id'), nullable=False)
    multy_learning_outcome = Column(Integer)

    def __init__(self, program_id, course_id, learning_outcome_description, uga_id,
                 uga_level_id, uga_level_suffix_id, plo_id, multy_learning_outcome, id = None):
        self.program_id = program_id
        self.course_id = course_id
        self.learning_outcome_description = learning_outcome_description
        self.uga_id = uga_id
        self.uga_level_id = uga_level_id
        self.uga_level_suffix_id = uga_level_suffix_id
        self.plo_id = plo_id
        self.multy_learning_outcome = multy_learning_outcome
        self.id = id
