#if [ -z "$BOT_TOKEN" ]; then BOT_TOKEN="5727252293:test"; fi
if [ -z "$VPN_BOT_TOKEN_FILE" ]; then VPN_BOT_TOKEN_FILE="../deploy/secrets/BOT_TOKEN" ; fi
if [ -z "$LOGGER_CONFIGURATION_FILE" ]; then LOGGER_CONFIGURATION_FILE="logging.conf" ; fi

if [ -z "$CORE_API_URL" ]; then CORE_API_URL="http://127.0.0.1:5000/api" ; fi
if [ -z "$PAYMENT_PROVIDER_TOKEN_FILE" ]; then PAYMENT_PROVIDER_TOKEN_FILE="../deploy/secrets/PAYMENT_PROVIDER_TOKEN" ; fi


#export BOT_TOKEN
export BOT_TOKEN_FILE
export LOGGER_CONFIGURATION_FILE
export CORE_API_URL
export PAYMENT_PROVIDER_TOKEN_FILE

pipenv run python app.py

