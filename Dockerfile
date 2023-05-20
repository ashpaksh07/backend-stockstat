FROM python:3.10

RUN pip install fastapi uvicorn

EXPOSE 8000

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]