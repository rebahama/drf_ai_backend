## Smart Mechanic backend
The backend for Smart mechanig was build using Django and Django rest framework. This api will make it possible to Create/delete a post and  Register and create an account, Gemini is used for taking input and request and to display the result

# Website link
* [Deployed website](https://mechanic-ai-backend-30fbbccc99ba.herokuapp.com/)


# Technology 


* Django 5.2.7 – latest stable version. Compatible with DRF 3.16.1.

* dj-rest-auth + allauth – handles authentication and registration endpoints.

* djangorestframework_simplejwt – JWT authentication.

* psycopg2 – PostgreSQL database adapter.

* gunicorn – for production deployment.

* Google Generative AI libraries – to integrate AI-based solutions.

* Heroku was used for deployment.

* Github was used for develompment.


# Libraries and deployment

## Deployment


1. Install Django 5.2.7
pip3 install "Django==5.2.7"

2. Install Pillow for image handling
pip3 install Pillow

3. Install Django REST Framework
pip3 install djangorestframework==3.16.1

4. Install dj-rest-auth for authentication endpoints
pip3 install dj-rest-auth==7.0.1

5. Install Django Filter for API query filtering
pip3 install django-filter==25.2

6. Install dj-rest-auth with social authentication
pip3 install "dj-rest-auth[with_social]"

7. Install JWT support
pip3 install djangorestframework-simplejwt==5.5.1

8. Install Django Allauth (required for social auth)
pip3 install django-allauth==65.13.0

9. Install PostgreSQL adapter and database URL helper
pip3 install psycopg2==2.9.11 dj-database-url==3.0.1

10. Install Gunicorn (for deployment)
pip3 install gunicorn==23.0.0

11. Install CORS headers (if frontend is served separately)
pip3 install django-cors-headers==4.9.0

12. Install Google Generative AI libraries (for AI integration)
* pip3 install google-ai-generativelanguage==0.6.15
* pip3 install google-api-core==2.28.1
* pip3 install google-api-python-client==2.185.0
* pip3 install google-auth==2.42.1
* pip3 install google-auth-httplib2==0.2.0
* pip3 install google-generativeai==0.8.5
* pip3 install googleapis-common-protos==1.71.0

13. pip3 freeze > requirements.txt

14. Create a Procfile in the main directory of the project and inside add the following line:
release: python manage.py makemigrations && python manage.py migrate
web: gunicorn DRF_AI.wsgi


# Deployment

1. Go to Heroku and create a new app.

2. After creating a new app, go to "resources" and type " Heroky postgres" and add it.

3. Go to settings and scroll down to "config vars" and a DATABASE_URL will be created for the database.

4. Create a config var named CLOUDINARY_URL and paste in the api key from Cloudinary.

5. Create a config var named SECRET_KEY and paste in a password.

6. Add DISABLE_COLLECTSTATIC and set it to 1.

7. Connect your Heroku with Github and finally click deploy.




# Develop in local enviorment

1. Create a python file called env.py and import os

2. Add os.environ["DATABASE_URL"] = value from heroku

3. Add os.environ["SECRET_KEY"] = value from heroku

4. Add os.environ["DEV"] = '1'

5. Add os.environ["GEMINI_API_KEY"] = value from heroku

6. Type python3 manage.py runserver to start up the browser.
