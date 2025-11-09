System Components
=================

Overview
--------

This section provides a detailed breakdown of the core components that make up the FITMIND application. Each component is designed to serve a specific role, and together they deliver a seamless, responsive, and personalized experience to the user.

FITMIND is modular by design, making it easier to maintain, scale, and upgrade over time.

.. note::

   All components work independently but are integrated through consistent data flow, API interaction, and session management.

Frontend Components
-------------------

These components are responsible for user interaction, input handling, and visual feedback.

1. **Landing Page**

   - Introduces the app to new users.
   - Provides links to Register, Log In, and the Breathe Flow tool.
   - Designed to quickly explain the app’s value without requiring a sign-in.

   .. tip::

      The Breathe Flow tool can be launched directly from here — no account needed.

2. **Register and Login Pages**

   - Allow users to securely create an account or sign in.
   - Validate user input and communicate with the backend to manage sessions.
   - Display error messages for incorrect credentials or missing input.

3. **Homepage (Dashboard)**

   - Acts as the user's central hub after logging in.
   - Provides navigation to all other features.
   - May display welcome messages or quick summaries in future versions.

4. **Stress Page**

   - Lets users log their stress using a 1–5 scale and emojis.
   - Includes a notes field to capture stress causes.
   - Immediately triggers context-aware recommendations (e.g., suggesting Breathe Flow).
   - Sends all data to the backend and displays confirmation.

   .. note::

      Stress entries are stored with timestamps and mood indicators for progress tracking.

5. **Exercise Page**

   - Allows users to log various types of physical activity.
   - Supports dropdown and custom input.
   - Displays a live bar chart that updates in real time as entries are added.
   - Suggests suitable activities based on recent stress data.

6. **Breathe Flow Page**

   - Publicly accessible (no login required).
   - Guides users through calming inhale–hold–exhale breathing cycles.
   - Uses animations and text prompts for visual clarity.
   - Offers a quick escape from stress with no barriers.

   .. seealso::

      This is the only page that remains fully open to the public. All others require login.

7. **Notes Page**

   - Provides a free-form text input for journaling or workout reflections.
   - Saves entries to the backend and displays them in a list.
   - Includes a search bar for quick filtering of saved notes.

   .. tip::

      Users can search notes by keywords — useful for reviewing thoughts related to specific events (e.g., exams).

8. **Reminder Page**

   - Allows users to create custom reminders with a message and time.
   - Triggers a pop-up alert with sound across all pages at the specified time.
   - Displays a list of all upcoming reminders.

   .. note::

      Reminder notifications stay active across pages and help users stay consistent with wellness habits.

Backend Components
------------------

The backend, built using Flask, handles authentication, routing, data processing, and storage.

1. **Authentication Manager**

   - Validates credentials and manages user sessions.
   - Controls access to protected pages and features.
   - Handles login, logout, and registration securely.

2. **Stress Manager**

   - Receives and stores stress entries.
   - Evaluates stress level and returns appropriate recommendations.
   - Sends data to the frontend for visualization if needed.

3. **Exercise Manager**

   - Processes incoming exercise logs and links them to the current user.
   - Supports real-time updates of the session chart.
   - Generates suggestions based on combined stress and activity history.

4. **Reminder Manager**

   - Stores custom reminders for each user.
   - Sends reminder data to the frontend for scheduling and triggering.
   - Ensures sound alerts and pop-ups work regardless of the current page.

5. **Notes Manager**

   - Saves notes tied to the user's account.
   - Handles retrieval and filtering (search) requests.
   - Supports storing timestamped, searchable text entries.

6. **Database Handler**

   - Stores all structured data in a local SQLite database.
   - Uses unique user IDs to associate data correctly.
   - Ensures data integrity and security during read/write operations.

   .. tip::

      The backend is structured in a way that allows SQLite to be replaced with PostgreSQL or another RDBMS in future deployments.

7. **Session Controller**

   - Tracks active users and page access.
   - Ensures that only authenticated users can access sensitive features.
   - Clears session data on logout or timeout.

   .. warning::

      All protected data (stress logs, notes, etc.) is inaccessible without an active session.

Component Relationships
-----------------------

- All frontend components send data to backend endpoints via form submissions or fetch/AJAX calls.
- The backend verifies, processes, and stores this data in the database.
- The frontend reflects responses with UI updates — charts, messages, suggestions, or alerts.
- Session control ensures users see only what they are authorized to access.

.. seealso::

   These components are tightly coordinated to support real-time user feedback while preserving data privacy and performance.

---

Each component is designed to serve its role independently while working seamlessly with others. This modular structure ensures that FITMIND remains lightweight, focused, and easy to enhance as new features are added.
