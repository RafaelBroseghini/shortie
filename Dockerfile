FROM python:3.9

WORKDIR /src
COPY . /src

RUN pip install pipenv
RUN pip install pipenv && pipenv install --dev --system --deploy

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]