Setup Instructions
==================

Overview
--------

This guide will walk you through setting up the FITMIND application on your local machine for development, testing, or evaluation purposes.

Whether you're using Windows or macOS, the steps below will help you install dependencies, configure the environment, and run the app.

.. note::

   This setup assumes basic familiarity with the terminal/command prompt and Python. If you're new to virtual environments or pip, consult Python’s official documentation for more guidance.

Clone the Repository
--------------------

Start by cloning the project from GitHub (or your private repo):

.. code-block:: bash

   git clone https://github.com/yourusername/FITMIND-APP-MAIN-PROJECT.git
   cd FITMIND-APP-MAIN-PROJECT

.. tip::

   Replace the GitHub URL with the actual repository location if needed.

Environment Setup
-----------------

The steps differ slightly depending on your operating system.

.. contents::
   :local:
   :depth: 1

Windows Instructions
--------------------

1. **Navigate to your project directory**:

.. code-block:: batch

   cd "c:\Users\gyamp\OneDrive\Desktop\FITMIND\FITMIND-APP-MAIN-PROJECT"

2. **Create a virtual environment**:

.. code-block:: batch

   python -m venv venv

   :: or

   py -m venv venv

3. **Activate the virtual environment**:

.. code-block:: batch

   venv\Scripts\activate

   :: or (for PowerShell)

   .\venv\Scripts\Activate.ps1

4. **Install required dependencies**:

.. code-block:: bash

   pip install flask
   pip install flask-login
   pip install flask-migrate
   pip install flask-wtf
   pip install flask-mail
   pip install itsdangerous
   pip install sqlalchemy
   pip install password-strength

macOS Instructions
------------------

1. **Navigate to your project directory**:

.. code-block:: bash

   cd ~/Desktop/FITMIND/FITMIND-APP-MAIN-PROJECT

2. **Create a virtual environment**:

.. code-block:: bash

   python3 -m venv venv

3. **Activate the virtual environment**:

.. code-block:: bash

   source venv/bin/activate

4. **Install required dependencies**:

.. code-block:: bash

   pip install flask
   pip install flask-login
   pip install flask-migrate
   pip install flask-wtf
   pip install flask-mail
   pip install itsdangerous
   pip install sqlalchemy
   pip install password-strength

Running the Application
-----------------------

Once your environment is set up, run the application using:

.. code-block:: bash

   python main.py

Then open your browser and go to:

.. code-block:: none

   http://127.0.0.1:5000/

.. tip::

   Ensure your `main.py` file contains the Flask app setup and is properly configured to run the server.

Testing
-------

FITMIND includes backend unit testing capabilities. To run tests, follow the steps below:

1. **Install testing dependencies**:

.. code-block:: bash

   pip install pytest
   pip install Flask-Testing

2. **Run the test suite**:

.. code-block:: bash

   pytest tests

.. note::

   All test files should be located in a folder named `tests/`. Make sure this folder exists and contains your `.py` test scripts.

Project Structure (Simplified)
------------------------------

A simplified overview of the project structure:

.. code-block:: none

   FITMIND-APP-MAIN-PROJECT/
   ├── main.py
   ├── model.py
   ├── instance/
   ├── migrations/
   ├── static/
   ├── templates/
   ├── tests/
   ├── FitMind/
   ├── docs/
   ├── venv/
   ├── README.md
   ├── README.rst
   ├── pyproject.toml
   └── readthedocs.yaml

.. tip::

   Your `main.py` file serves as the app entry point. It should initialize Flask, register routes, and start the server.

Troubleshooting
---------------

- **Command not recognized**  
  Make sure the virtual environment is activated and you're using the correct Python command.

- **Permission denied (macOS)**  
  Use `chmod +x` or run with elevated permissions if needed.

- **Module not found**  
  Double-check that you've installed all required dependencies and that your virtual environment is active.

Conclusion
----------

After completing these steps, your FITMIND application should be fully functional on your machine. You're now ready to explore the app, contribute code, run tests, or demonstrate features.
