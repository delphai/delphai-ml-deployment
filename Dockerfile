FROM delphairegistry/ml-deploymnet:latest

LABEL maintainer="delphai/devops"
COPY . /app
ENTRYPOINT ["python", "/app/src/server.py"]