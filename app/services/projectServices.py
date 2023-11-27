from flask import jsonify, session
from ..model.project_permissions import ProjectPermissions
from ..model.project import Project
from app.services.dbServices import createSession, closeSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import union,and_, or_, delete
from .utils import getSessionUserID

def addProject(project,members, guests):
    try:
        session = createSession()
        project.owner = getSessionUserID()
        session.add(project)
        session.flush()
        print(project.id)
        
        member_permissions = generate_member_permissions(members, project.id)
        guest_permissions=generate_guest_permissions(guests,project.id)

        # Add member permissions to the session
        for permission in member_permissions:
            session.add(permission)

        # Add guest permissions to the session
        for permission in guest_permissions:
            session.add(permission)
        
        # Add the permissions to the session
        session.commit()

        closeSession(session)
        return jsonify({"success": "Project added successfully"})
    
    except SQLAlchemyError as e:
        session.rollback()
        closeSession(session)
        return jsonify({"error": "Failed to add program", "message": str(e)}), 500


def generate_member_permissions(emails, project_id):

    # Split the emails by comma
    email_list = []
    if emails:
        email_list = emails.split(',')
    email_list.append(getSessionUserID())
    # Generate project permissions for each email
    permissions = []
    for email in email_list:
        permission = ProjectPermissions(user_id=email.strip(),project_id=project_id, read=True, read_write= True)
        permissions.append(permission)

    return permissions

def generate_guest_permissions(emails, project_id):

    # Split the emails by comma
    email_list = []
    if emails:
        email_list = emails.split(',')
    email_list.append(getSessionUserID())

    # Generate project permissions for each email
    permissions = []
    for email in email_list:
        permission = ProjectPermissions(user_id=email.strip(),project_id=project_id, read=True, read_write= False)
        permissions.append(permission)

    return permissions

def get_projects_of_user():
    try:
        session = createSession()
        combined_query = (
            union(get_default_read_project_id(session), get_project_id_by_user_read(session))
            .subquery())
        result = session.query(combined_query).all()
        project_names = [{"name": name, "id": project_id} for name, project_id in result]
        closeSession(session)
        return jsonify(project_names)
    except SQLAlchemyError as e:
        closeSession(session)
        return jsonify({"error": "Failed to fetch programs", "message": str(e)}), 500
    
def get_default_read_project_id(session):
    project_default_names = (
    session.query(Project.name, Project.id)
        .filter(Project.default_read == True))
    return project_default_names


def get_project_id_by_user_read(session):
    email_id = getSessionUserID()
    project_default_names = (
        session.query(Project.name, Project.id)
        .join(ProjectPermissions, Project.id == ProjectPermissions.project_id)
        .filter(ProjectPermissions.user_id == email_id and ProjectPermissions.read == True))
    return project_default_names

def get_project_by_ID(id):
    try:
        session = createSession()
        project_details = (
            session.query(Project)
            .join(ProjectPermissions, Project.id == ProjectPermissions.project_id)
            .filter(Project.id == id
                    and (Project.default_read or 
                            (ProjectPermissions.read == True and ProjectPermissions.user_id == getSessionUserID()) 
                        ))
            .first())

        if project_details is None:
            return jsonify({"error": "Project not found or user with no read permissions"}), 401
        
        project_details = {
            "id" : project_details.id,
            "name" : project_details.name,
            "owner" : project_details.owner,
            "default_read" : project_details.default_read,
            "default_read_write" : project_details.default_read_write,
        }

        closeSession(session)
        return jsonify(project_details)
    except SQLAlchemyError as e:
        closeSession(session)
        return jsonify({"error": "Failed to fetch programs", "message": str(e)}), 500


def update_project(project,members,guests):
    try:
        session = createSession()
        
        default_read_write_condition = Project.default_read_write == True
        read_write_condition = ProjectPermissions.read_write == True
        user_id_condition = ProjectPermissions.user_id == getSessionUserID()

        nested_condition = and_(read_write_condition, user_id_condition)
        final_condition = or_(default_read_write_condition, nested_condition)

        project_query = (
            session.query(Project)
            .join(ProjectPermissions, Project.id == ProjectPermissions.project_id)
            .filter(Project.id == project.id)
            .filter(final_condition))
        
        project_details = project_query.first()
        
        if project_details is None:
            return jsonify({"error": "Project not found or user with no read permissions"}), 501
        
        project_details.id = project.id
        project_details.name = project.name
        project_details.owner = project.owner
        project_details.default_read = project.default_read
        project_details.default_read_write = project.default_read_write
        
        session.execute(deletion_project_Permissions(project.id))

        member_permissions = generate_member_permissions(members, project.id)
        guest_permissions=generate_guest_permissions(guests,project.id)

        # Add member permissions to the session
        for permission in member_permissions:
            session.add(permission)

        # Add guest permissions to the session
        for permission in guest_permissions:
            session.add(permission)
        
        session.commit()
        closeSession(session)
        return jsonify({"success": "Program updated successfully"})
    except SQLAlchemyError as e:
        closeSession(session)
        return jsonify({"error": "Failed to fetch programs", "message": str(e)}), 500

def deletion_project_Permissions(project_id):
    
    condition = ProjectPermissions.project_id == project_id
    delete_statement = delete(ProjectPermissions).where(condition)
    return delete_statement

def getSessionUserID():
    user_id = session['user_id']
    print(user_id)
    return user_id