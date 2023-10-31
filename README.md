# Jetson Copilot

This repo contains the work to train (in a jupyter notebook) and deploy a small coding assistant LLM, which can be used to autocomplete code in a text editor. The model is trained on a small dataset of python code, and is deployed on a Jetson Nano.


## Rant / What I need to figure out

Model is fine-tuned and lives on HF. Am struggling a bit with loading the Docker container on my nano 2gb. I'm not sure what the proper base environment should be, I need something which enables cuda, allows for the latest versions of accelerate and transformers, and doesn't eat up the remaining disk space on the Jetson so I have room for the model and quantized model. 

Still researching this and will update this readme when I figure it out.