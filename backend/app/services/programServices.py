from flask import jsonify
from ..model.program import Program
from ..model.projectProgram import ProjectProgram
from ..model.project_course import ProjectCourse
from ..model.faculty import Faculty
from ..model.project import Project
from ..model.projectProgramAlignment import ProjectProgramAlignment
from ..model.programAlignment import ProgramAlignment
from ..model.projectProgramCourseXref import ProjectProgramCourseXref
from app.services.dbServices import createSession, closeSession
from sqlalchemy.exc import SQLAlchemyError
from .project_permissionservices import checkPermissions
from .utils import getSessionUserID
from sqlalchemy import and_, or_
from .projectProgramAlignmentServices import getProjectProgramAlignmentsByProgramID,addProjectProgramAlignments,deleteProjectProgramAlignments
from datetime import datetime

def getAllProgramsOfProject(project_id):
    try:
        session = createSession()
        program_data = session.query(ProjectProgram).filter(ProjectProgram.project_id == project_id).all()
        closeSession(session)
        program_list = []
        for data in program_data:
            program_list.append({
                "id": data.id,
                "project_id": data.project_id,
                "name": data.name,
                "academic_level": data.academic_level,
                "faculty_id": data.faculty_id,
                "document_id": data.document_id,
                "latest_modified": data.latest_modified.strftime("%Y-%m-%d"),
                "revision_start_date": data.revision_start_date.strftime("%Y-%m-%d"),
                "state": data.state,
                "parent_program_id": data.parent_program_id
            })

        return program_list
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch programs", "message": str(e)}), 500


def getProjectProgramByID(project_id, program_id):
    try:    
        session = createSession()
        
        if not checkPermissions(project_id, getSessionUserID(), session, False):
            return jsonify({"error": "Permission Denied"}), 500
        
        leftCondition = ProjectProgram.project_id == project_id
        rightCondition = ProjectProgram.id == program_id
        condition = and_(leftCondition, rightCondition)
        program_data = session.query(ProjectProgram) \
            .filter(condition) \
            .first()
        closeSession(session)
        
        if program_data is None:
            return jsonify({"error": "Program not found"})
        
        program = ({
                "program_id": program_data.id,
                "project_id": program_data.project_id,
                "name": program_data.name,
                "academic_level": program_data.academic_level,
                "faculty_id": program_data.faculty_id,
                "document_id": program_data.document_id,
                "latest_modified": program_data.latest_modified,
                "revision_start_date": program_data.revision_start_date.strftime("%Y-%m-%d"),
                "state": program_data.state,
                "parent_program_id": program_data.parent_program_id,
                "UGA_alignments": getProjectProgramAlignmentsByProgramID(program_data.id)
            })
        return program
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch programs", "message": str(e)}), 500


