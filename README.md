# Casting Agency API

Casting Agency API is a RESTFUL API which is deployed on Heroku. The API provides the details of actors and movies and based on the user's permissions allow him/her to add new actors or movies. This project is submitted as a Capstone for the Full Stack Nanodegree program. The application covers all the concepts which I have acquired throughout the entire course.
The technologies used in the project are:
- Flask (Server)
- Postgres (Database)
- SQLAlchemy (ORM for interacting with the DB)
- Auth0 (Authentication)
- Heroku (Deployment)

## Getting Started

### Installing Dependencies

#### Python 3.8

This project is built using Python 3.8
Head to the python website to get the latest version

#### PIP Dependencies

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Heroku Setup
The app is hosted on Heroku at the following URL: https://casting-agency-raghuchandan1.herokuapp.com/
The API endpoints can be accessed from the same URL as mentioned above.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`. 
- Authentication: This version of the application requires the user to have the appropriate permissions to access the endpoints. It uses the Auth0 sign in for authentication. The app verifies that the user has the required permissions using the JWT.
  - Add the appropriate JWT as a `Bearer` token to the `Authorization` segment of the `Header`
  
### Authentication
Use https://casting-agency-raghuchandan1.herokuapp.com/login to login and get the JWT
I have added some pre-defined users with the following roles which you can use to get the required JWT token:
- Casting Assistant    
  - `ca@castingagency.com`:`Qaz12345`
- Casting Director  
  - `cd@castingagency.com`:`Qaz12345`
- Executive Producer  
  - `ep@castingagency.com`:`Qaz12345`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Roles
- Casting Assistant:
  - `get:actors` Retreive all the actors
  - `get:movies` Retreive all the movies  
- Casting Director
  - `get:actors` Retreive all the actors
  - `post:actors` Add a new actor
  - `delete:actors` Delete an existing actor  
  - `get:movies` Retreive all the movies
  - `post:movies` Add a new movie
  - `delete:movies` Delete an existing movie
- Executive Producer
  - `get:actors` Retreive all the actors
  - `post:actors` Add a new actor
  - `delete:actors` Delete an existing actor
  - `patch:actors` Update the details of an existing actor  
  - `get:movies` Retreive all the movies
  - `post:movies` Add a new movie
  - `delete:movies` Delete an existing movie
  - `patch:movies` Update the details of an existing movie
  
### Endpoints
#### GET /actors
- General:
    - Fetches all the actors
- Permitted Roles:
    - Casting Assistant
    - Casting Director
    - Executive Producer

#### GET /movies
- General:
    - Fetches all the movies
- Required Role:
    - Casting Assistant
    - Casting Director
    - Executive Producer

#### POST /actors
- General:
    - Adds a new actor
- Permitted Roles:
    - Casting Director
    - Executive Producer    
- Required Body:  
    - `name`: Name of the actor  
    - `age`: Actor's age  
    - `gender`: Actor's gender
    
#### POST /movies
- General:
    - Adds a new movie
- Permitted Roles:
    - Casting Director
    - Executive Producer    
- Required Body:  
    - `title`: Movie's title  
    - `release_date`: Movie's date of release in one of the formats "DD/MM/YYYY" or "DD-MM-YYYY"

#### DELETE /actors/`{int:actor_id}`
- General:
    - Deletes the given actor, if exists
    
#### DELETE /movies/`{int:movie_id}`
- General:
    - Deletes the movie with the given id, if exists

#### PATCH /actors/`{int:actor_id}`
- General:
    - Updates the details of the actor having the given id
- Body(Atleast one required):  
    - `name`: Name of the actor  
    - `age`: Actor's age  
    - `gender`: Actor's gender

#### PATCH /actors/`{int:actor_id}`
- General:
    - Updates the details of the actor having the given id
- Body(Atleast one required):  
    - `title`: Movie's title  
    - `release_date`: Movie's date of release in one of the formats "DD/MM/YYYY" or "DD-MM-YYYY"
    
## Testing
To run the tests, run the command below and also remove the `requires_authentication` decorator in app.py 
```
python test_app.py
```
### Test using Postman
Import the Postman collection and run the tests to test the role based access control. You can also use the button below to run the tests directly  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b057daf38a223628f598)  
or else visit the link [Postman Link](https://www.getpostman.com/collections/b057daf38a223628f598)
