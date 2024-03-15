from app import app, conn
from app.services.facultyServices import (
    getFacultyByID,
    getAllFaculty,
    addFaculty,
    updateFacultyByID,
    deleteFacultyByID,
)
from app.services.courseServices import (
    getAllCoursesOfProject,
    getProjectCourseByID,
    addProjectCourse,
    updateProjectCourseByID,
    deleteProjectCourse,
    searchProjectCourse,
    copyCoursesToProject,
    beginRevision,
    getAllCourses,
    deleteCourseByID,
)
from app.services.programServices import (
    getAllProgramsOfFaculty,
    getAllProgramsOfProject,
    getProjectProgramByID,
    addProjectProgram,
    updateProjectProgramByID,
    deleteProgramByID,
    searchProjectProgram,
    copyProgramsToProject,
    beginRevisionProgram,
    mapCoursesToPrograms,
    deleteProjectProgram,
    getAllProgramsCoursesOfProject,
    getAllPrograms,
    getCount,
)
from app.services.projectServices import (
    addProject,
    get_projects_of_user,
    get_project_by_ID,
    update_project,
)
from app.services.ugaAlignmentServices import (
    getUgaAlignmentByID,
    getAllUgaAlignments,
    addUgaAlignment,
    updateUgaAlignmentByID,
    deleteUgaAlignmentByID,
)
from flask import request, jsonify, session
from datetime import datetime

from app.model.faculty import Faculty
from app.model.project_course import ProjectCourse
from app.model.projectProgram import ProjectProgram
from app.model.program import Program
from app.model.project import Project
from app.model.project_permissions import ProjectPermissions


@app.route("/test", methods=["GET"])
def test():
    return "testing"


def validate_login():
    return True
    # print(session)
    # if 'user_id' in session:
    #     return True
    # else:
    #     return False


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    uwinid = data["uwinid"]
    password = data["password"]
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM login_uwin WHERE uwinid=%s AND password=%s", (uwinid, password)
    )
    user = cur.fetchone()
    print(user, data)
    cur.close()
    if user:
        session["user_id"] = user[1]
        print("session created->", session)
        return jsonify(
            {
                "message": "Login successful!",
                "success": "true",
                "username": user[1][0 : user[1].find("@")],
            }
        )
    else:
        return jsonify({"message": "Invalid username or password", "success": "false"})


##API to know wether a user is logged or not
@app.route("/status")
def session_status():
    if not validate_login():
        return getAllCourses()
        # return jsonify({'message': 'User not logged in'}), 401
    else:
        return jsonify("ok"), 200


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logout successful!", "success": "true"})


##
# http://localhost:5000/faculty_list
##
@app.route("/faculty_list", methods=["GET"])
def get_faculty_list():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        return getAllFaculty(), 200


##
# http://localhost:5000/faculty_list_by_id?id=4
##
@app.route("/faculty_list_by_id", methods=["GET"])
def get_faculty_list_by_id():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.args.get("id")
        if id is None:
            return jsonify({"message": "Missing ID parameter"}), 400

        return getFacultyByID(id), 200


##
# http://localhost:5000/addFaculty
# {
#    "name": "testFaculty"
# }
##
@app.route("/addFaculty", methods=["POST"])
def addFaculty_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        name = request.json["name"]
        faculty = Faculty(name=name)
        if name is None:
            return jsonify({"message": "Missing name parameter"}), 400

        return addFaculty(faculty), 200


##
# http://localhost:5000/updatefaculty
# {
#    "name": "testFacultynew",
#    "id": 10
# }
##
@app.route("/updatefaculty", methods=["POST"])
def updatefaculty():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.json["id"]
        name = request.json["name"]
        faculty = Faculty(id=id, name=name)
        if name is None or id is None:
            return jsonify({"message": "Missing name or id parameter"}), 400

        return updateFacultyByID(faculty), 200


