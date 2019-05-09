Markov Chain Text Generator: Dad Joke Edition
=============================================

Prompt / Motivation
------

We’d love to give you the opportunity to build a small full stack application.

  We’d like you to build a [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) automated text generator. Our only restriction is that the data source for your application must use the [icanhazdadjoke API](https://icanhazdadjoke.com/api), which has “internet's largest selection of dad jokes”. So think of your application as a new dad joke generator!  

You can use any tools you wish to create your application, including any libraries or languages you find useful, however we would like for you to manually implement the Markov generation logic in the language of your choosing. As you are building out your application consider interesting joke generation and application efficiency as your top priority!

As a stretch goal, we’d like for you to add caching to your application.

When you are ready to submit your test, send us either a .zip of your application in the link below or share a link to a repository. Keep in mind we will be cloning and spinning up your application locally to evaluate it.
 
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

- Convert Markov Chain build step to use matrices.
- Parallelize the Markov Chain build process to use multiple threads.
