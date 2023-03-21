FROM python

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app /app

COPY ./private.pem /app/private.pem
COPY ./public.pem /app/public.pem

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]