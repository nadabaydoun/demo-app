FROM python:3.9

RUN set -ex && mkdir /generator
WORKDIR /generator

COPY requirments.txt ./requirments.txt
RUN pip install -r requirments.txt

COPY templates/ ./templates
COPY . ./


ENV PYTHONPATH /generator
CMD python3 /generator/project.py