##
# http://localhost:5000/deletefaculty
# {
#    "id": 10
# }
##
@app.route("/deletefaculty", methods=["POST"])
def deletefaculty():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.json["id"]
        if id is None:
            return jsonify({"message": "Missing id parameter"}), 400

        return deleteFacultyByID(id)


##
# http://localhost:5000/getAllCoursesOfProject?id=4
##
@app.route("/getAllCoursesOfProject", methods=["GET"])
def getAllCoursesOfProject_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.args.get("id")
        return getAllCoursesOfProject(id)


##
@app.route("/getAllCourses", methods=["GET"])
def getAllCourses_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        return getAllCourses()


##
# http://localhost:5000/getProjectCourseByID?project_id=4&course_id=1
##
@app.route("/getProjectCourseByID", methods=["GET"])
def getProjectCourseByID_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        project_id = int(request.args.get("project_id"))
        course_id = int(request.args.get("course_id"))
        if id is None:
            return jsonify({"message": "Missing ID parameter"}), 400

        return getProjectCourseByID(project_id, course_id)


##
# http://localhost:5000/addProjectCourse
# {
#     "project_id": 19,
#     "course_code": "CSE101",
#     "also_known_as": "Intro to Computer Science",
#     "formerly_known_as": "CS101",
#     "name": "Computer Science Fundamentals",
#     "document_id": "DOC001",
#     "revision_start_date": "2023-06-01",
#     "latest_modified": "2023-06-01" #assign current date
#     "state": "draft" #default for newely creating projects
#     "parent_course_id": null # default null for newly created projects
#     "alignments" :
# [
#         {
#             "description": "Interpret mathematically about basic (discrete) structures used in Computer Science.",
#             "legend": "C"
#         },
#         {
#             "description": "Calculate the computational time complexity of algorithms (also relevant to Section A).\n",
#             "legend": "CA"
#         }
#     ]
# }
##
@app.route("/addProjectCourse", methods=["POST"])
def addProjectCourse_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        try:
            project_id = request.json["project_id"]
            course_code = request.json["course_code"]
            also_known_as = request.json.get(
                "also_known_as"
            )  # Use get for optional fields
            formerly_known_as = request.json.get(
                "formerly_known_as"
            )  # Use get for optional fields
            name = request.json["name"]
            document_id = request.json.get("document_id")  # Use get for optional fields
            revision_start_date_str = request.json.get(
                "revision_start_date", datetime.now().strftime("%Y-%m-%d")
            )
            # Parse date strings to date objects
            revision_start_date = datetime.strptime(
                revision_start_date_str.split("T")[0], "%Y-%m-%d"
            ).date()

            latest_modified_str = request.json.get(
                "latest_modified", datetime.now().strftime("%Y-%m-%d")
            )  # Default to now if not provided

            latest_modified = datetime.strptime(
                latest_modified_str.split("T")[0], "%Y-%m-%d"
            ).date()
            state = request.json.get("state")  # Use get for optional fields
            alignments = request.json.get(
                "alignments", []
            )  # Default to empty list if not provided
            parent_course_id = request.json.get(
                "parent_course_id"
            )  # Use get for optional fields

            if any(
                value is None
                for value in [project_id, course_code, name, revision_start_date_str]
            ):
                return jsonify({"message": "Missing required parameters"}), 400

            projectCourse = ProjectCourse(
                project_id=project_id,
                course_code=course_code,
                also_known_as=also_known_as,
                formerly_known_as=formerly_known_as,
                name=name,
                document_id=document_id,
                revision_start_date=revision_start_date,
                latest_modified=latest_modified,
                state=state,
                parent_course_id=parent_course_id,
            )

            # Attempt to add the project course and alignments
            response = addProjectCourse(projectCourse, alignments)
            return response

        except Exception as e:
            print(f"Error adding project course: {e}")  # Ideally, use proper logging
            return (
                jsonify(
                    {"message": "Failed to add project course, internal server error"}
                ),
                500,
            )


