# food-app

New app to cook your fav dish instantly.

In this period of unease when people are looking for various hobbies to distract themselves from the tensions of daily life during a pandemic, anybody with a social media account can observe the increase in the number of people dabbling in the culinary arts. The application that we would like to present seeks to encourage and simplify such endeavours. Moreover, even after this era of the pandemic, this application's relevance does not fade away with time. 
This application is different from other recipe applications because of the intended search system. Not only can a user search for a specific dish by name to obtain it's recipe, users may input the supplies, utensils and cooking equipment (such as an oven) using check boxes to view the various dishes that are possible, where the default view will be in a descending order of upvotes . Users can add recipes which strike their fancy or variations in pre-existing recipes as new entries after creating a handle connected to their email ids or social media accounts. This ensures that the application never stops improving itself.

# Installation

```bash
# step 1: Update your repositories
	sudo apt-get update
# step 2: Install pip for python 3
	sudo apt-get install build-essential libssl-dev libffi-dev python-dev
	sudo apt install python3-pip
# step 3: Use pip to install virtualenv
	sudo pip3 install virtualenv
# step 4: launch the virtual environment
	virtualenv -p python3 <name of virtual environment>
# step 5: activate the environment
	. <name>/bin/activate

# exiting the virtual environment
	deactivate
```

# Instructions for creating virtual environment

```bash	
 python3 -m virtualenv venv
	# This simply creates a Virtual Environment venv for the app development.
 . venv/bin/activate
	# The Virtual Environment is now activted ie, we are now in this environment.
 python3 -m pip install -r requirements.txt
	# pip installs all the packages specified in the requirement.txt file
 python3 flaskmain.py
	# runs the flaskmain.py file which takes us to the website.
```

# Instructions for running the web application

```bash
# step 1: Open terminal in the master directory and run the python file 'seed.py'
	python seed.py
# step 2: Now set the location of flask application
	export FLASK_APP=flaskmain.py
# step 3: Now run the application
	flask run
# instead of step 2 and step 3 running the python app with the following command will also work
	python flaskmain.py
# visit http://localhost:5000/ or http://127.0.0.1:5000/ to see the application running
		
```

# contributers

* Sivaprasad - sivaprasad2000
* Ivin Kuriakose - ivin-3-69
* Pranoy Chithra - RayChithra
* Rhuthik -rhuthik
* Vivek - vivek-r-2000

