FROM python:3.9.1-alpine
RUN apk update
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN mkdir -p /user/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1 
EXPOSE 8501 80
COPY . . 
CMD ["streamlit", "run", "main.py"]