##
# http://localhost:5000/updateProjectCourseByID
# {   "id":12,
#     "project_id": 19,
#     "course_code": "CSE101",
#     "also_known_as": "Intro to Computer Science",
#     "formerly_known_as": "CS101",
#     "name": "Computer Science Fundamentals",
#     "document_id": "DOC001",
#     "revision_start_date": "2023-06-01",
#     "latest_modified": "2023-06-01" #assign current date
#     "state": "draft" #default for newely creating projects
#     "parent_course_id": 1,
#     "alignments" :
# [
#         {
#             "description": "Interpret mathematically about basic (discrete) structures used in Computer Science.",
#             "legend": "C"
#         },
#         {
#             "description": "Calculate the computational time complexity of algorithms (also relevant to Section A).\n",
#             "legend": "CA"
#         }
#     ]
# }
##
@app.route("/updateProjectCourseByID", methods=["POST"])
def updateProjectCourseByID_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.json["id"]
        project_id = request.json["project_id"]
        course_code = request.json["course_code"]
        also_known_as = request.json["also_known_as"]
        formerly_known_as = request.json["formerly_known_as"]
        name = request.json["name"]
        document_id = request.json["document_id"]
        revision_start_date = request.json["revision_start_date"]
        latest_modified = request.json["latest_modified"]
        state = request.json["state"]
        alignments = request.json["alignments"]
        parent_course_id = request.json["parent_course_id"]

        projectCourse = ProjectCourse(
            id=id,
            project_id=project_id,
            course_code=course_code,
            also_known_as=also_known_as,
            formerly_known_as=formerly_known_as,
            name=name,
            document_id=document_id,
            revision_start_date=revision_start_date,
            latest_modified=latest_modified,
            state=state,
            parent_course_id=parent_course_id,
        )

        if any(value is None for value in [id, course_code, name, alignments]):
            return jsonify({"message": "Missing required parameters"}), 400

        return updateProjectCourseByID(projectCourse, alignments)


##
# http://localhost:5000/deleteProjectCourse
# {
#     "project_course_id": 10,
#     "project_id": 10
# }
##
@app.route("/deleteProjectCourse", methods=["POST"])
def deleteProjectCourse_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        project_course_id = request.json["project_course_id"]
        project_id = request.json["project_id"]
        if id is None:
            return jsonify({"message": "Missing id parameter"}), 400

        return deleteProjectCourse(project_course_id, project_id)


##
# http://localhost:5000/searchProjectCourse?search_query=test-100
##
@app.route("/searchProjectCourse", methods=["GET"])
def searchProjectCourse_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    search_query = request.args.get("search_query")

    return searchProjectCourse(search_query)


##
# http://localhost:5000/copyCoursesToProject
# {
#     "project_id":"19",
#     "course_ids":[2]
# }
@app.route("/copyCoursesToProject", methods=["POST"])
def copyCoursesToProject_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    try:
        # Get the project ID and course IDs from the request
        data = request.json
        project_id = data.get("project_id")
        course_ids = data.get("course_ids")

        if project_id is None or course_ids is None:
            return jsonify({"message": "Missing project ID or course IDs"}), 400

        # Call the function to copy the courses to the project
        result = copyCoursesToProject(project_id, course_ids)
        return result

    except Exception as e:
        return (
            jsonify({"error": "Failed to copy courses to project", "message": str(e)}),
            500,
        )


##
# http://localhost:5000/beginRevision
# {
#     "project_id":"19",
#     "course_id":2
# }
@app.route("/beginRevision", methods=["POST"])
def beginRevision_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    project_id = request.json.get("project_id")
    course_id = request.json.get("course_id")

    if project_id is None or course_id is None:
        return jsonify({"error": "Missing project_id or course_id parameter"}), 400

    return beginRevision(project_id, course_id)


##
# http://localhost:5000/getAllProgramsOfProject?id=19
##
@app.route("/getAllProgramsOfProject", methods=["GET"])
def getAllProgramsOfProject_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.args.get("id")
        return getAllProgramsOfProject(id)


