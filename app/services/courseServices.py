from flask import jsonify
from ..model.course import Course
from ..model.project_course import ProjectCourse
from ..model.project import Project
from ..model.project_course_alignments import ProjectCourseAlignment
from ..model.courseAlignments import CourseAlignment
from .projectCourseAlignmentServices import (
    getProjectCourseAlignmentsByCourseID,
    addProjectCourseAlignments,
    deleteProjectCourseAlignments,
)
from app.services.dbServices import createSession, closeSession
from .project_permissionservices import checkPermissions
from .utils import getSessionUserID
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_
from ..model.projectProgramCourseXref import ProjectProgramCourseXref


def getAllCoursesOfProject(project_id):
    try:
        session = createSession()
        course_data = (
            session.query(ProjectCourse)
            .filter(ProjectCourse.project_id == project_id)
            .all()
        )
        closeSession(session)
        course_list = []
        for data in course_data:
            course_list.append(
                {
                    "id": data.id,
                    "project_id": data.project_id,
                    "course_code": data.course_code,
                    "also_known_as": data.also_known_as,
                    "formerly_known_as": data.formerly_known_as,
                    "name": data.name,
                    "document_id": data.document_id,
                    "revision_start_date": data.revision_start_date.strftime(
                        "%Y-%m-%d"
                    ),
                    "latest_modified": data.latest_modified,
                    "state": data.state,
                    "parent_course_id": data.parent_course_id,
                }
            )

        return course_list
    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch courses", "message": str(e)}), 500


def getAllCourses():
    try:

        session = createSession()
        course_data = session.query(Course).all()
        closeSession(session)

        course_list = []
        for data in course_data:
            course_list.append(
                {
                    "id": data.id,
                    "course_code": data.course_code,
                    "also_known_as": data.also_known_as,
                    "formerly_known_as": data.formerly_known_as,
                    "name": data.name,
                    "document_id": data.document_id,
                    "latest_modified": data.latest_modified,
                    "state": data.state,
                }
            )

        return course_list

    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch courses", "message": str(e)}), 500


def getProjectCourseByID(project_id, course_id):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, False):
            return jsonify({"error": "Permission Denied"}), 500

        leftCondition = ProjectCourse.project_id == project_id
        rightCondition = ProjectCourse.id == course_id
        condition = and_(leftCondition, rightCondition)
        course_data = session.query(ProjectCourse).filter(condition).first()
        closeSession(session)

        if course_data is None:
            return jsonify({"error": "Course not found"})

        course = {
            "course_id": course_data.id,
            "project_id": course_data.project_id,
            "course_code": course_data.course_code,
            "also_known_as": course_data.also_known_as,
            "formerly_known_as": course_data.formerly_known_as,
            "name": course_data.name,
            "document_id": course_data.document_id,
            "revision_start_date": course_data.revision_start_date.strftime("%Y-%m-%d"),
            "latest_modified": course_data.latest_modified,
            "state": course_data.state,
            "parent_course_id": course_data.parent_course_id,
            "UGA_alignments": getProjectCourseAlignmentsByCourseID(course_data.id),
        }
        return course

    except SQLAlchemyError as e:
        return jsonify({"error": "Failed to fetch courses", "message": str(e)}), 500


def addProjectCourse(project_course, alignments):
    session = createSession()  # Start a new session
    try:
        # Check permissions before proceeding
        if not checkPermissions(
            project_course.project_id, getSessionUserID(), session, True
        ):
            # If permission check fails, return 403 Forbidden
            return jsonify({"error": "Permission Denied"}), 403

        # Proceed with adding the project course
        new_project_course = ProjectCourse(
            project_id=project_course.project_id,
            course_code=project_course.course_code,
            also_known_as=project_course.also_known_as,
            formerly_known_as=project_course.formerly_known_as,
            name=project_course.name,
            document_id=project_course.document_id,
            revision_start_date=project_course.revision_start_date,
            latest_modified=project_course.latest_modified,
            state=project_course.state,
            parent_course_id=project_course.parent_course_id,
        )
        session.add(new_project_course)
        # Flush to get the new project course ID
        session.flush()

        # Add project course alignments
        alignment_result = addProjectCourseAlignments(
            alignments, new_project_course.id, session
        )
        # Log or handle the result as needed
        print(alignment_result)
        # Commit the transaction
        session.commit()
        return jsonify({"success": "Project Course added successfully"}), 200
    except SQLAlchemyError as e:
        # Rollback in case of error
        session.rollback()
        # Log the error for debugging
        print(f"SQLAlchemy Error: {e}")
        return (
            jsonify({"error": "Failed to add Project Course", "message": str(e)}),
            500,
        )
    finally:
        # Ensure the session is closed in any case
        closeSession(session)


