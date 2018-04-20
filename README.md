# NBA-Trade-Machine
A new and updated design to ESPN's Trade Machine

# How to run
You can run the following command in the main directory:
```
python manage.py runserver
```

Then open http://localhost:8000/nbatrademachine/ in your browser.

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
		- base.html is a base template which some other templates inherit
		- index.html is the main index template
		- home.html inherits from base.html and supports showing a user's name when they are logged in
		- signup.html is a template which is used for creating a new account
		- login.html is used for logging in
		- trade.html is the main trade template
		- success.html is the template that is routed to in the case of a trade being successful
		- failure.html is the template that is routed to in the case of a trade being unsuccessful
	- settings.py is a file that is required for Django applications
	- urls.py is the file which helps route requests to views
	- wsgi.py is another file that is required for Django applications
	- There are also various __init__.py files which are required for Django applications.
- web_scraping is a directory which houses a couple of Python scripts that were used for web scraping using BeautifulSoup
	- These scripts were then used to help populate the database
	- contract_script.py was used to mainly get the contract information for a given player
	- web_scraping_script.py is a more general script that gets various statistics for a given player




