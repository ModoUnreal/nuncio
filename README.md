# Nuncio
The fair news aggregator, allowing for all kinds of news from
any real news sources.

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

And then install all the necessary requirements using:

```bash
$ pip install -r requirements.txt
```

```bash
$ python nuncio.py
```

The website should be running in your local network, so probably `localhost:5000`.
