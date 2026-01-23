TODO:
Create a simple flask-based TO-DO app. It should use a sqlite database to store the tasks and their status (unchecked || checked)
The app should allow the user to create and delete tasks.
After completion of the initial setup, the app should be containerized and the image pushed to dockerhub.

To deploy the heml chart
heml package py-todo-chart
help install py-todo-app ./py-todo-chart-0.1.0.tgz 
https://hub.docker.com/r/chas3bg/flask-todo
