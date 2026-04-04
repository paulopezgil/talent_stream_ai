# Backend Architecture

## Directory Structure

```text
backend/
├── core/           # Application config, security, and DB connection singletons
├── routers/        # API routing and endpoint definitions
│   ├── agent.py      # Endpoints for interacting with the Pydantic AI agent
│   └── database.py   # Endpoints for CRUD operations on standard DB entities and frontend tab data
├── services/       # Core business logic (LLM orchestration, DB operations)
├── models/         # Database ORM models (SQLAlchemy table structures)
├── schemas/        # Pydantic validation schemas (API requests/responses)
└── app.py
```

## Database Schema

### 1. Vector Table (`project_index`)
Used for retrieval-augmented generation (RAG) and semantic search. Can be implemented in PGVector or an external Vector DB.

| Column         | Type                | Description |
|----------------|------------------|-------------|
| project_id     | UUID (PK)          | Links to Postgres project table |
| title          | TEXT               | Project title for search |
| description    | TEXT               | Full project description used for embedding |
| tags           | TEXT[]             | Optional tags for filtering |
| embedding      | VECTOR(1536)       | Vector embedding of project content (OpenAI embedding) |
| created_at     | TIMESTAMPTZ        | Timestamp of creation |
| updated_at     | TIMESTAMPTZ        | Timestamp of last update |

> Notes: Embeddings generated via OpenAI `text-embedding-3-large`.

### 2. Projects Table (`projects`)
Stores metadata about each project.

| Column     | Type       | Description |
|-----------|------------|-------------|
| id        | UUID (PK) | Unique project identifier |
| name      | TEXT       | Project name/title |
| created_at| TIMESTAMPTZ| Timestamp of creation |

### 3. Documents Table (`documents`)
Stores different content outputs (script, social media captions, references) for each project.

| Column      | Type       | Description |
|------------|------------|-------------|
| id         | UUID (PK) | Unique document identifier |
| project_id | UUID (FK) | Links to project |
| type       | TEXT      | Content type: `script`, `social_media`, `references` |
| content    | TEXT      | Generated content |
| updated_at | TIMESTAMPTZ | Timestamp of last update |

### 4. Messages Table (`messages`)
Stores chat history for the AI agent per project.

| Column      | Type       | Description |
|------------|------------|-------------|
| id         | UUID (PK) | Unique message identifier |
| project_id | UUID (FK) | Links to project |
| role       | TEXT      | `user` or `assistant` |
| content    | TEXT      | Message text |
| created_at | TIMESTAMPTZ | Timestamp of message |

## AI Agent

- Implemented using **Pydantic AI**
- Backend enforces structured interaction:
  - **Intent declaration**: `brainstorming_mode` (chat-only), `execution_mode` (writing scripts, captions, etc. to the database)
  - **Function calls**: `save_document`, `update_project`, etc.
- Backend handles database writes; AI never accesses DB directly
- Integrated with vector table for retrieval and context-aware responses

## Backend Responsibilities

1. Receive user messages from frontend via API routers (`agent.py`, `database.py`)
2. Fetch relevant context from:
   - `messages` table
   - `documents` table
   - `project_index` vector table (for semantic retrieval)
3. Call OpenAI API via Pydantic AI (handled in `services/`)
4. Parse AI response:
   - If intent = `brainstorming_mode` → save to messages only
   - If intent = `execution_mode` → save to documents table (`script`, `references`, `social_media`)
5. Return response to frontend (validated via `schemas/`)
6. Update vector embeddings if project content changes
