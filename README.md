# django_to_heroku
previous django blog modified to deploy to heroku


_For AWS EC2 provides only one year hosting, and further produces considerable cost to such a little shitty website, I sought to transfer to a cheap or free platform to get hosted to avoid further trouble. Heroku has hosted a large number of small websites with few budgets and provides excellent user interface and experience._

**Cons:**

- **Heroku filesystem is ephemeral, which means any static files uploaded from admin backend won't be stored long. The dyno reboots every day. Probably your uploads disappear after a nap, sort of like cache huh? Yes, annoying. So, AWS S3 is strongly recommended as your storage service.**
- **The timeout limit of web requests processed by Heroku is set to 30 seconds and can't be set higher. So make sure no large images to be uploaded.**

_Anyway, if you still decide to harness this free platform, prepare your local django project and follow the steps below to make a successful deployment._

1. Clear all migration files under migrations directories in each app

2. Make migrations again. Since some models relies on others, I'm gonna make migration for each app one by one:

   ```python
   # userprofile contains all users' info, so it's the most basic
   python3 manage.py makemigrations userprofile
   # post, with author, tags, etc, is fundamental as well
   python3 manage.py makemigrations post
   # album
   python3 manage.py makemigrations album
   # comment relies on users, posts and photos
   python3 manage.py makemigrations comment
   # about, the lowest priority
   python3 manage.py makemigrations about
   # in case if there is something left
   python3 manage.py makemigrations
   ```

3. On Heroku, create an app and a PostgreSQL db connected to the app

4. Add the domain name to ALLOWED_HOSTS: _my_heroku_app_name_.herokuapp.com

5. Install heroku command CLI

6. Activate the virtual env: source the "activate" file under "bin" directory

7. cd _my/project/directory_

8. heroku login

9. pip3 install gunicorn

10. pip3 freeze > requirements.txt

11. touch .Procfile and write:

    > web: gunicorn _dir_where_wsgi.py_is_.wsgi:application --log-file -

    to tell heroku that it's a web app run with gunicorn through wsgi.

12. Initialise git and push to heroku:

    - git init
    - build .gitignore file and put file names to be ignored
    - heroku git:remote -a _my_heroku_app_name_
    - heroku config:set DISABLE_COLLECTSTATIC=1
    - git status to check files and directories to be committed
    - git add .
    - git commit -m "first commit"
    - git push heroku master

13. Set all the environ variables, for example: heroku config:set DJANGO_DEBUG=0

    Attention: AWS_S3_REGION_NAME also needs to be set. Otherwise, false regoin causes 400 bad request error.

14. "heroku run bash" to enter heroku bash command line (ubuntu)

15. python3 manage.py collectstatic

16. python3 manage.py migrate. Since makemigrations already done and pushed to heroku, only migrate needed to create tables in PostgreSQL

17. python3 manage.py createsuperuser

_If there is any error, heroku logs --tail to check. Further, sentry-sdk addon is suggested as the logging system to get a crystal clear error report to your email, since the local logging setting disfunctions on Heroku._

---
## Apply AWS S3 to store static files for Django projects

For any "upload_to" in models.py files, we can use AWS S3 to store these static files.

- Create an AWS S3 bucket. The name better consists of full letters, and set default for all other parameters.

- Set CORS configuration in permissions.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
   <CORSRule>
       <AllowedOrigin>yourdomain.com</AllowedOrigin>
       <AllowedMethod>GET</AllowedMethod>
       <AllowedMethod>POST</AllowedMethod>
       <AllowedMethod>PUT</AllowedMethod>
       <AllowedHeader>*</AllowedHeader>
   </CORSRule>
   </CORSConfiguration>
   ```

- Search IAM in AWS service, create User and get AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.

- Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and S3_BUCKET_NAME in system environment variables to hide them in .bash or .zshrc file. Don't forget to source it.

- pip3 install boto3 django-storages. Don't forget to pip3 freeze > requirements.txt

- Add "storages" to INSTALLED_APPS in settings.py. Also, append these to the end, just as what the official doc of django-storage module suggests:

   ```python
   AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
   AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
   AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
   AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
   # if a user upload a file with the same name as another in s3, rename it automatically
   AWS_S3_FILE_OVERWRITE = False
   # some issue with the default value, so reset it to None
   AWS_DEFAULT_ACL = None
   # set the storage backend
   DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
   ```

Now, we are free to upload any static files as usual. But they will be stored in AWS S3, instead of under static directory on server.