##
# http://localhost:5000/getProjectProgramByID?project_id=19&program_id=1
##
@app.route("/getProjectProgramByID", methods=["GET"])
def getProjectProgramByID_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        project_id = request.args.get("project_id")
        program_id = request.args.get("program_id")
        if project_id is None:
            return jsonify({"message": "Missing ID parameter"}), 400

        return getProjectProgramByID(project_id, program_id)


##
# http://localhost:5000/addProjectProgram
# {
#     "project_id": 19,
#     "name": "Computer Science Program",
#     "academic_level": "Undergraduate",
#     "faculty_id": 5,
#     "document_id": "DOC002",
#     "latest_modified": "2023-06-01",  # assign current date
#     "revision_start_date": "2023-06-01",
#     "state": "draft",  # default for newly creating projects
#     "parent_program_id": null,  # default null for newly created projects
#     "alignments": [
#         {
#             "legend": "C",
#             "description": "Interpret mathematically about basic (discrete) structures used in Computer Science."
#         },
#         {
#             "legend": "CA",
#             "description": "Calculate the computational time complexity of algorithms (also relevant to Section A).\n"
#         }
#     ]
# }
##
@app.route("/addProjectProgram", methods=["POST"])
def addProjectProgram_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        project_id = request.json["project_id"]
        name = request.json["name"]
        academic_level = request.json["academic_level"]
        faculty_id = request.json["faculty_id"]
        document_id = request.json["document_id"]
        latest_modified = request.json["latest_modified"]
        revision_start_date = request.json["revision_start_date"]
        state = request.json["state"]
        alignments = request.json["alignments"]
        parent_program_id = request.json["parent_program_id"]

        projectProgram = ProjectProgram(
            project_id=project_id,
            name=name,
            academic_level=academic_level,
            faculty_id=faculty_id,
            document_id=document_id,
            latest_modified=latest_modified,
            revision_start_date=revision_start_date,
            state=state,
            parent_program_id=parent_program_id,
        )

        if any(value is None for value in [name]):
            return jsonify({"message": "Missing required parameters"}), 400

        return addProjectProgram(projectProgram, alignments)


##
# http://localhost:5000/updateProjectProgramByID
# {
#     "id": 1,
#     "project_id": 19,
#     "name": "Computer Science Program",
#     "academic_level": "Undergraduate",
#     "faculty_id": 5,
#     "document_id": "DOC002",
#     "latest_modified": "2023-06-01",  # assign current date
#     "revision_start_date": "2023-06-01",
#     "state": "draft",  # default for newly creating projects
#     "parent_program_id": null,  # default null for newly created projects
#     "alignments": [
#         {
#             "legend": "C",
#             "description": "Interpret mathematically about basic (discrete) structures used in Computer Science."
#         },
#         {
#             "legend": "CA",
#             "description": "Calculate the computational time complexity of algorithms (also relevant to Section A).\n"
#         }
#     ]
# }
##
@app.route("/updateProjectProgramByID", methods=["POST"])
def updateProjectProgramByID_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.json["id"]
        project_id = request.json["project_id"]
        name = request.json["name"]
        academic_level = request.json["academic_level"]
        faculty_id = request.json["faculty_id"]
        document_id = request.json["document_id"]
        latest_modified = request.json["latest_modified"]
        revision_start_date = request.json["revision_start_date"]
        state = request.json["state"]
        parent_program_id = request.json["parent_program_id"]
        alignments = request.json["alignments"]

        projectProgram = ProjectProgram(
            id=id,
            project_id=project_id,
            name=name,
            academic_level=academic_level,
            faculty_id=faculty_id,
            document_id=document_id,
            latest_modified=latest_modified,
            revision_start_date=revision_start_date,
            state=state,
            parent_program_id=parent_program_id,
        )

        if any(value is None for value in [id, name, faculty_id, alignments]):
            return jsonify({"message": "Missing required parameters"}), 400

        return updateProjectProgramByID(projectProgram, alignments)


##
# http://localhost:5000/deleteprogram
# {
#     "id": 10
# }
##


