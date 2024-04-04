# reken-fullstack-demo
See Reken in action with our dynamic demo CRUD web application. Master GET, POST, DELETE, PUT REST calls with Python Flask REST service. Efficiently manage SQLite database tasks—fetch, create, delete, update rows. Enhance UI with Tailwind styling. Ideal for developers aiming to use Reken for effective web app development.

## Run instructions
Clone repo to local environment.
```bash
# Start a terminal
git clone https://github.com/hbroek/reken-fullstack-demo.git
cd reken-fullstack-demo
```

Make sure you have python3 and pip installed. Then install the following packages:
```bash
#In terminal
pip install flask
pip install db-sqlite3 # if you don't have sqlite installed, typically shipped with python3
pip install flask-cors #only when using cors. REST API and Web App need to run on different domain/port. Not applicable for instructions below.
```

After packages are installed, go to the src
```bash
cd src
python3 rest_employees.py # Start the Flask server and the web server and REST end points
```

Start your browser and type in the following url:
http://127.0.0.1:5000/
This opens the Tailwind styled employees Web App.

http://127.0.0.1:5000/bare
To open the unstyled employees Web App. Enter this url: http://127.0.0.1:5000/bare

More information about this project check out this [blog post](https://blog.henryvandenbroek.com/reken-powered-full-stack-web-app-with-sqlite-python-flask-tailwind/) source, see this blog post.

Any comments, or questions send me an email at hbroek (at) gmail.com

More resources:
- https://reken.dev