FROM python:3.8
LABEL maintainer="delphai/devops"
WORKDIR /app
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa

# Install Terraform
RUN apt-get install unzip
RUN wget https://releases.hashicorp.com/terraform/0.13.3/terraform_0.13.3_linux_amd64.zip
RUN unzip terraform_0.13.3_linux_amd64.zip
RUN mv terraform /usr/local/bin/

RUN pip install pipenv
ENV PIPENV_VENV_IN_PROJECT=true 
COPY Pipfile Pipfile.lock  /app/
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python", "/app/src/server.py"]