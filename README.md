# Nuncio
The fair news aggregator, allowing for all kinds of news from
any real news sources.

https://nuncio-production.herokuapp.com

## Setting up
Get the source code using the following:

```bash
$ git clone https://www.github.com/ModoUnreal/nuncio.git
```

Once inside the nuncio directory you should probably set up a virtual environment:

```bash
$ virtualenv <env_name>
$ <env_name>\Scripts\activate
```

(Replace `env_name` with whatever you want to call it)

Then set up the flask app as such:

```bash
$ export FLASK_APP=nuncio.py
```

Or if you are using Windows:

```bash
$ set FLASK_APP=nuncio.py
```

And then install all the necessary requirements using:

```bash
$ pip install -r requirements.txt
```

Prepare the database by doing:

```bash
$ flask db init
$ flask db migrate -m "users table"
$ flask db upgrade
```

This will initialise all of the tables in the models.py file.


Then run the server....

```bash
$ python nuncio.py
```

The website should be running in your local network, so probably `localhost:5000`.
