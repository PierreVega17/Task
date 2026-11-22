from fastapi.testclient import TestClient
import app.main as main

client = TestClient(main.app)

def setup_function():
    main.fake_db.clear()
    main.id_counter = 1

def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == [] 

def test_create_and_get_tasks_list():
    # Creamos dos tareas
    first = client.post("/tasks", json={"title": "Estudiar FastAPI", "description": "Repasar rutas"})
    second = client.post("/tasks", json={"title": "Hacer pruebas", "description": "Usar pytest"})

    assert first.status_code == 201
    assert second.status_code == 201

    # Traemos toda la lista de tareas
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    
    # Validamos que devuelva una lista con 2 elementos
    assert len(data) == 2
    assert data[0]["title"] == "Estudiar FastAPI"
    assert data[1]["title"] == "Hacer pruebas"

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_get_task_success():
    created = client.post(
        "/tasks",
        json={"title": "Estudiar Python"}
    )

    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Estudiar Python"


def test_delete_task_success():
    created = client.post(
        "/tasks",
        json={"title": "Eliminar esta tarea"}
    )

    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""

    response_after_delete = client.get(f"/tasks/{task_id}")

    assert response_after_delete.status_code == 404


def test_create_task_invalid_title():
    response = client.post(
        "/tasks",
        json={"title": "Hi"}
    )

    assert response.status_code == 422

def test_update_task_success():
    created = client.post(
        "/tasks",
        json={"title": "Tarea a actualizar"}
    )

    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Tarea actualizada", "completed": True}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Tarea actualizada"
    assert response.json()["completed"] is True

def test_update_task_not_found():
    response = client.patch(
        "/tasks/999",
        json={"title": "Tarea inexistente"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_update_task_invalid_title():
    created = client.post(
        "/tasks",
        json={"title": "Estudiar Python"}
    )
    task_id = created.json()["id"]
    
    # Intentamos actualizar enviando null explícitamente
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": None}
    )
    
    # Debe ser rechazado por Pydantic con un 422
    assert response.status_code == 422

def test_update_task_preserves_unmodified_fields():
    created = client.post(
        "/tasks",
        json={
            "title": "Estudiar Python",
            "description": "Practicar FastAPI"
        }
    )

    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Estudiar Python"
    assert data["description"] == "Practicar FastAPI"
    assert data["completed"] is True