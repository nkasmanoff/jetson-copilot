# create fast api app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.codecomplete import CodeCompletionModel


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


@app.post("/")
async def request_completion(request: VisualStudioCodeCompletionRequest):
    """
    Creates a completion for a given prompt.

    Adapted from https://github.com/pacman100/mlc-llm/blob/main/python/mlc_chat/rest.py#L214C1-L214C74, 
    this is what you'd need to run an API which returns LLM generated text.
    """
    prompt = request.inputs
    if len(prompt.split(" ")) > 6000:
        diff_len = len(prompt.split(" ")) - 6000
        prompt_suffix = prompt.split("<fim_siffix>")[1].split(" ")
        prompt_suffix = """<fim_suffix>""" if len(
            prompt_suffix)-(diff_len) < 0 else " ".join(prompt_suffix[:len(prompt_suffix)-(diff_len)])
        prompt_prefix = prompt.split("<fim_siffix>")[0].split(" ")
        prompt = prompt_prefix+prompt_suffix+"<fim_middle>"

    print(prompt)

    msg = code_model.generate(prompt)

    print(msg)
    # TODO: filter out prompt from returned message?
    return {"generated_text": msg}


@app.get("/codecomplete/{input_string}")
def complete(input_string):
    return {'response': code_model.complete(input_string)}


@app.get("/codecomplete/docstring/{input_string}")
def complete_docstring(input_string):
    return {'response': code_model.complete_docstring(input_string)}


# example curl command

# curl -X GET "http://localhost:8000/codecomplete/def%20add%28a%2C%20b%29%3A%0A%20%20%20%20return%20a%20%2B%20b%0A%0Aprint%28add%281%2C%202%29%29%0A" -H  "accept: application/json"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, reload=True)
