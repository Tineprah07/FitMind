Future Work
===========

Overview
--------

While FITMIND successfully delivers its core features — stress tracking, exercise logging, breathing guidance, note-taking, and reminders — there is still room for improvement. Future development will focus on deepening the user experience, improving scalability, and expanding the app’s capabilities based on feedback, testing, and evolving user needs.

The following ideas are under consideration for future updates.

Planned Features and Improvements
---------------------------------

1. **Progress Dashboard**

   Introduce a central dashboard where users can view long-term trends in their stress and exercise logs. This may include line graphs, daily averages, and filter options (e.g., week, month, semester).

   .. note::
      This would help students identify patterns over time and reflect on progress more visually.

2. **Recurring and Editable Reminders**

   Upgrade the current reminder system to support editing, deleting, and setting recurring reminders (daily, weekly). A dedicated reminder management interface could be added.

3. **Custom Tags and Categories**

   Allow users to tag stress causes or exercise types with custom labels. These tags could later be used to group logs and generate insights like, “You often feel stressed before deadlines.”

4. **Dark Mode and UI Themes**

   Add dark mode support to reduce eye strain, especially for night use. Offer theme customization so users can personalize the app's appearance.

5. **Mobile Optimization & PWA Support**

   While FITMIND is already responsive, deeper mobile optimization would improve usability on smaller screens. Turning the app into a Progressive Web App (PWA) would allow users to "install" it on their phone, use it offline, and receive native notifications.

6. **Multi-language Support**

   Translate the app into other languages to serve a broader user base, beginning with those most relevant to FITMIND’s target audience (e.g., Twi, French, Spanish).

7. **User Feedback System**

   Add a simple in-app form where users can submit feedback, suggestions, or report issues directly. This would help guide future feature prioritization and usability improvements.

Technical Enhancements
----------------------

1. **Database Upgrade**

   Move from SQLite to PostgreSQL to support remote deployment, concurrent users, and improved performance.

2. **Modular Code Refactor**

   Refactor backend code into modular components (e.g., separate files for each manager), making it easier to maintain, scale, and add new features.

3. **Continuous Integration & Automated Testing**

   Implement CI tools like GitHub Actions to run tests automatically during development. Expand test coverage, especially for frontend interactions and edge cases.

4. **Improved Error Handling**

   Provide more user-friendly error messages and fallback behavior when issues occur (e.g., reminder time format errors or missing input).

Deferred Features
-----------------

- **Community Page**

   This feature was originally envisioned as a space for users to share progress and wellness tips. It was removed based on user feedback and development scope.

   .. note::
      The Community Page may be revisited in future versions if demand rises and privacy concerns can be addressed.
