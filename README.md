# Casting Agency API

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

## Database Setup

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` find the application. 


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`. 
- Authentication: This version of the application requires the user to have the appropriate permissions to access the endpoints. It uses the Auth0 sign in for authentication. The app verifies that the user has the required permissions using the JWT.
  - Add the appropriate JWT as a `Bearer` token to the `Authorization` segment of the `Header`
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
#### GET /categories
- General:
    - Fetches a dictionary of all available categories with the category id as its key and the category name as value
- Request Parameters:
    - None    
- Sample: `curl http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET /questions
- General:
    - Fetches a paginated dictionary of questions of all available categories
    - Results are paginated in groups of 10
 - Request Parameters(Optional): 
	- `page=<int:page_number>`     
- Sample: `curl http://127.0.0.1:5000/questions?page=2`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
#### POST /questions
- General:
    - Adds a new question to the database if a new book is provided as JSON and returns the book id
    - Searches questions for a keyword and returns results if `searchTerm` is provided as JSON and returns the search results
- Request Body (Adding a new question):  
    - `question`: Question statement  
    - `answer`: Answer statement  
    - `category`: Category ID  
    - `difficulty`: Difficulty Level
    
- Sample: `curl http://127.0.0.1:5000/questions -X POST -d '{question: "Is the new question added?", answer: "Yes", difficulty: 1, category: "5"}'`
        
``` 
{
"success": True,
"created": 20
}
```

   - Request Body (For searching questions):
        `searchTerm`: The keyword to be searched in the questions
        
   - Sample: `curl http://127.0.0.1:5000/questions -X POST -d '{searchTerm: "new question"}'`
        
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Yes", 
      "category": 5, 
      "difficulty": 1, 
      "id": 20, 
      "question": "Is the new question added?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

#### DELETE /questions/`{int:question_id}`
- General:
    - Deletes the question from the database
- Request Parameters: 
	- None     
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/20`

```
{
  "deleted": "20", 
  "success": true
}
```

#### GET /categories/`{int:category_id}`/questions
- General:
    - Fetches a dictionary of questions for the specified category
- Request Parameters: 
	- None     
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```

#### POST /quizzes
- General:
    - Fetches one random question within a specified category. Previously asked questions are not asked again.
- Request Body: 
	- `previous_questions`: Array of questions previously asked
	- `quiz_category`: Dictionary containing category_id:category_type     
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -d '{previous_questions: [18], quiz_category: {type: "Science", id: "1"}}'`

```
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 16, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}

```

## Testing
To run the tests, run
```
python test_app.py
```
You can also import the Postman collection and run the tests
