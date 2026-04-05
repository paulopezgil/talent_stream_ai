# VidPlan AI

**VidPlan AI**
(Previously Talent Stream AI)
is an intelligent content-creator assistant designed to streamline the production of video scripts, social media captions, and overall project management. By leveraging a structured AI agent, VidPlan AI helps creators brainstorm ideas and seamlessly execute them into organized, structured formats.

## 🚀 Project Overview

VidPlan AI assists content creators in generating video-related content using a sophisticated AI agent. The AI is designed with two distinct modes:
- **Brainstorming Mode (Chat-only):** Discuss ideas, explore concepts, and refine strategies without altering project files.
- **Execution Mode:** The AI autonomously writes and updates scripts, captions, and reference notes directly into the database.

## 🖥️ User Interface

The application features a highly productive, multi-tab layout:

- **Left Sidebar:** Displays a list of all your projects with a convenient "Create New Project" button.
- **Right Main Panel:** A workspace dedicated to the selected project, divided into multiple functional tabs:
  - **Chat Tab:** Your primary interface for interacting with the AI agent.
  - **Script Tab:** Holds generated and refined video scripts.
  - **References Tab:** Stores research notes, links, and background context.
  - **Social Media Tab:** Contains auto-generated captions, descriptions, and hashtags.

**Workflow:** When you create a new project, the backend instantly provisions a project ID and initializes a corresponding entry in the vector database for semantic search. As you interact with the agent in the Chat tab, it intelligently populates the other tabs with relevant content.

## 🏗️ Backend Architecture

The backend is built for performance and modularity using **FastAPI**. It implements a strict RESTful architecture with domain-specific routers (`projects`, `messages`, `scripts`, `social_media`) that map 1:1 to the frontend tabs, while the AI orchestrator runs invisibly as a side-effect of message creation.

### Hybrid Storage System
- **PostgreSQL:** Provides structured storage for projects, documents (scripts, captions), and chat messages.
- **Vector Database (PGVector):** Stores project embeddings to enable semantic search and Retrieval-Augmented Generation (RAG) workflows.

### AI Agent (Pydantic AI)
The core intelligence is powered by **Pydantic AI**, which enforces structured intent outputs. It utilizes function calling to safely save documents, update project statuses, and generate content without direct database access.

## ✨ Key Features

- **Structured AI Agent:** Clear separation between idea generation (brainstorming) and content generation (execution).
- **Hybrid Data Storage:** Combines the reliability of Postgres for structured data with the intelligence of a Vector DB for semantic retrieval.
- **Multi-Tab GUI:** An organized, intuitive interface for seamless project management and content creation.
- **Full Traceability:** Complete history of chat interactions and generated content versions.

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy (Postgres), PGVector (or external Vector DB like Qdrant)
- **Frontend:** Streamlit
- **AI/LLM:** OpenAI API, Pydantic AI

## 📚 Documentation

For a deeper dive into the technical design, database schemas, and folder structures, please refer to the detailed documentation located in the `/docs` directory:

- [Backend Architecture](docs/backend_architecture.md)
- [Frontend Architecture](docs/frontend_architecture.md)
