# create fast api app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.codecomplete import CodeCompletionModel
import requests

base_url = 'http://localhost:8000'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)

code_model = CodeCompletionModel(model_name='bigcode/starcoderbase-1b')


@app.get("/")
def read_root():
    return {"message": "Welcome to the tools api on FASTAPI"}


@app.get("/codecomplete/{input_string}")
def complete(input_string):
    return {'response': code_model.complete(input_string)}


# example curl command

# curl -X GET "http://localhost:8000/codecomplete/def%20add%28a%2C%20b%29%3A%0A%20%20%20%20return%20a%20%2B%20b%0A%0Aprint%28add%281%2C%202%29%29%0A" -H  "accept: application/json"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
