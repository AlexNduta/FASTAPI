from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import json
app = FastAPI()


# our temporary storage space for our data
my_post = [{"title": "title of post1", "content": "content of post1", "id":1}, {"title":"Favourite food", "content":"I just love food", "id": 2}]

filename = "stoarge.txt"
@app.get("/posts")

def root():
    """get method to get all the data fom our storage space"""
    return my_post



class Post(BaseModel):
#    Used to validate posted data
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None

# POST Request
@app.post("/posts")
def create_post(new_post : Post):
    """ creates a post and sends it to the remote server using a URL provided and later auto-generates an ID
    """
# post data to the Array created
    new_dict = new_post.dict() #  convert our post to a python dictionary
    new_dict['id'] = randrange(0, 120000) # generate a random ID in the range 0 -120000

    my_post.append(new_dict) # append the data sent and converted to the dictionary
    return {"data": new_dict} # send back data saved

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    """ gets a specifi item in a list using its ID"""
    # print(type(id))
    found_post = find_post(int(id))
    #check if the post exist and send a status code
    if not found_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "item with id:{} is not found".format(id))
    return found_post

def find_post(id):
    """ gets a specific post with the iD passed """
    for p in my_post: 
        if p['id'] == id:
            return p
