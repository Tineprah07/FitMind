System Architecture
===================

Overview
--------

This section outlines the internal structure of the FITMIND application, including its key components and how they interact. The architecture is designed to be modular, scalable, and easy to maintain, while supporting all core features such as logging, authentication, reminders, and personalized recommendations.

The system follows a standard **client-server architecture**, where the frontend (client) interacts with the backend (server) through HTTP requests. All data is stored in a structured relational database, ensuring security and persistence.

.. note::

   FITMIND uses a lightweight stack — perfect for fast development and student use — but is structured to support future scaling.

Main Components
---------------

FITMIND is divided into the following core layers:

1. **Frontend (Client Side)**

   - Built with **HTML**, **CSS**, and **JavaScript**.
   - Provides the user interface for:
     - Stress logging
     - Exercise tracking
     - Breathing sessions
     - Note-taking
     - Reminder setup
   - Updates UI dynamically based on user actions.
   - Sends form data and fetch requests to the backend via HTTP.

   .. tip::

      The frontend is responsive and mobile-ready, supporting students across laptops, tablets, and phones.

2. **Backend (Server Side)**

   - Developed using **Python Flask**.
   - Handles:
     - API routing
     - Input validation
     - Authentication and session control
     - Business logic (e.g., suggestions based on stress level)
   - Interacts with the SQLite database for data read/write operations.

   .. seealso::

      Backend endpoints also enforce access restrictions to ensure user-specific data is only available after login.

3. **Database Layer**

   - Uses **SQLite** — a lightweight, file-based relational database.
   - Stores:
     - User credentials (hashed)
     - Stress logs
     - Exercise entries
     - Notes with timestamps
     - Reminders with time and text
   - Data is structured with foreign keys based on user ID.

   .. note::

      The database layer is abstracted to allow switching to PostgreSQL or MySQL in future upgrades.

4. **Authentication & Access Control**

   - Handles login, registration, and logout.
   - Uses secure sessions to protect private routes.
   - Redirects unauthenticated users trying to access:
     - Stress Page
     - Exercise Page
     - Notes Page
     - Reminder Page
   - Grants public access to:
     - Landing Page
     - Breathe Flow tool
     - Login & Registration

   .. warning::

      All private data is session-restricted. Any expired or unauthorized session attempts are blocked at both frontend and backend levels.

5. **Reminder System**

   - Built using **JavaScript timing functions** and local scheduling logic.
   - Shows pop-up alerts (with sound) at scheduled times.
   - Works globally across all pages — reminders stay active regardless of navigation.

   .. tip::

      This system runs fully in-browser, minimizing backend load while maintaining reliability.

6. **Recommendation Engine**

   - Triggered upon logging stress or exercise.
   - Uses lightweight logic to evaluate input and suggest next actions (e.g., launching the Breathe Flow tool).
   - Operates entirely in real-time with zero delay or page reloads.

   .. note::

      Recommendations are based on logic thresholds (e.g., stress level ≥ 4), but could evolve into AI-based personalization later.

Component Interaction Flow
--------------------------

1. The user registers or logs in through the **authentication module**.
2. After login:
   - The **Stress** or **Exercise** form is submitted from the frontend.
   - The **backend** validates and saves the data into the **SQLite database**.
   - A real-time suggestion (if applicable) is returned to the frontend.
3. The frontend updates:
   - **Charts**, **lists**, and **notes**
   - Pop-ups for reminders and feedback
4. If a reminder time is reached:
   - The frontend displays a **sound alert** and **visual pop-up**.
5. The user logs out.
   - Session data is cleared and access to protected features is revoked.

.. seealso::

   This full loop ensures that all features — from data tracking to guidance — remain user-driven and immediate.

Pages and Navigation
--------------------

- Navigation is controlled through a top bar/menu.
- Publicly accessible pages:
  - **Landing Page**
  - **Register/Login**
  - **Breathe Flow**
- Protected pages (require login):
  - **Stress Page**
  - **Exercise Page**
  - **Notes Page**
  - **Reminder Page**

Navigation control is handled on both the frontend (hiding/showing elements) and backend (access blocking). This provides **fail-safe protection** in case users attempt direct URL access.

Scalability and Maintenance
---------------------------

- The backend and database are structured to allow seamless upgrades (e.g., replace SQLite with PostgreSQL).
- Each functional component (e.g., stress logging, note-taking) is modular.
  - New pages or tools can be added without breaking existing logic.
- The frontend is structured for maintainability:
  - CSS is reusable and consistent
  - JavaScript is scoped to each feature

.. tip::

   Future plans include API separation and possibly turning FITMIND into a Progressive Web App (PWA) or mobile app.

.. note::

   Developers can extend this architecture to include analytics, dark mode, or third-party login (e.g., Google OAuth) as next steps.

