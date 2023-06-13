FROM python:3.8-slim-bullseye

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./api ./api
COPY ./model ./model

CMD ["uvicorn", "api.api:app", "--host=0.0.0.0", "--port=80"]