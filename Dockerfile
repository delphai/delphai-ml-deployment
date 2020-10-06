FROM python:3.8
ARG ssh
LABEL maintainer="delphai/devops"
WORKDIR /app
RUN pip install pipenv
ENV PIPENV_VENV_IN_PROJECT=true 
COPY Pipfile Pipfile.lock  /app/
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

# RUN echo "${ssh}" > /app/id_rsa.pub
# RUN cat /app/id_rsa.pub
# RUN ssh-keygen -f /app/id_rsa.pub -m 'PEM' -e > /app/public.pem
# RUN rm -f /app/id_rsa.pub
COPY . /app

ENTRYPOINT ["python", "/app/src/server.py"]