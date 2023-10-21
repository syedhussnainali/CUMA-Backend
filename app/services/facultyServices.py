from flask import jsonify
from ..model.faculty import Faculty
from app.services.dbServices import createSession,closeSession
import json
from sqlalchemy.exc import SQLAlchemyError

def getAllFaculty():
    try:
        session = createSession()
        faculty_data = session.query(Faculty).all()
        closeSession(session)

        faculty_list = []
        for data in faculty_data:
            faculty_list.append({"id": data.id, "name": data.name})

        # Convert the list to a JSON array
        faculty_list = json.dumps(faculty_list)
        return faculty_list
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch faculty", "message": str(e)}), 500


def getFacultyByID(id):
    try:
        session = createSession()
        faculty = session.query(Faculty).get(id)
        closeSession(session)

        if faculty is None:
            return jsonify({"error": "Faculty not found"})

        faculty_data = {"id": faculty.id, "name": faculty.name}
        return jsonify(faculty_data)
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch faculty", "message": str(e)}), 500

def addFaculty(faculty):
    try:
        session = createSession()
        new_faculty = Faculty(name=faculty.name)
        session.add(new_faculty)
        session.commit()
        closeSession(session)
        return jsonify({"success": "Faculty added successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to add faculty", "message": str(e)}), 500


def updateFacultyByID(newfaculty):
    try:
        session = createSession()
        faculty = session.query(Faculty).get(newfaculty.id)

        if faculty is None:
            return jsonify({"error": "Faculty not found"})

        faculty.name = newfaculty.name
        session.commit()
        closeSession(session)
        return jsonify({"success": "Faculty updated successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to update faculty", "message": str(e)}), 500


def deleteFacultyByID(id):
    try:
        session = createSession()
        faculty = session.query(Faculty).get(id)

        if faculty is None:
            return jsonify({"error": "Faculty not found"})

        session.delete(faculty)
        session.commit()
        closeSession(session)
        return jsonify({"success": "Faculty deleted successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to delete faculty", "message": str(e)}), 500
