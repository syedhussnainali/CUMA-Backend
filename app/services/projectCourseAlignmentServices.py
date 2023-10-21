from flask import jsonify
from ..model.project_course_alignments import ProjectCourseAlignment
from app.services.dbServices import createSession, closeSession
from .utils import getSessionUserID
from sqlalchemy.exc import SQLAlchemyError

def getProjectCourseAlignmentsByCourseID(course_id):
    try:
        session = createSession()
        alignments = session.query(ProjectCourseAlignment).filter(ProjectCourseAlignment.course_id == course_id).all()
        closeSession(session)

        if not alignments:
            return []

        alignment_data = []
        for alignment in alignments:
            alignment_data.append({
                "id": alignment.id,
                "course_id": alignment.course_id,
                "legend": alignment.legend,
                "description": alignment.description
            })
        return alignment_data
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch Project Course Alignments", "message": str(e)}), 500

def addProjectCourseAlignments(alignments, id, session = None):
    try:
        
        for alignment in alignments:
            new_alignment = ProjectCourseAlignment(
                course_id = id,
                legend = alignment['legend'],
                description = alignment['description']
            )
            session.add(new_alignment)
        
        return "Alignments added"
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        print(str(e))
        return jsonify({"error": "Failed to add ProjectCourseAlignments", "message": str(e)}), 500
    

def deleteProjectCourseAlignments(course_id, session):

    session.query(ProjectCourseAlignment).filter(ProjectCourseAlignment.course_id == course_id).delete()
        
