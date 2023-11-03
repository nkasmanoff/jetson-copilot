FROM ghcr.io/pytorch/pytorch-nightly:c69b6e5-cu11.8.0
# install apt-get

#RUN apt-get update && apt-get -y install python3-pip --fix-missing

# Set the working directory in the container to /app
WORKDIR /app


COPY models ./models

COPY requirements.txt ./requirements.txt

COPY .env ./.env

COPY __init__.py ./__init__.py

COPY app.py ./app.py

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start uvcorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# To build and run this container
# sudo docker build -t jetpilot-app .
# sudo docker run -p 8000:8000 jetpilot-app

# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