def updateProjectCourseByID(project_course, alignments):
    try:
        session = createSession()

        if not checkPermissions(
            project_course.project_id, getSessionUserID(), session, True
        ):
            return jsonify({"error": "Permission Denied"}), 500

        existing_project_course = session.query(ProjectCourse).get(project_course.id)

        if existing_project_course is None:
            return jsonify({"error": "Project Course not found"})

        existing_project_course.course_code = project_course.course_code
        existing_project_course.also_known_as = project_course.also_known_as
        existing_project_course.formerly_known_as = project_course.formerly_known_as
        existing_project_course.name = project_course.name
        existing_project_course.document_id = project_course.document_id
        existing_project_course.revision_start_date = project_course.revision_start_date
        existing_project_course.latest_modified = project_course.latest_modified
        existing_project_course.state = project_course.state
        existing_project_course.parent_course_id = project_course.parent_course_id

        deleteProjectCourseAlignments(existing_project_course.id, session)
        print(
            addProjectCourseAlignments(alignments, existing_project_course.id, session)
        )
        session.commit()
        closeSession(session)
        return jsonify({"success": "Course updated successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to update course", "message": str(e)}), 500


def deleteProjectCourse(project_course_id, project_id):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 403

        project_course = session.query(ProjectCourse).get(project_course_id)

        if project_course is None:
            return jsonify({"error": "Project Course not found"})

        session.query(ProjectProgramCourseXref).filter_by(
            project_id=project_id, course_id=project_course_id
        ).delete(synchronize_session=False)
        deleteProjectCourseAlignments(project_course_id, session)
        session.delete(project_course)
        session.commit()
        closeSession(session)
        return jsonify({"success": "project Course deleted successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to delete course", "message": str(e)}), 500


def searchProjectCourse(search_query):
    try:
        session = createSession()

        search_results = (
            session.query(Course)
            .filter(
                or_(
                    Course.course_code.ilike(f"%{search_query}%"),
                    Course.also_known_as.ilike(f"%{search_query}%"),
                    Course.formerly_known_as.ilike(f"%{search_query}%"),
                    Course.name.ilike(f"%{search_query}%"),
                    Course.document_id.ilike(f"%{search_query}%"),
                )
            )
            .all()
        )

        result_list = []
        for result in search_results:
            result_dict = {
                "id": result.id,
                "course_code": result.course_code,
                "also_known_as": result.also_known_as,
                "formerly_known_as": result.formerly_known_as,
                "name": result.name,
                "document_id": result.document_id,
                "latest_modified": (
                    result.latest_modified.strftime("%Y-%m-%d")
                    if result.latest_modified
                    else None
                ),
                "state": result.state,
            }
            result_list.append(result_dict)

        closeSession(session)
        return jsonify(result_list)
    except SQLAlchemyError as e:
        return (
            jsonify({"error": "Failed to search Project Course", "message": str(e)}),
            500,
        )


def copyCoursesToProject(project_id, course_ids):
    try:
        session = createSession()

        # if not checkPermissions(project_id, getSessionUserID(), session, True):
        #     return jsonify({"error": "Permission Denied"}), 500

        project = session.query(Project).get(project_id)
        if project is None:
            return jsonify({"error": "Project not found"})

        for course_id in course_ids:
            course = session.query(Course).get(course_id)
            if course is None:
                continue

            new_project_course = ProjectCourse(
                project_id=project_id,
                parent_course_id=course.id,
                course_code=course.course_code,
                also_known_as=course.also_known_as,
                formerly_known_as=course.formerly_known_as,
                name=course.name,
                document_id=course.document_id,
                revision_start_date=datetime.now().date(),
                latest_modified=course.latest_modified,
                state=course.state,
            )
            session.add(new_project_course)

            alignments = (
                session.query(CourseAlignment).filter_by(course_id=course_id).all()
            )
            for alignment in alignments:
                new_alignment = ProjectCourseAlignment(
                    course_id=new_project_course.id,
                    legend=alignment.legend,
                    description=alignment.description,
                )
                session.add(new_alignment)

        session.commit()
        closeSession(session)
        return jsonify({"success": "Courses copied to project successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return (
            jsonify({"error": "Failed to copy courses to project", "message": str(e)}),
            500,
        )


def beginRevision(project_id, course_id):
    try:
        session = createSession()

        if not checkPermissions(project_id, getSessionUserID(), session, True):
            return jsonify({"error": "Permission Denied"}), 500

        project_course = (
            session.query(ProjectCourse)
            .filter_by(project_id=project_id, id=course_id)
            .first()
        )

        if project_course is None:
            return jsonify({"error": "Project Course not found"})

        project_course.state = "draft"
        project_course.latest_modified = datetime.now()
        session.commit()
        closeSession(session)

        return jsonify({"success": "Revision started successfully"})

    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to begin revision", "message": str(e)}), 500


def deleteCourseByID(id):
    try:
        session = createSession()
        course = session.query(Course).get(id)

        if course is None:
            return jsonify({"error": "Course not found"})

        session.delete(course)
        session.commit()
        closeSession(session)
        return jsonify({"success": "Course deleted successfully"})
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to delete course", "message": str(e)}), 500
