from app.internal.base_crud import CRUDBase
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.models.department import Department


class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    async def count_departments(self):
        total = await self.model.all().count()
        return total

deparment = CRUDDepartment(Department)