FROM python:3.7-bullseye

COPY ./requirements.txt /api/requirements.txt

WORKDIR /api

RUN pip install -r requirements.txt

COPY ./app /api/app

COPY ./private.pem /api/private.pem
COPY ./public.pem /api/public.pem
COPY ./.env /api/.env

# CMD ["uvicorn", "app:main:app", "--host", "0.0.0.0", "--port", "3000"]
# CMD ['tail', '-f', '/dev/null']