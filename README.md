# Vibly

Vibly es una red social moderna que combina lo mejor de la mensajería instantánea con un feed social.

## Estructura del Proyecto

- `frontend/`: Aplicación React + Vite
- `backend/`: API REST con Python FastAPI

## Requisitos

- Node.js (v18+)
- Python (v3.10+)

## Cómo iniciar el proyecto

### 1. Backend (Python)

```bash
cd backend
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
# Activar entorno virtual
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
uvicorn main:app --reload
```

El backend correrá en `http://localhost:8000`

### 2. Frontend (React)

```bash
cd frontend
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend correrá en `http://localhost:5173`

## Características

- Interfaz moderna con tema Claro/Oscuro
- Gradiente distintivo "Vibly Red"
- Lista de chats y ventana de conversación
- Feed social (Próximamente)
