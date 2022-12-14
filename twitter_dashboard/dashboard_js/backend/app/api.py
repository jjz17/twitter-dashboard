from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from twitter_dashboard.personal_twitter_data import TweetLoader
from twitter_dashboard.mongo_data import MongoStore


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

loader = TweetLoader()
store = MongoStore("twitter_dashboard_db", "home_timeline")

todos = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    },
    {
        "id": "3",
        "item": "Increase in Faith, Hope, and Charity."
    }
]

# Example using path parameters (required)
# @app.get("/load-tweets/{n_tweets}", tags=["tweets"])
# async def get_tweets(n_tweets: int) -> dict:
#     return loader.extract_tweets(count=n_tweets)


# Example using query parameters (not required)
@app.get("/load-tweets", tags=["tweets"])
async def get_tweets(n_tweets: int = 5) -> list:
    loader.extract_tweets(count=n_tweets)
    return loader.get_loaded_tweets_as_json()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return { "data": todos }


@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    # Check if todo to add is a duplicate
    if todo in todos:
        return {
            "data": { "Error: duplicate Todo" }
        }
    todos.append(todo)
    return {
        "data": { "Todo added." }
    }


@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }


@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: int) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todos.remove(todo)
            return {
                "data": f"Todo with id {id} has been removed."
            }

    return {
        "data": f"Todo with id {id} not found."
    }