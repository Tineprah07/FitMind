User Requirements
=================

Overview
--------

The user requirements describe what FITMIND must offer to ensure a helpful, meaningful, and accessible experience for its primary audience: university students managing both mental and physical well-being.

These requirements were gathered through structured interviews, user feedback, and iterative testing. They evolved throughout the development process to prioritize simplicity, personalization, and usability over complexity or gamification.

.. note::

   These requirements are based on real-world feedback from students. The goal is to make FITMIND feel useful, not overwhelming.

Core User Needs
---------------

Below is a refined list of what users should be able to do within FITMIND:

1. **Stress Tracking and Management**

   - Log daily stress using a 1–5 scale.
   - Use emojis to express how they feel (mood-based prompts).
   - Add short notes to describe the cause of stress (e.g., “exam coming up”).
   - Instantly receive a personalized suggestion after logging (e.g., launch the Breathe Flow tool).
   - Access past stress entries through visual summaries or graphs.

   .. tip::

      Stress tracking is designed to be completed in less than one minute — making it easy to build a daily habit.

2. **Exercise Tracking**

   - Log physical activity, such as cardio, stretching, or custom workouts.
   - Choose from a dropdown list or enter a custom exercise type.
   - See a live-updating progress chart as new entries are added.
   - View a session-based list of all exercises logged.
   - Receive context-aware suggestions based on recent stress data.

3. **Breathe Flow (Relaxation Tool)**

   - Access a simple, guided breathing tool to reduce stress.
   - Use the tool without logging in — it's freely available to all users.
   - Follow inhale–hold–exhale animations with supportive text prompts.
   - Return to the previous page after completing the breathing session.

   .. seealso::

      The Breathe Flow tool is publicly available from the landing page — no login required.

4. **Notes Page**

   - Write reflections, thoughts, or workout notes in a free-form text field.
   - View all saved notes in a scrollable list.
   - Use a search feature to find specific notes by keyword.
   - Store notes securely, linked to the user’s authenticated account.

5. **Reminders**

   - Set custom reminders for any wellness task (e.g., "stretch", "breathe", "hydrate").
   - Choose a specific time for each reminder to trigger.
   - Receive a pop-up alert with sound across all pages when the reminder activates.
   - View and manage a list of upcoming saved reminders.

   .. note::

      Reminder pop-ups are functional across all pages, ensuring users never miss their scheduled wellness tasks.

6. **Authentication and Data Privacy**

   - Register with a secure email and password.
   - Sign in to access personal features such as stress logs, notes, and reminders.
   - Log out to end the session and secure user data.
   - Require login access for Stress, Exercise, Notes, and Reminder pages.
   - Keep the Breathe Flow page open to all users to promote wellness accessibility.

7. **Removed Feature: Community Page**

   - Originally planned to allow users to share progress and wellness tips.
   - Removed based on time constraints and user feedback to maintain focus and simplicity.
   - FITMIND now emphasizes personal wellness tools over social interaction.

   .. important::

      This decision reflects the app’s core philosophy: support individual well-being without introducing social pressure.

Experience Expectations
------------------------

Users expect the app to be:

- **Quick to use** – All tasks (logging, breathing, note-taking) should take no more than 5–10 minutes.
- **Easy to navigate** – Clear layout, large buttons, and mobile-friendly views.
- **Private** – All entries are stored securely and only accessible when signed in.
- **Encouraging** – No gamification or pressure; only useful, calm, and responsive features.

.. tip::

   Many students shared they preferred simplicity and flexibility over gamified rewards — so FITMIND keeps things calm and focused.

How Requirements Were Gathered
------------------------------

The user requirements were developed using:

- **Structured interviews** with university students from different fields
- **Feedback** collected during early prototypes and testing phases
- **Observations** about common habits, stress patterns, and feature expectations
- **Refinements** based on what students found helpful vs. unnecessary

.. warning::

   Features like badges and streaks were removed after feedback showed they added unnecessary pressure. FITMIND focuses on calm, self-paced engagement.

---

This completes the user-facing expectations of FITMIND. Next, we’ll outline how these features are translated into **system-level requirements** in the following section.

