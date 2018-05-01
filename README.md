# NBA-Trade-Machine
A new and updated design to ESPN's Trade Machine

# Usage
Unfortunately, we were not able to successfully deploy our application to Heroku due to some complications. Thus, we do not have a live demo of our application at this time. However, we have included detailed instructions on how to run the project on your local machine.

Prerequisites

- An internet browser (we recommend Google Chrome)
- Python 2.7 or higher (instructions to install Python on various operating systems can be found online)

## Step 1 - Install Django

As our project uses Django, it must be installed for the project to run correctly. If you already have Python installed, this should be fairly straightforward. You can follow the directions given here: https://docs.djangoproject.com/en/2.0/topics/install/#install-the-django-code

Essentially, you will need to install pip, and afterwards you can run this command:

```
pip install Django
```

There is no need to install virtualenv for our project, so you can skip step 2 in the link provided. Note that we used Django version 1.11 for our project, but version 2.0 should also work fine in most cases.

## Step 2 - Verify Django installation

Try to run this command:

```
python -m django --version
```

If a version number is printed, then your installation was successful.

## Step 3 - Run project

Before attempting this step, it is important to note that you must be in the main directory of the project. Specifically, this is the directory in which manage.py sits. When you are in this directory, you can run this command:

```
python manage.py runserver
```

When running this command for the first time, it may take some time to start the project. Once it is running, you can open your internet browser and type in localhost:8000 in the address bar and hit Enter. Then, you should see the main page of the application.

## Step 4 - Using the application

You can use the application as a guest, or log in with a username and password that was already registered. You can make an account normally and it should work, but if you would like to log in with an existing account without making a new one then you can use the following username and password combination:

username: final
password: password123

This should let you into the application.

After that, you're in! You can try out different trades, and see what happens. Just to get you started, an example of a successful trade would be to trade Timofey Mozgov from the Brooklyn Nets to the Golden State Warriors, and trade Klay Thompson from the Golden State Warriors to the Brooklyn Nets. An example of an unsuccessful trade would be the same trade scenario, except also trade Jeremy Lin from the Brooklyn Nets to the Golden State Warriors.

Have fun!

# Structure
- manage.py is the main file needed to run the server
- the sqlite3 files are for the database
- mysite is the directory where almost all of the project contents are housed
	- core is the directory which contains the files that handle the back-end and connecting to the front-end
		- the migrations directory houses important information for the back-end
		- admin.py contains the models which can be viewed in the admin panel
		- apps.py defines the apps we are using (in this case, it's just core)
		- models.py defines the models we are using (Team and Player)
		- views.py defines the views that are routed to from urls.py
	- static contains static files for our project
		- the css directory contains all relevant CSS files to our project
		- the js directory contains all relevant JS files for our project
	- templates contains the Django templates we used
	- settings.py is a file that is required for Django applications
	- urls.py is the file which helps route requests to views
	- wsgi.py is another file that is required for Django applications
	- There are also various __init__.py files which are required for Django applications.
- web_scraping is a directory which houses a couple of Python scripts that were used for web scraping using BeautifulSoup
	- These scripts were then used to help populate the database
	- contract_script.py was used to mainly get the contract information for a given player
	- web_scraping_script.py is a more general script that gets various statistics for a given player