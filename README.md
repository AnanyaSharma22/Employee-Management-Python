# Employee-Management-Python

Overview:

The Employee Management project consists of an admin in which admin user can login and add, edit managers profile and a website that enables a manager to list, add, edit an employee details.

This application is based on python, django and django REST framework, Angular and typescript, HTML, CSS.

In this application, I have created backend APIs and admin for basic user authentication system, list, create, retrieve and update employee.

Steps To Setup The Project:

1. Git clone the repository https://github.com/AnanyaSharma22/Employee-Management-Python.git
2. Make sure you have python3 installed in your system.
3. Create a virtual environment on windows with venv, with the following command:
   python -m venv env
4. Activate the virtual environment with the command: .\env\Scripts\activate
5. Install the requirements file with the following command:
   pip install -r requirements.txt
6. Create a superuser to login into the admin by running the following command in the terminal:
   python manage.py createsuperuser
7. Then, run the project with command: 'python manage.py runserver' and login in the admin with superuser credentials.
8. In admin, go to managers tab and create a user with checking it's is_appuser and is_active checkbox. This will an appuser.
9. Now, go to applications tab and create an application with the name 'EMPLOYEE-MANAGEMENT' and select the user which you have created in the above step, cleint type 'confidential' and grant-type 'resource owner password based'.
10. Now, we need to set these credentials in Angular project environment.ts file.

In your browser, visit http://localhost:8000 to view, access and test the employee management application.
