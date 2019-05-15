Markov Chain Text Generator: Dad Joke Edition
=============================================

Prompt / Motivation
------
Markov Chain implementation at learning to generate dad jokes using icanhazdadjoke.com

## Dev Setup
### Python Setup
1. Install Python 3.7:
```bash
brew install python
```
2. Install virtualenv:
```bash
pip install virtualenv
```
3. Install virtualenvwrapper:
```bash
pip install virtualenvwrapper
```
4. Add these to your ~/.bash_profile. This will cause virtualenv to create all your virtual envs in your home directory.
```bash
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
export WORKON_HOME=$HOME/.venv
source /usr/local/bin/virtualenvwrapper.sh
```
5. Setup virtual environment.
```
mkvirtualenv dadjokes
```
6. Install requirements.txt for applicable environment.
```
pip install -r requirements/dev.txt
```

### Database

Dev environment is currently set up to use SQLite by default.

Migrate the database.
```bash
./manage.py migrate

```

Data sources are data driven (hear an echo?). So load the initial data into the database:
```
./manage.py loaddata database.json
```

### Local Server

This serves the django app locally.
```shell
./manage.py runserver
```

## Command-line Test
Run this to test out the API download, Markov Chain, and joke generation, all at once. 


```bash
./manage.py fetch_jokes 1000
```


### Webpack and React.js 
Install dependencies and start the webpack/React dev server.
```bash
cd src/frontend/
npm start
```

Next Steps
----------

- Train the Markov model using fitness functions.
- Convert Markov Chain build step to use matrices.
- Parallelize the Markov Chain build process to use multiple threads.
- Better caching.
- More data sources.
