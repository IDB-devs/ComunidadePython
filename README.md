# ComunidadeCursoPython
### Objective:

Create a Hashtag python course community site.

### Features:

Posting comments, homepage for post feed, creating users, changing profile image and blocking for non-logged in users.

### Languages:

- Python
    - Flask
- HTML
- CSS

### Files Explanation:

- main.py -> Main file, used to run the app/site.
- tests.py -> File for testing some features and the database.
- comunidadeimpressionadora folder -> Folder utilized for creating the actual website with it's features.
    - templates folder -> Folder with each HTML page in the website (frontend).
    - static folder -> Folder for CSS settings of HTML files and to store each user's profile images.
    - __init__.py -> File that when executed will start the project, loading the initial configurations of the website, database, and login management.
    - forms.py -> File to create the forms that will be present within the website such as login, account creation, changing profile image and creating posts (backend).
    - models.py -> Arquivo criado para estruturar como os dados dos usuários e das imagens serão armazenadas dentro do banco de dados (backend).
    - routes.py -> File to manage what goes on each HTML page in the templates folder and how they will work (backend).