@app.route("/deleteprogram/<int:id>", methods=["DELETE"])
def deleteprogram(id: int):
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        if id is None:
            return jsonify({"message": "Missing id parameter"}), 400

        return deleteProgramByID(id)


@app.route("/deleteCourse/<int:id>", methods=["DELETE"])
def deleteCourse(id: int):
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        if id is None:
            return jsonify({"message": "Missing id parameter"}), 400

        return deleteCourseByID(id)


##
# http://localhost:5000/searchProjectProgram?search_query=test-100
##
@app.route("/searchProjectProgram", methods=["GET"])
def searchProjectProgram_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    search_query = request.args.get("search_query")

    return searchProjectProgram(search_query)


##
# http://localhost:5000/copyProgramsToProject
# {
#     "project_id":"19",
#     "program_ids":[2]
# }
@app.route("/copyProgramsToProject", methods=["POST"])
def copyProgramsToProject_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    try:
        data = request.json
        project_id = data.get("project_id")
        program_ids = data.get("program_ids")

        if project_id is None or program_ids is None:
            return jsonify({"message": "Missing project ID or program IDs"}), 400

        result = copyProgramsToProject(project_id, program_ids)
        return result

    except Exception as e:
        return (
            jsonify({"error": "Failed to copy programs to project", "message": str(e)}),
            500,
        )


##
# http://localhost:5000/beginRevisionProgram
# {
#     "project_id":"19",
#     "program_id":2
# }
@app.route("/beginRevisionProgram", methods=["POST"])
def beginRevisionProgram_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    project_id = request.json.get("project_id")
    program_id = request.json.get("program_id")

    if project_id is None or program_id is None:
        return jsonify({"error": "Missing project_id or program_id parameter"}), 400

    return beginRevisionProgram(project_id, program_id)


##
# http://localhost:5000/mapCoursesToPrograms
##
# {
#   "project_id": 19,
#   "mapping": {
#     "1": [
#       [2, true],
#       [5, false]
#     ],
#     "2": [
#       [3, true],
#       [6, false]
#     ]
#   }
# }
@app.route("/mapCoursesToPrograms", methods=["POST"])
def mapCoursesToPrograms_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    try:
        # Get the project ID and mapping from the request
        data = request.json
        project_id = data.get("project_id")
        mapping = data.get("mapping")

        if project_id is None or mapping is None:
            return jsonify({"message": "Missing project ID or mapping"}), 400

        # Call the function to map courses to programs
        result = mapCoursesToPrograms(project_id, mapping)
        return result

    except Exception as e:
        return (
            jsonify({"error": "Failed to map courses to programs", "message": str(e)}),
            500,
        )


##
# http://localhost:5000/getAllProgramsCoursesOfProject?project_id=19
##
@app.route("/getAllProgramsCoursesOfProject", methods=["GET"])
def getAllProgramsCoursesOfProject_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    project_id = request.args.get("project_id")

    return getAllProgramsCoursesOfProject(project_id)


##
# http://localhost:5000/deleteProjectProgram
##
# {
#   "project_program_id": 1,
#   "project_id": 19
# }
@app.route("/deleteProjectProgram", methods=["POST"])
def deleteProjectProgram_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401

    try:
        data = request.json
        project_program_id = data.get("project_program_id")
        project_id = data.get("project_id")

        if project_program_id is None or project_id is None:
            return (
                jsonify(
                    {"error": "Missing project_program_id or project_id parameter"}
                ),
                400,
            )

        return deleteProjectProgram(project_program_id, project_id)

    except Exception as e:
        return (
            jsonify({"error": "Failed to delete project program", "message": str(e)}),
            500,
        )


##
# http://localhost:5000/addproject
##
# {
#     "name" : "lol",
#     "owners" : "test@uwindsor.ca",
#     "default_read" : false,
#     "default_read_write" : false,
#     "members": "test@uwindsor.ca",
#     "guests": ""
# }
@app.route("/addproject", methods=["POST"])
def add_project():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:

        pname = request.json["name"]
        owner = request.json["owners"]
        members = request.json["members"]
        guests = request.json["guests"]
        default_read = request.json["default_read"]
        default_read_write = request.json["default_read_write"]

        if any(
            value is None for value in [pname, owner, default_read, default_read_write]
        ):
            return jsonify({"message": "Missing required parameters"}), 400

        project = Project(
            name=pname,
            owner=owner,
            default_read=default_read,
            default_read_write=default_read_write,
        )

        return addProject(project, members, guests)