def addProjectProgram(project_program, alignments):
    try:
        session = createSession()

        if not checkPermissions(project_program.project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500
        
        new_project_program = ProjectProgram(
            project_id=project_program.project_id,
            name=project_program.name,
            academic_level=project_program.academic_level,
            faculty_id=project_program.faculty_id,
            document_id=project_program.document_id,
            latest_modified=project_program.latest_modified,
            revision_start_date=project_program.revision_start_date,
            state=project_program.state,
            parent_program_id=project_program.parent_program_id
        )
        session.add(new_project_program)
        session.flush()

        print(addProjectProgramAlignments(alignments, new_project_program.id, session))
        session.commit()
        closeSession(session)
        return jsonify({"success": "Project Program added successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to add Project Program", "message": str(e)}), 500


def updateProjectProgramByID(project_program, alignments):
    try:
        session = createSession()

        if not checkPermissions(project_program.project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500

        existing_project_program = session.query(ProjectProgram).get(project_program.id)

        if existing_project_program is None:
            return jsonify({"error": "Project Program not found"})

        existing_project_program.name = project_program.name
        existing_project_program.academic_level = project_program.academic_level
        existing_project_program.faculty_id = project_program.faculty_id
        existing_project_program.document_id = project_program.document_id
        existing_project_program.latest_modified = project_program.latest_modified
        existing_project_program.revision_start_date = project_program.revision_start_date
        existing_project_program.state = project_program.state
        existing_project_program.parent_program_id = project_program.parent_program_id

        deleteProjectProgramAlignments(existing_project_program.id, session)
        print(addProjectProgramAlignments(alignments, existing_project_program.id, session))
        session.commit()
        closeSession(session)
        return jsonify({"success": "Program updated successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to update program", "message": str(e)}), 500


def deleteProgramByID(id):
    try:
        session = createSession()
        program = session.query(Program).get(id)

        if program is None:
            return jsonify({"error": "Program not found"})

        session.delete(program)
        session.commit()
        closeSession(session)
        return jsonify({"success": "Program deleted successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to delete program", "message": str(e)}), 500

def searchProjectProgram(search_query):
    try:
        session = createSession()

        search_results = session.query(Program).filter(
            or_(
                Program.name.ilike(f"%{search_query}%"),
            )
        ).all()

        result_list = []
        for result in search_results:
            result_dict = {
                "id": result.id,
                "name": result.name,
                "academic_level": result.academic_level,
                "faculty_id": result.faculty_id,
                "document_id": result.document_id,
                "latest_modified": result.latest_modified.strftime("%Y-%m-%d") if result.latest_modified else None,
                "state": result.state
            }
            result_list.append(result_dict)

        closeSession(session)
        return jsonify(result_list)
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to search Project Program", "message": str(e)}), 500


def copyProgramsToProject(project_id, program_ids):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500
        
        project = session.query(Project).get(project_id)
        if project is None:
            return jsonify({"error": "Project not found"})
        
        for program_id in program_ids:
            program = session.query(Program).get(program_id)
            if program is None:
                continue

            new_project_program = ProjectProgram(
                project_id=project_id,
                parent_program_id=program.id,
                name=program.name,
                academic_level=program.academic_level,
                document_id=program.document_id,
                latest_modified=program.latest_modified,
                revision_start_date=datetime.now().date(),
                state=program.state,
                faculty_id=program.faculty_id
            )
            session.add(new_project_program)

            alignments = session.query(ProgramAlignment).filter_by(program_id=program.id).all()
            for alignment in alignments:
                new_alignment = ProjectProgramAlignment(
                    program_id=new_project_program.id,
                    legend=alignment.legend,
                    description=alignment.description
                )
                session.add(new_alignment)
        
        session.commit()
        closeSession(session)
        return jsonify({"success": "Programs copied to project successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to copy programs to project", "message": str(e)}), 500


def beginRevisionProgram(project_id, program_id):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500

        project_program = session.query(ProjectProgram).filter_by(project_id=project_id, id=program_id).first()

        if project_program is None:
            return jsonify({"error": "Project Program not found"})

        project_program.state = "draft"
        project_program.latest_modified = datetime.now()
        session.commit()
        closeSession(session)

        return jsonify({"success": "Revision started successfully"})

    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to begin revision", "message": str(e)}), 500


def mapCoursesToPrograms(project_id, mapping):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500
        
        project = session.query(Project).get(project_id)
        if project is None:
            return jsonify({"error": "Project not found"})

        for program_id, courses in mapping.items():
            
            session.query(ProjectProgramCourseXref).filter_by(project_id=project_id, program_id = program_id).delete()
            for course_info in courses:
                course_id = course_info[0]
                core_flag = course_info[1]
                
                xref_entry = ProjectProgramCourseXref(
                    project_id=project_id,
                    program_id=program_id,
                    course_id=course_id,
                    core=core_flag
                )
                session.add(xref_entry)

        session.commit()
        closeSession(session)
        return jsonify({"success": "Courses mapped to programs successfully"})

    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to map courses to programs", "message": str(e)}), 500


def deleteProjectProgram(project_program_id, project_id):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500
        
        project_program = session.query(ProjectProgram).get(project_program_id)

        if project_program is None:
            return jsonify({"error": "Project Program not found"})

        # Delete mappings in projectprogramcourscxref for the specified project program
        session.query(ProjectProgramCourseXref).filter_by(project_id=project_id, program_id=project_program_id).delete()
        deleteProjectProgramAlignments(project_program_id, session)
        session.delete(project_program)
        session.commit()
        closeSession(session)
        
        return jsonify({"success": "Project Program deleted successfully"})
    
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to delete project program", "message": str(e)}), 500

def getAllProgramsCoursesOfProject(project_id):
    try:
        session = createSession()
        program_data = session.query(ProjectProgram).filter(ProjectProgram.project_id == project_id).all()
        closeSession(session)
        
        program_list = []
        for data in program_data:
            program_courses = getProgramCourses(project_id, data.id) 
            print(program_courses)

            program_list.append({
                "id": data.id,
                "project_id": data.project_id,
                "name": data.name,
                "academic_level": data.academic_level,
                "faculty_id": data.faculty_id,
                "document_id": data.document_id,
                "latest_modified": data.latest_modified.strftime("%Y-%m-%d"),
                "revision_start_date": data.revision_start_date.strftime("%Y-%m-%d"),
                "state": data.state,
                "parent_program_id": data.parent_program_id,
                "courses": program_courses  # Add the courses linked to the program to the result
            })

        return program_list
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch programs", "message": str(e)}), 500

def getProgramCourses(project_id, program_id):
    try:
        session = createSession()
        program_courses = (
            session.query(ProjectProgramCourseXref)
            .filter(ProjectProgramCourseXref.program_id == program_id)
            .filter(ProjectProgramCourseXref.project_id == project_id)
            .all()
        )
        print(program_courses)
        course_list = []
        for course_xref in program_courses:
            course = session.query(ProjectCourse).get(course_xref.course_id)
            if course:
                course_list.append({
                    "course_id": course.id,
                    "course_name": course.name,
                    "core": course_xref.core
                })

        closeSession(session)
        print(course_list)
        return course_list
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch program courses", "message": str(e)}), 500
