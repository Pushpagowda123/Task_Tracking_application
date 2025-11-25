# Task Tracking Application

This project now ships with two layers:

1. A lightweight **Flask** app that serves the HTML/CSS UI plus user-management endpoints used to demonstrate relationships.
2. A dedicated **Node.js + Express + MongoDB** API that owns the task data model and exposes a full CRUD surface.

The combo shows how to create, assign, update, and track tasks while demonstrating selector-driven derived state such as “tasks assigned to me”.

## Features

- Manage demo users (name + role) to illustrate assignments.
- Add tasks with title, description, priority, status, assignee, and due date.
- Task List page with filters: **All**, **Assigned to me**, **Completed**, plus “tasks by assignee” selector.
- Task detail controls inline per card to update status or delete the task.
- Derived dashboard cards (totals, by status, by assignee) backed by client-side selectors.
- RESTful Node/Express APIs backed by MongoDB.

## Getting Started

### 1. Run the Flask shell (frontend + user endpoints)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python app.py
```

Navigate to http://127.0.0.1:5000/ to use the UI.

### 2. Run the Node.js API (task data)

```bash
cd node_backend
npm install
cp env.example .env   # create your own if the copy is blocked; set PORT & MONGODB_URI
npm run dev
```

By default the API listens on http://127.0.0.1:4000 and connects to `mongodb://127.0.0.1:27017/tasktracker`.

> The frontend JavaScript points to `http://127.0.0.1:4000/api`. Update `window.API_BASE` if you need a different origin.

## API Quick Reference

### Flask (`app.py`)

| Method | Endpoint                           | Description                    |
| ------ | ---------------------------------- | ------------------------------ |
| GET    | `/api/users`                       | List demo users                |
| POST   | `/api/users`                       | Create user (`name`, `role`)   |
| GET    | `/api/tasks/by-assignee/<user_id>` | (Legacy) derived view          |
| GET    | `/api/dashboard`                   | (Legacy) status/assignee sums  |

### Node/Express (`node_backend/src/server.js`)

| Method | Endpoint         | Description                                          |
| ------ | ---------------- | ---------------------------------------------------- |
| GET    | `/api/users`     | List users stored in MongoDB                         |
| POST   | `/api/users`     | Create user (`name`, `role`)                         |
| GET    | `/api/tasks`     | List tasks, supports `status` & `assigneeId` filters |
| POST   | `/api/tasks`     | Create task (title, description, assigneeId, dueDate)|
| GET    | `/api/tasks/:id` | Fetch single task                                    |
| PATCH  | `/api/tasks/:id` | Update task (status, dueDate, etc.)                  |
| DELETE | `/api/tasks/:id` | Delete task                                          |

All endpoints exchange JSON.

