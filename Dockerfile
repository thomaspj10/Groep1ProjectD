FROM python:3.9-slim

RUN apt-get update && apt-get -y install tk tcl
RUN pip install --upgrade cython
RUN pip install --upgrade pip

RUN mkdir -p /user/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1 
EXPOSE 8501

COPY . . 

# ENTRYPOINT [ "streamlit", "run" ]
# CMD [ "main.py" ]