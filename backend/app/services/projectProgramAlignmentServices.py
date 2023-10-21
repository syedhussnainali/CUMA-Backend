from flask import jsonify
from ..model.projectProgramAlignment import ProjectProgramAlignment
from app.services.dbServices import createSession, closeSession
from sqlalchemy.exc import SQLAlchemyError

def getProjectProgramAlignmentsByProgramID(program_id):
    try:
        session = createSession()
        alignments = session.query(ProjectProgramAlignment).filter(ProjectProgramAlignment.program_id == program_id).all()
        closeSession(session)

        if not alignments:
            return []

        alignment_data = []
        for alignment in alignments:
            alignment_data.append({
                "id": alignment.id,
                "program_id": alignment.program_id,
                "legend": alignment.legend,
                "description": alignment.description
            })
        return alignment_data
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch Project Program Alignments", "message": str(e)}), 500

def addProjectProgramAlignments(alignments, id, session=None):
    try:
        for alignment in alignments:
            new_alignment = ProjectProgramAlignment(
                program_id=id,
                legend=alignment['legend'],
                description=alignment['description']
            )
            session.add(new_alignment)

        return "Alignments added"
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        print(str(e))
        return jsonify({"error": "Failed to add ProjectProgramAlignments", "message": str(e)}), 500

def deleteProjectProgramAlignments(program_id, session):
    session.query(ProjectProgramAlignment).filter(ProjectProgramAlignment.program_id == program_id).delete()
