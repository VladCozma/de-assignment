FROM python:3.9.12-slim-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-dev musl-dev libpq-dev gcc

RUN mkdir -p /cdm/lib
COPY lib /cdm/lib/
COPY requirements.txt /cdm/

WORKDIR /cdm
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENV PYTHONPATH="/cdm/lib/src:/cdm/lib/tests:$PYTHONPATH"
CMD ["python3", "lib/src/main.py"]
