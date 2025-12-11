FROM python:3.12-slim

EXPOSE 8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl nano \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY bin ./bin/
RUN ["chmod", "+x", "bin/entrypoint.sh"]

COPY app /code/
COPY run.py /code/
COPY .env.example ./
RUN if [ ! -f .env ]; then cp .env.example .env; fi

CMD ["bin/entrypoint.sh"]
