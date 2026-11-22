from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse


class TaskRepository:

    def __init__(self):
        self.tasks: list[TaskResponse] = []
        self.id_counter = 1

    def create(self, task_data: TaskCreate) -> TaskResponse:
        # Crear una tarea con un ID único.
        task = TaskResponse(id=self.id_counter, **task_data.model_dump())
        # Guardarla en self.tasks.
        self.tasks.append(task)
        # Incrementar el contador.
        self.id_counter += 1
        # Devolver la tarea creada.
        return task.model_copy()

    def get_all(self) -> list[TaskResponse]:
        # Devolver todas las tareas.
        return [task.model_copy() for task in self.tasks]

    def get_by_id(self, task_id: int) -> TaskResponse | None:
        # Buscar por ID.
        for task in self.tasks:
            if task.id == task_id:
                return task.model_copy()
        # Si no existe, devolver None.
        return None

    def delete(self, task_id: int) -> bool:
        # Eliminar la tarea si existe.
        for index, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[index]
                return True
        # Devolver True si se eliminó, False si no existe.
        return False

    def update(
        self,
        task_id: int,
        task_data: TaskUpdate
    ) -> TaskResponse | None:
        # Actualizar únicamente los campos enviados.
        for task in self.tasks:
            if task.id == task_id:
                updates = task_data.model_dump(exclude_unset=True)
                for field, value in updates.items():
                    setattr(task, field, value)
                return task.model_copy()
        # Devolver la tarea actualizada o None.
        return None