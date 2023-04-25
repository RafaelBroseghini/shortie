FROM python:3.11

WORKDIR /src
COPY . /src

RUN pip install pip-tools && pip-sync

EXPOSE 8000

RUN chmod +x start-server.sh

CMD ["./start-server.sh"]