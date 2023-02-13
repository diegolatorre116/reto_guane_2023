from app.internal.CRUD.base_crud import CRUDBase
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.models.department import Department


class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    pass

deparment = CRUDDepartment(Department)