FROM python:3.10.13-alpine

RUN apt-get update && apt-get -y install python3-pip --fix-missing

# Set the working directory in the container to /app
WORKDIR /app

COPY models ./models

COPY requirements.txt ./requirements.txt

COPY __init__.py ./__init__.py

COPY app.py ./app.py

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start uvcorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# To build and run this container
# docker build -t fastapi-app .
# docker run -d -p 8000:8000 fastapi-app

