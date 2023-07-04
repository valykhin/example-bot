export FLASK_DEBUG=true
export PROMETHEUS_CLIENT_HOST=http://94.131.109.165:9090
export CLIENT_API_URL=http://127.0.0.1:5001/api
export SERVER_STATUS_POLLING_ENABLE=""

pipenv run flask db migrate
pipenv run flask db upgrade
pipenv run flask --app app run

