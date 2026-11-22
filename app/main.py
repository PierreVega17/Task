from app.models.task import Task, TaskCreate, TaskUpdate
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Task Management API", description="API for managing tasks", version="1.0.0")

fake_db = []
id_counter = 1


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    global id_counter
    task = Task(id=id_counter, **task_data.model_dump())
    id_counter += 1
    fake_db.append(task)
    return task

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return fake_db

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in fake_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(fake_db):
        if task.id == task_id:
            del fake_db[index]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate) -> Task:
    for task in fake_db:
        if task.id == task_id:
            updates = task_data.model_dump(exclude_unset=True)

            for field, value in updates.items():
                setattr(task, field, value)

            return task 

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )