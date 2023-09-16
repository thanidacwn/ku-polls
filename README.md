# KU Polls: Online Survey Questions 
[![Testing](https://github.com/thanidacwn/ku-polls/actions/workflows/python-app.yml/badge.svg?branch=iteration2)](https://github.com/thanidacwn/ku-polls/actions/workflows/python-app.yml)

This application, developed during the  [Individual Software Process](
https://cpske.github.io/ISP) course at Kasetsart University, expands upon the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) project to facilitate online polls and surveys while incorporating extra features.

## How to install and configuration
- [Installation and configuration](https://github.com/thanidacwn/ku-polls/blob/iteration4/installation.md)
## How to Run
1.Start the virtual environment
```sh
source env/bin/activate
```
On Microsoft Windows:
```sh
. env/bin/activate
```
2.How to set values for externalized variables

create file name `.env` to configuration **note that you may get your secretkeys [here](https://djecrety.ir)**

`.env` file template looks like [sample.env](sample.env) you can modify value and copy it into `.env`

3.Install requirements inside the virtual environment:
```sh
pip install -r requirements.txt
```
4.Run migrations
```sh
python3 manage.py migrate
```
5.Run tests
```sh
python3 manage.py test
```
6.Install data from the data fixtures
```sh
python3 manage.py loaddata data/*.json
```
7.Run the application
```sh
python3 manage.py runserver
```

Then, go to `http://127.0.0.1:8000/` or `localhost:8000/` for application.

| Username  | Password  |
|-----------|-----------|
|   panda   | Jumbo@123 |
|   dinosaur   | Cute@123 |
|   bhayu   | Saifha@123 |
|   coconut   | Juice@123 |

8.Exit the virtualenv
```sh
deactivate
```

## Project Documents

All project documents are in the [Project Wiki](https://github.com/thanidacwn/ku-polls/wiki)

* [Vision Statement](https://github.com/thanidacwn/ku-polls/wiki/Vision-Statement)
* [Requirements](https://github.com/thanidacwn/ku-polls/wiki/Requirements)
* [Project Plan](https://github.com/thanidacwn/ku-polls/wiki/Development-plan)
* [Task Board](https://github.com/users/thanidacwn/projects/7)
* [Iteration 1 Plan](https://github.com/thanidacwn/ku-polls/wiki/Iteration-1-Plan)
* [Iteration 2 Plan](https://github.com/thanidacwn/ku-polls/wiki/Iteration-2-Plan)
* [Iteration 3 Plan](https://github.com/thanidacwn/ku-polls/wiki/Iteration-3-Plan) and [Domain model](https://github.com/thanidacwn/ku-polls/wiki/Iteration-3-Plan)
* [Iteration 4 Plan](https://github.com/thanidacwn/ku-polls/wiki/Iteration-4-Plan)