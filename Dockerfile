FROM python:3.12

# Install dependencies
WORKDIR /code
RUN apt-get update && \
    apt-get -y install libgl1-mesa-glx libglib2.0-0

# Install python requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy repo
COPY src src

# Run container
EXPOSE 80
CMD ["python", "-m", "uvicorn", "src.main:app", "--port", "80", "--host", "0.0.0.0"]
