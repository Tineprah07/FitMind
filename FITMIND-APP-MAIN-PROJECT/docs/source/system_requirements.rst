System Requirements
===================

Overview
--------

The system requirements define how FITMIND should function behind the scenes to meet the needs of its users. These requirements are informed directly by the user requirements and were refined throughout development based on testing, performance needs, and design feedback.

They are grouped into **functional** (what the system should do) and **non-functional** (how the system should perform) categories.

.. tip::

   This section translates user-facing expectations into specific system behaviors — ensuring every feature is technically grounded.

Functional Requirements
------------------------

These describe the features and behaviors the system must provide.

1. **Stress Tracking and Management**

   - The system must allow users to log stress using a 1–5 scale.
   - A mood-based emoji interface should be available for intuitive stress input.
   - Users should be able to add optional notes for each stress entry.
   - Logged data must include: stress value, mood (emoji), note (if any), and timestamp.
   - The system must store stress data in a user-specific format and retrieve it on request.
   - Upon submission, the system should analyze the stress level and trigger a personalized suggestion (e.g., launch Breathe Flow).

   .. note::
      Stress logging is lightweight and real-time — providing feedback as soon as the form is submitted.

2. **Exercise Tracking**

   - The system must allow users to log various exercise types via dropdown or custom input.
   - Each entry must include the type of activity and the time it was logged.
   - A live bar chart should dynamically update as entries are made.
   - The system must also list all logged exercises during a session.
   - Based on recent stress data, the system should offer a suitable exercise suggestion (e.g., light stretching after high stress).

3. **Breathe Flow Tool**

   - The system must provide a guided breathing experience with animated timing (inhale, hold, exhale).
   - This feature should be accessible without login.
   - It must include text instructions and visual cues, and return users to their previous page after completion.

   .. seealso::
      The Breathe Flow page is the only page open to all users — promoting accessible wellness without registration.

4. **Notes Page**

   - The system must provide a text input field for users to create personal notes.
   - Notes must be saved with timestamps and associated with the correct user account.
   - All saved notes should be displayed in a list below the input field.
   - A search function must allow users to filter notes based on keyword input.

5. **Reminder System**

   - Users must be able to enter a custom reminder message and set a specific time for it.
   - The system should trigger a pop-up notification with sound at the specified time.
   - Reminders should work regardless of the page the user is on.
   - The system must maintain a list of all reminders created by the user.

   .. note::
      Reminders continue working across all pages, ensuring no notification is missed during navigation.

6. **Authentication and Access Control**

   - The system must allow users to register with email and password.
   - Users must be able to log in, maintain a session, and log out securely.
   - Stress, Exercise, Notes, and Reminder pages should only be accessible when logged in.
   - The Breathe Flow tool must remain available to all users without authentication.

   .. warning::
      Unauthorized users must be prevented from accessing private pages or stored user data.

7. **Data Management and Storage**

   - All personal data (logs, notes, reminders) must be stored securely in a structured database.
   - Each data entry must be linked to the correct user session.
   - Data should be retained and displayed only while the user is logged in.

   .. tip::
      The current implementation uses SQLite, but the system is designed to support future upgrades (e.g., PostgreSQL).

Non-Functional Requirements
---------------------------

These describe how the system should perform, behave, and support the user experience.

1. **Usability**

   - The interface should be clean, intuitive, and usable without more than a page of instructions.
   - All pages should be responsive across devices (mobile, tablet, desktop).
   - Users should be able to complete core tasks (e.g., logging stress, writing notes) within 5–10 minutes.

   .. tip::
      UI decisions were made based on interview feedback, emphasizing fast, low-friction interactions.

2. **Performance**

   - The system must respond to user input (e.g., logging, chart updates) within 1–2 seconds.
   - Data entries and pop-up reminders must trigger in real-time without noticeable delay.

3. **Security and Privacy**

   - User authentication must be required for access to personal data.
   - Sensitive information must be handled securely and only shown to the logged-in user.
   - Sessions must expire after logout or inactivity to protect user data.

   .. important::
      FITMIND is designed around privacy — users control what they log, and only they can access their data.

4. **Reliability**

   - The system should remain stable during regular use and handle multiple simultaneous users.
   - Reminders and notifications must work consistently across sessions and pages.

5. **Testability**

   - The system must provide clear error messages for invalid inputs (e.g., stress outside 1–5, empty reminder fields).
   - Components should be testable individually (unit tests) and together (integration tests).

6. **Maintainability**

   - Code should be organized into reusable components.
   - The system should support future updates, such as re-enabling removed features like the community page if needed.

Removed Features
----------------

- **Community Page**: Originally planned for user interaction and sharing, this feature was removed based on user feedback and time constraints. It was replaced by a stronger focus on personal tools that prioritize privacy, simplicity, and self-reflection.

.. note::

   This feature may be reconsidered in future versions depending on demand and implementation resources.

---

This completes the technical foundation required to implement FITMIND as envisioned by its users. The next section will detail how these requirements were translated into the final architecture and component structure of the system.
