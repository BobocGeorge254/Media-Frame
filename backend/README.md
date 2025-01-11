## Requirements

- Python 3.11.1
- Django 5.1.3 (and any other dependencies specified in `requirements.txt`)


## Setup Instructions

Follow these steps to set up and start the application:

### 1.Clone the Repository

   Clone the repository to your local machine:
   - git clone https://github.com/BobocGeorge254/Media-Frame.git
   - cd backend

### 2.Create and activate the virtual enviroment

    To isolate dependencies, create a virtual environment within the project directory:
    - python -m venv env

    In order to activate the virtual enviroment use OS specific command:
    - Windows: env\Scripts\Activate
    - UNIX: source env/bin/Activate

### 3.Install requirements

    Install the necessary dependencies from the requirements.txt file:
    - pip install -r requirements.txt

    If you install new dependencies at any point, please use:
    - pip freeze > requirements.txt

### 4.Set Up the Database

    Navigate to the main project directory and apply migrations to set up the database:
    - cd media_frame
    - python manage.py makemigration
    - python manage.py migrate

### 5.Start the Development Server

    - python manage.py runserver



## Good to know 

### Database

 SQLite databases are very easy to use in development, does not require a separate server, however not ideal because of scalability and features constraints (what more can you expect from a single file :D)
