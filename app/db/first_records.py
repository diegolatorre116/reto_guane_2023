from app.models.department import Department
from app.models.user import User
from app.core.security.pwd import password_hash

info_department = {
        "name": 'Development',
        "description": 'Software_Development'
        }

info_user = {
        "username": 'guane',
        "password": 'ironparadise16',
        "role": 'C-LEVEL',
        "email": 'guane@example.com',
        "department_id": 1
    }

async def first_records():  
    department = Department(**info_department)
    print(department) 
    print("asd")
    await department.save()

    info_user["password"] = password_hash(info_user["password"])
    user = User(**info_user)
    await user.save()

    return "Done"


