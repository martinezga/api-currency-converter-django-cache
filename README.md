## 🎯 Purpose

Develop a currency converter API.

---

### ❤️ Available on

https://api-currency-converter.onrender.com

**Note**: Web Services on the free plan are automatically spun down after 15 minutes of inactivity. When a new request for a free service comes in, **Render** spins it up again so it can process the request.
This can cause a _response delay of up to 30 seconds_ for the first request that comes in after a period of inactivity.

---

### 🔧 Technologies used

* Python 3.8.12
* Django
* PostgreSQL
* Redis
* Docker
* Render - Cloud Application Hosting

### 📖 Description
- Passwordless authentication

### 🔎 Improvements
- Logging

### 🏁 API Usage

The API don't need registration by user, it uses `Passwordless authentication` workflow.

That means you don't have and don't need to remember your password because we will send you and email with a token everytime you need to access our application.

In that way we ensure you use a valid email 😀 and simplify the sign-in experience.

Automatically creates users and according given domain creates admins privileges.

For testing purposes accounts with emails ending on `yopmail.com` are admin.

To create an admin account go to: https://yopmail.com/ this service allow to have a disposable email address with inbox to receive real emails.

### ✨ Local environment set up

There are two set up, using pipenv or docker-compose. Next steps are common between them.

- Copy _.env to .env:

        $ cp _.env .env

- Update .env file with the right values

#### Using pipenv

- Install dependencies using pipenv. 
In case you don't have pipenv, execute: `pip install pipenv` first.

        $ pipenv install

    To allow DB use, install psycopg2-binary with:

        $ pipenv install --dev

- Run the development server executing:

        $ pipenv run server

- To create new django application:

        $ mkdir ./api/apps/new_app_name
        $ pipenv run startapp new_app_name api/apps/new_app_name

#### Using docker-compose

- Execute:

        $ docker-compose up -d build

- To stop it execute:

        $ docker-compose stop

**To test successfully set up visit: http://localhost:8000**

### ☁️ Production environment

Set up with Gunicorn, psycopg2 and Docker deploy. Use the [Dockerfile](Dockerfile) file.

To use [render](https://render.com/) connect your GitHub repository and allow automatic deploy by push.

In server needs to configure this list of environment variables [_.env](_.env).

**Keep an eye on PORT value** It is required to deploy the app, Heroku and Render assign it automatically.

On Render you could create Postgres Database and Redis instance for free.

Have a nice coding, Pythonizate!

---
⌨️ with ❤️ by [Gabriella Martínez](https://github.com/martinezga) 😊
