from flask import jsonify
from ..model.ugaAlignments import UgaAlignments
from app.services.dbServices import createSession,closeSession
import json
from sqlalchemy.exc import SQLAlchemyError

def getAllUgaAlignments():
    try:
        session = createSession()
        uga_data = session.query(UgaAlignments).all()
        closeSession(session)

        uga_list = []
        for data in uga_data:
            uga_list.append({"id": data.id, "legend": data.legend, "description": data.description})

        # Convert the list to a JSON array
        uga_list = json.dumps(uga_list)
        return uga_list
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch UGA alignments", "message": str(e)}), 500


def getUgaAlignmentByID(id):
    try:
        session = createSession()
        uga_alignment = session.query(UgaAlignments).get(id)
        closeSession(session)

        if uga_alignment is None:
            return jsonify({"error": "UGA alignment not found"}), 500

        uga_data = {"id": uga_alignment.id, "legend": uga_alignment.legend, "description": uga_alignment.description}
        return jsonify(uga_data)
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch UGA alignment", "message": str(e)}), 500


#TODO further testing needed (not tested yet)
def addUgaAlignment(uga_alignment):
    try:
        session = createSession()
        new_uga_alignment = UgaAlignments(id=uga_alignment.id, legend=uga_alignment.legend, description=uga_alignment.description)
        session.add(new_uga_alignment)
        session.commit()
        closeSession(session)
        return jsonify({"success": "UGA alignment added successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to add UGA alignment", "message": str(e)}), 500


#TODO further testing needed (not tested yet)
def updateUgaAlignmentByID(new_uga_alignment):
    try:
        session = createSession()
        uga_alignment = session.query(UgaAlignments).get(new_uga_alignment.id)

        if uga_alignment is None:
            return jsonify({"error": "UGA alignment not found"})

        uga_alignment.legend = new_uga_alignment.legend
        uga_alignment.description = new_uga_alignment.description
        session.commit()
        closeSession(session)
        return jsonify({"success": "UGA alignment updated successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to update UGA alignment", "message": str(e)}), 500


#TODO further testing needed (not tested yet)
def deleteUgaAlignmentByID(id):
    try:
        session = createSession()
        uga_alignment = session.query(UgaAlignments).get(id)

        if uga_alignment is None:
            return jsonify({"error": "UGA alignment not found"})

        session.delete(uga_alignment)
        session.commit()
        closeSession(session)
        return jsonify({"success": "UGA alignment deleted successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to delete UGA alignment", "message": str(e)}), 500