##
# http://localhost:5000/project_list
##
@app.route("/project_list", methods=["GET"])
def project_list():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        return get_projects_of_user()


##
# http://localhost:5000/projectdetail_by_id?id=10
##
@app.route("/projectdetail_by_id", methods=["GET"])
def projectdetail_by_id():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.args.get("id")
        return get_project_by_ID(id)


##
# http://localhost:5000/updateproject
##
# {
#     "id": 17,
#     "name" : "lol",
#     "owner" : "test@uwindsor.ca",
#     "default_read" : false,
#     "default_read_write" : false,
#     "members": "patel4r4@uwindsor.ca",
#     "guests": ""
# }
@app.route("/updateproject", methods=["POST"])
def updateproject():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.json["id"]
        name = request.json["name"]
        owner = request.json["owner"]
        default_read = request.json["default_read"]
        default_read_write = request.json["default_read_write"]
        members = request.json["members"]
        guests = request.json["guests"]

        project = Project(
            id=id,
            name=name,
            owner=owner,
            default_read=default_read,
            default_read_write=default_read_write,
        )

        if any(
            value is None
            for value in [
                id,
                name,
                owner,
                default_read_write,
                default_read,
            ]
        ):
            return jsonify({"message": "Missing required parameters"}), 400

        return update_project(project, members, guests)


##
# http://localhost:5000/uga_alignments_list
##
@app.route("/uga_alignments_list", methods=["GET"])
def get_uga_alignments_list():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        return getAllUgaAlignments(), 200


##
# http://localhost:5000/uga_alignment_by_id?id=4
##
@app.route("/uga_alignment_by_id", methods=["GET"])
def get_uga_alignment_by_id():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.args.get("id")
        if id is None:
            return jsonify({"message": "Missing ID parameter"}), 400

        return getUgaAlignmentByID(id)


###TODO further testing needed (not tested yet)
# http://localhost:5000/add_uga_alignment
##
@app.route("/add_uga_alignment", methods=["POST"])
def add_uga_alignment():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        data = request.json
        if data is None:
            return jsonify({"message": "Missing request body"}), 400

        return addUgaAlignment(data), 200


###TODO further testing needed (not tested yet)
# http://localhost:5000/update_uga_alignment
##
@app.route("/update_uga_alignment", methods=["PUT"])
def update_uga_alignment():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        data = request.json
        if data is None:
            return jsonify({"message": "Missing request body"}), 400

        return updateUgaAlignmentByID(data), 200


###TODO further testing needed (not tested yet)
# http://localhost:5000/delete_uga_alignment?id=4
##
@app.route("/delete_uga_alignment", methods=["DELETE"])
def delete_uga_alignment():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        id = request.args.get("id")
        if id is None:
            return jsonify({"message": "Missing ID parameter"}), 400

        return deleteUgaAlignmentByID(id), 200


##
# http://localhost:5000/getAllPrograms
##
@app.route("/getAllPrograms", methods=["GET"])
def getAllPrograms_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        return getAllPrograms()


@app.route("/getCount", methods=["GET"])
def getCount_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        return getCount()


##
# http://localhost:5000/getAllProgramsOfFaculty?faculty_id=1
##
@app.route("/getAllProgramsOfFaculty", methods=["GET"])
def getAllProgramsOfFaculty_route():
    if not validate_login():
        return jsonify({"message": "User not logged in"}), 401
    else:
        faculty_id = request.args.get("faculty_id")
        if faculty_id is None:
            return jsonify({"message": "Missing faculty Id parameter"}), 400

        return getAllProgramsOfFaculty(faculty_id), 200
