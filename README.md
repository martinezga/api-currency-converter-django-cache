## 🎯 Purpose

Develop a currency converter API.

---

### ❤️ Available on

https://api-currency-converter.onrender.com

---

### 🔧 Technologies used

* Python 3.8.12
* Django
* PostgreSQL
* Redis
* Docker
* Render - Cloud Application Hosting

### 📖 Description


### 🔎 Improvements


### 🏁 API Usage


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
- 
**To test successfully set up visit: http://localhost:8000**

### ☁️ Production environment

Set up with Gunicorn, psycopg2 and Docker deploy. Use the [Dockerfile](Dockerfile) file.

To use [render](https://render.com/) connect your GitHub repository and allow automatic deploy by push.

In server needs to configure the follow environment variables (minimal ones):

- ENV
- DATABASE_URI
- CACHE_REDIS_URL

Full environment variables list is available on [_.env](_.env) file.

**Keep an eye on PORT value** It is required to deploy the app, Heroku and Render assign it automatically.

On Render you could create Postgres Database and Redis instance for free.

Have a nice coding, Pythonizate!

---
⌨️ with ❤️ by [Gabriella Martínez](https://github.com/martinezga) 😊
