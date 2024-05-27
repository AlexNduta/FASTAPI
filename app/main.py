from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine

app = FastAPI()


# our temporary storage space for our data
my_post = [{"title": "title of post1", "content": "content of post1", "id":1}, {"title":"Favourite food", "content":"I just love food", "id": 2}]

# run continously until we get a connection then break
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database= 'fastapi',user= 'wong', password= '123', cursor_factory=RealDictCursor)
        cursor = conn.cursor() 
        print("connetion to the database succefull!")
        break
    # if we fail, the loop will repeat
    except Exception as error:
        print("Failed to conect to the DB")
        print("ERROR:", error)

    
filename = "stoarge.txt"
@app.get("/posts")

def root():
    """get method to get all the data fom our storage space"""
    cursor.execute(""" SELECT * FROM posts""")
    post = cursor.fetchall()
    print(post)
    return post



class Post(BaseModel):
#    Used to validate posted data
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None

# POST Request
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post : Post):
    """ creates a post and sends it to the remote server using a URL provided and later auto-generates an ID
    """
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    new_db_post= cursor.fetchone()
    conn.commit()

    return {"data": new_db_post} 

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    """ gets a specifi item in a list using its ID"""

    cursor.execute(""" SELECT * FROM posts WHERE id= %s""", (str(id)))
    found_post = cursor.fetchone()
    
    #check if the post exist and send a status code
    if not found_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "item with id:{} is not found".format(id))
    return {"post_detail": found_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_item(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", str(id))
    deleted_posts = cursor.fetchone()
    conn.commit()
    return {"message" : "Post successfully deleted"}

    if deleted_posts is None:
        raise HTTPException(status_cod=status.HTTP_404_NOT_FOUND, detail= "Post with id:{} not found".format(id))

@app.put("/posts/{id}")
def update_post(id:int, new_post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s returning *""", (new_post.title, new_post.content, new_post.published, str(id)))
    update_post= cursor.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id {} does not exist".format(id))
    return{"data": update_post}
