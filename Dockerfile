FROM python:3.13.1-alpine
WORKDIR /todo_app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./todo_app/* ./
ADD ./todo_app/templates/ /todo_app/templates/
EXPOSE 5000
CMD ["flask", "--app", "__init__.py", "run", "--host", "0.0.0.0"]