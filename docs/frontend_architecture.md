# Frontend Architecture

## UI Structure

The UI consists of a **Left Sidebar** and a **Right Main Panel**. It is built using **Next.js**, **Tailwind CSS**, and potentially **shadcn/ui** for tabs and layouts.

### 1. Left Sidebar
- Displays a list of all existing projects
- Features a **"Create New Project"** button
- Clicking a project selects it and loads its corresponding data into the Right Main Panel

### 2. Right Main Panel
- The workspace for the currently selected project
- Divided into the following tabs:
  - **Chat Tab:** For interacting with the AI agent. Used for brainstorming and issuing commands.
  - **Script Tab:** Contains the generated video scripts.
  - **References Tab:** Stores generated or manual research notes and reference links.
  - **Social Media Tab:** Displays auto-generated captions, descriptions, and hashtags for platforms like YouTube, Twitter, and Instagram.

## Workflow Execution

1. **Project Creation:**
   - User clicks "Create New Project".
   - Frontend calls the `database` router.
   - Backend provisions a project ID and initializes an entry in the vector database.
2. **Interaction (Brainstorming):**
   - User types in the **Chat Tab**.
   - Frontend sends the message to the `agent` router.
   - AI agent responds with brainstorming output. The backend saves the history to the `messages` table.
3. **Execution (Document Generation):**
   - User asks the agent to draft a script or a caption.
   - AI agent changes intent to execution mode and uses function calling.
   - The backend directly saves the generated content to the `documents` table.
   - Frontend detects the update (via polling, WebSocket, or revalidation) and populates the **Script**, **References**, or **Social Media** tab accordingly.
