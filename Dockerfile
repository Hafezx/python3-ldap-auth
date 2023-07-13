# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-buster

EXPOSE 8080

RUN pip install gunicorn

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .

ARG CI_PY_REPO_USER
ARG CI_PY_REPO_PASS

# RUN apt-get update && apt-get install -y python3-venv build-essential python3-dev

RUN python -m pip install -r requirements.txt 


WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "server:app"]
