Testing
=======

Overview
--------

Testing played a critical role in ensuring FITMIND is stable, functional, and user-friendly. A combination of **manual testing**, **unit testing**, and **integration testing** was used throughout development to verify both frontend and backend behavior.

The goal was to validate user interactions, system logic, and data handling across all key features, while also ensuring cross-device compatibility.

.. tip::

   Testing was performed continuously throughout development — not just at the end — which helped catch and fix issues early.

Test Types
----------

1. **Manual Testing**

   Manual testing was conducted regularly by interacting with the app in a browser. It focused on:

   - Form behavior and input validation
   - Navigation flow and access restrictions
   - Page responsiveness across desktop and mobile
   - UI elements (e.g., charts, pop-ups, search field)

   .. note::

      Manual testing was especially useful for verifying dynamic behaviors like the live exercise chart and real-time pop-up reminders.

2. **Unit Testing (Backend)**

   Backend logic was tested for core features such as:

   - User authentication (login/logout/registration)
   - Form validation for stress, exercise, notes, and reminders
   - Reminder time validation and scheduling logic
   - Data consistency when saving to the SQLite database

   .. tip::

      Tests also checked for edge cases like empty input, invalid stress values, and duplicate reminder times.

3. **Integration Testing**

   Integration testing validated the communication between frontend and backend:

   - Ensured form submissions correctly updated charts and logs
   - Verified feedback from backend (e.g., Breathe Flow suggestions)
   - Confirmed data was stored and retrieved accurately per session
   - Tested reminder alerts across different pages

   .. seealso::

      Integration testing confirmed that reminders, charts, notes, and suggestions worked smoothly across the entire system.

Tools Used
----------

- **Browser Developer Tools** – Console and network tabs for inspecting errors and AJAX responses
- **Postman** – For sending test requests to backend endpoints
- **VS Code** – With Python extension for debugging backend logic
- **Git** – For version control and collaborative issue tracking

What Was Tested
---------------

**Stress Page**

- Validated stress input (1–5) with emojis  
- Notes stored with stress entries  
- Suggestions triggered for high stress  
- Backend and frontend sync confirmed  

**Exercise Page**

- Logged cardio, stretching, and custom inputs  
- Bar chart updated after each log  
- Suggestions adapted based on recent stress logs  
- All logs displayed in a growing list  

**Breathe Flow Tool**

- Launched from multiple pages (navigation and stress suggestion)  
- Publicly accessible without login  
- Animation and timing consistent across browsers  
- Feature worked independently and repeatedly  

**Notes Page**

- Notes saved with timestamp  
- Entries listed in scrollable view  
- Search field filtered notes by keywords  
- Data remained consistent on refresh  

**Reminders**

- Created reminders with custom messages and times  
- Pop-up with sound triggered correctly across all pages  
- Reminders persisted across session navigation  
- Reminder list displayed accurately  

**Authentication System**

- Successful registration, login, and logout  
- Session-based access control enforced  
- Protected pages blocked unauthenticated users  
- Breathe Flow remained accessible without login  

.. warning::

   All protected routes were tested for direct URL access — unauthorized users were correctly redirected.

Test Outcome Summary
--------------------

- Core functionality for all pages performed as expected  
- Cross-browser and device tests confirmed responsive design  
- No critical bugs were found in session control, form handling, or reminder alerts  
- Minor issues (e.g., button alignment, emoji padding) were resolved during UI testing  


.. note::

   Automated test coverage is currently limited to backend logic, but expanding it to include full end-to-end testing is part of the future roadmap.
