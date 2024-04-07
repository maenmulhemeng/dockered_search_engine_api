# syntax=docker/dockerfile:1

FROM python:alpine as builder

WORKDIR /search_engine

COPY requirements.txt requirements.txt
RUN python -m venv .venv && .venv/bin/pip3 install -r requirements.txt


ENV FLASK_ENV=development


FROM python:alpine as runner
WORKDIR /search_engine
ENV PATH="/search_engine/.venv/bin:$PATH"
COPY --from=builder /search_engine/.venv /search_engine/.venv
COPY . .
EXPOSE 5000

CMD [ "flask","--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]

FROM python:alpine as db_initalizer
WORKDIR /search_engine
ENV PATH="/search_engine/.venv/bin:$PATH"
COPY --from=builder /search_engine/.venv /search_engine/.venv
COPY . .

CMD ["flask","--app","flaskr", "init-db"]
