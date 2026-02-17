import { useEffect, useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [error, setError] = useState("");

  const endpoint = useMemo(() => `${API_BASE}/api/tasks`, []);

  const loadTasks = async () => {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error("No se pudieron obtener tareas.");
    }
    setTasks(await response.json());
  };

  useEffect(() => {
    loadTasks().catch((e) => setError(e.message));
  }, []);

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setEditingTaskId(null);
  };

  const submitTask = async (event) => {
    event.preventDefault();
    setError("");

    const isEditing = Boolean(editingTaskId);
    const url = isEditing ? `${endpoint}/${editingTaskId}` : endpoint;
    const method = isEditing ? "PUT" : "POST";

    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description }),
    });

    if (!response.ok) {
      const payload = await response.json();
      setError(payload.detail || "Error al guardar la tarea.");
      return;
    }

    await loadTasks();
    resetForm();
  };

  const toggleTask = async (task) => {
    const response = await fetch(`${endpoint}/${task.id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: !task.completed }),
    });

    if (!response.ok) {
      setError("Error al actualizar estado.");
      return;
    }
    await loadTasks();
  };

  const deleteTask = async (taskId) => {
    const response = await fetch(`${endpoint}/${taskId}`, { method: "DELETE" });
    if (!response.ok) {
      setError("Error al eliminar tarea.");
      return;
    }
    await loadTasks();
    if (editingTaskId === taskId) {
      resetForm();
    }
  };

  const startEdit = (task) => {
    setEditingTaskId(task.id);
    setTitle(task.title);
    setDescription(task.description || "");
  };

  return (
    <main className="container">
      <h1>Monolith To-Do</h1>
      <p className="subtitle">Python + React + Vercel</p>

      <section className="card">
        <form onSubmit={submitTask}>
          <div className="row">
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Titulo"
              required
              maxLength={120}
            />
          </div>
          <div className="row" style={{ marginTop: "0.5rem" }}>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Descripcion (opcional)"
            />
          </div>
          <div className="row" style={{ marginTop: "0.5rem" }}>
            <button className="primary" type="submit">
              {editingTaskId ? "Actualizar" : "Crear"}
            </button>
            {editingTaskId && (
              <button className="muted" type="button" onClick={resetForm}>
                Cancelar
              </button>
            )}
          </div>
          {error && <p className="error">{error}</p>}
        </form>
      </section>

      <section className="card">
        {tasks.length === 0 && <p className="small">No hay tareas registradas.</p>}
        {tasks.map((task) => (
          <article key={task.id} className={`task ${task.completed ? "completed" : ""}`}>
            <div>
              <h3>{task.title}</h3>
              {task.description && <p>{task.description}</p>}
              <p className="small">Creada: {new Date(task.created_at).toLocaleString()}</p>
            </div>
            <div className="row">
              <button className="muted" onClick={() => toggleTask(task)}>
                {task.completed ? "Reabrir" : "Completar"}
              </button>
              <button className="muted" onClick={() => startEdit(task)}>
                Editar
              </button>
              <button className="danger" onClick={() => deleteTask(task.id)}>
                Eliminar
              </button>
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}

export default App;
