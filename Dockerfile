FROM python:3.8
COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]