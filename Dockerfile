FROM python:3.8
COPY /src /src
ENTRYPOINT ["/code/entrypoint.sh"]