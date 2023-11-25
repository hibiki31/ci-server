FROM ubuntu:22.04

RUN apt update 

# Install dev tools
RUN apt install -y \
    git jq iproute2 htop vim \
    unzip zip wget net-tools openssh-client \
    rsync curl

# Install application package
RUN apt install -y \
    python3 python3-pip 

COPY ../requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

WORKDIR /app

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000