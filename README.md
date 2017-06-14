# Wildflower Foundation Dev Challenge

### Goal: Build UI for email template used by teachers

## Set-up
* Fork Repo
* Create Local Repo
* `git pull origin master`
* `npm install`

Install Pip - Run these commands
* `curl -O http://python-distribute.org/distribute_setup.py`
* `python distribute_setup.py`
* `curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py`
* `python get-pip.py`
* `pip install virtualenv`
* `virtualenv [name dir]` - install virtual env into project Repo
* `pip install -r requirements.txt` - Install Dependencies
*  `export FLASK_APP=app/__init__.py`
* `export APP_CONFIG_MODE=development`

Export the following variables with their assigned values
* `export APP_CONFIG_MODE`
* `export MAIL_USERNAME`
* `export MAIL_PASSWORD`
* `export SURVEY_MONKEY_OAUTH_TOKEN`
* `export AWS_ACCESS_KEY_ID`
* `export AWS_SECRET_ACCESS_KEY`
* `export S3_BUCKET`
* `export TRANSPARENT_CLASSROOM_API_TOKEN_CAMBRIDGE`
* `export TRANSPARENT_CLASSROOM_API_TOKEN_SANDBOX`
* `export SLACK_API_TOKEN`
* `export SLACK_VERIFICATION_TOKEN`

* `flask run`


## Global Heroku config/env vars:

  - heroku config:set APP_CONFIG_MODE=production
  - heroku config:set MAIL_USERNAME=TBD
  - heroku config:set MAIL_PASSWORD=TBD


## TODO:
  - set tablename_prefix and blueprint_name in __init


  Add flask cli command to create scaffolding blueprint w. empty req'd files
  post_compile in the blueprints, composited to root
  requirements.txt in the blueprints, composited to root


  Automatically prefix table names in blueprints (flask_sqlalchemy is causing problems)
  blueprint_name in tests feels leaky
  webpack config in the blueprints, composited to root
  nltk_data dir in root is leaky
  Config is still a global namspace; isolate each blueprint's config
  make 500 global and apply everywhere -  maybe copy template when create, update email
