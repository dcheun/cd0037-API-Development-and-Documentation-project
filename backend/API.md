## API Reference

---

### Getting Started
- Base URL: This app can be run and hosted locally. By default, it will be listening on `http://127.0.0.1:5000`.
- Authentication: This version of the API does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```
There are `5` error types that can be returned from the API, including:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

### Endpoints
#### GET /questions
- General:
  - Retrieves a list of questions.
  - Query Parameters:
    - `page` (int) - Results are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `questions` - List of question objects, paginated.
    - `current_category` - If provided, the category of the `questions` list.
    - `categories` - List of all categories.
    - `total_questions` - The number of total questions.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
```json
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

#### POST /questions
- General:
  - Creates a new question using the supplied fields.
  - Request Body:
    - `question` (str) - The text of the question.
    - `answer` (str) - The text of the answer.
    - `difficulty` (int) - The difficulty level.
    - `category` (int) - The category id.
  - Query Parameters:
    - `page` (int) - `questions` results list is paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `created_id` - id of the created question.
    - `questions` - List of question objects based on current page number to update the frontend.
    - `total_questions` - The number of total questions.
- Sample: `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", "answer": "Maya Angelou",
    "difficulty": 2, "category": 4 }'`
```json
{
    "created_id": 33,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 33,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

#### POST /questions (Search)
- General:
  - If a `searchTerm` field is provided in the body, this will run a serach on the `question` field of the resource and return a list of results.
  - Request Body:
    - `searchTerm` (str) - The search string.
  - Returns:
    - `success` - The success value.
    - `questions` - List of question objects matching the search term.
    - `current_category` - If provided, the category of the search.
    - `total_questions` - The number of total questions.
- Sample: `curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{
    "searchTerm": "soccer" }'`
```json
{
    "current_category": null,
    "questions": [
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

#### DELETE /questions/<question_id>
- General:
  - Deletes the question of the given ID if it exists.
  - Query Parameters:
    - `page` (int) - A list of question objects are returned and are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `deleted_id` - id of the deleted resource.
    - `questions` - List of questions objects based on the current page number to update the frontend.
    - `total_questions` - The number of total questions.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/40?page=3`
```json
{
    "deleted_id": 40,
    "questions": [
        {
            "answer": "August 3, 1776",
            "category": 4,
            "difficulty": 4,
            "id": 39,
            "question": "When was the Declaration of Independence signed?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

#### GET /categories
- General:
  - Retrieves a list of all category objects.
  - Returns:
    - `success` - The success value.
    - `categories` - List of category objects.
    - `total_categories` The number of total categories.
- Sample: `curl http://127.0.0.1:5000/categories`
```json
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        {
            "id": 2,
            "type": "Art"
        },
        {
            "id": 3,
            "type": "Geography"
        },
        {
            "id": 4,
            "type": "History"
        },
        {
            "id": 5,
            "type": "Entertainment"
        },
        {
            "id": 6,
            "type": "Sports"
        }
    ],
    "success": true,
    "total_categories": 6
}
```

#### GET /categories/<category_id>/questions
- General:
  - Retrieves a list of all question objects by category.
  - Query Parameters:
    - `page` (int) - Results are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `questions` - List of questions in the category specified.
    - `total_questions` - The number of total questions.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions?page=1`
```json
{
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
    "total_questions": 21
}
```

#### POST /quizzes
- General:
  - Retrieves a random question for the quiz by the following supplied fields.
  - Request body:
    - `previous_questions` - A list of all the previous questions seen, to be excluded for the next question returned.
    - `previous_category` (optional) - The category of the next question.
  - Returns:
    - `question` - The next question object.
    - `success` - The success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{
    "previous_questions": [20], "previous_category": 1 }'`
```json
{
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true
}
```
