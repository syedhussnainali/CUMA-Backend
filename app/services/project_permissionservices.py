from sqlalchemy.orm import aliased
from sqlalchemy import and_, or_
from flask import jsonify, session
from ..model.project_permissions import ProjectPermissions
from ..model.project import Project


# read_write_flag
#   true if read and write
#   flase if read
def checkPermissions(project_id, user_id, session, read_write_flag):
    project = aliased(Project)
    projectPermissions = aliased(ProjectPermissions)

    read_permission = projectPermissions.read == True
    default_read = project.default_read == True
    write_permission = projectPermissions.read_write == True
    default_write = project.default_read_write == True

    condition1 = project.id == project_id
    userCondition = projectPermissions.user_id == user_id
    if read_write_flag:
        rightConditions = and_(write_permission, userCondition)
        leftConditions = default_write
    else:
        rightConditions = and_(read_permission, userCondition)
        leftConditions = default_read
    conditions = or_(leftConditions, rightConditions)

    query = (
        session.query(projectPermissions.user_id, project.id)
        .join(project, project.id == projectPermissions.project_id)
        .filter(condition1)
        .filter(conditions)
    )
    print(
        query.statement.compile(
            dialect=session.bind.dialect, compile_kwargs={"literal_binds": True}
        )
    )
    results = query.count()
    # print(results)
    if results == 0:
        return False
    else:
        return True
