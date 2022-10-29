FROM python:3.9

COPY ./task/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./task /code/app

WORKDIR /code/app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["pytest"]

