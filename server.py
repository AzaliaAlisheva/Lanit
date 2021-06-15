import fasttext
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from main import my_people

# App creation
app = FastAPI()


class User(BaseModel):
    interests: str
    movies: str
    books: str
    music: str


@app.post('/companions')
def find_companions(user: User):
    nearest = my_people(user.interests, "na")
    return nearest[["Все интересы"]].to_json()


@app.post('/female_companions')
def find_females(user: User):
    nearest = my_people(user.interests, "f")
    return nearest["Все интересы"].to_json()


@app.post('/male_companions')
def find_males(user: User):
    nearest = my_people(user.interests, "m")
    return nearest["Все интересы"].to_json()


@app.post('/movies')
def find_movies(user: User):
    nearest = my_people(user.interests, "na")
    return nearest["Фильмы"].to_json()


@app.post('/books')
def find_books(user: User):
    nearest = my_people(user.interests, "na")
    return nearest["Книги"].to_json()


@app.post('/music')
def find_music(user: User):
    nearest = my_people(user.interests, "na")
    return nearest["Музыка"].to_json()


if __name__ == '__main__':
    # Run server using given host and port
    uvicorn.run(app, host='127.0.0.1', port=80)
