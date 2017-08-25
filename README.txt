Running the application
1. Activate virtual environment using  " source flaskenv/bin/activate"
2. from the root(cyberhawk17) directory run the python2 file run.py

Project Directory
cyberhawk17
      /flaskenv
      /tmp
      /app
          /static
          /templates
          __init__.py
          views.py
      run.py
      README.txt

1. cyberhawk17 is the root directory. the 'run.py' file  ,  readme.txt and app package are in this directory. A
    tmp folder and the environment are also in this directory

2. the 'app' subdirectory has the __init__.py file which initiates the Flask application instance application .
   I used the name application for the instance instead of app to avoid confusion between the package(folder)
   and the flask instance.

3. The views.py file is where we write all the app routes. Note that we will use
              @application.route("/")
  instead of
              @app.route("/")
4. models.py is the file where we declare all the the SQLAlchemy database models.
