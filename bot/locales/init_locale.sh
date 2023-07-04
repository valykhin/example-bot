LOCALE_NAME='en'
LOCALE_DIR="${LOCALE_NAME}/LC_MESSAGES"
mkdir -p "${LOCALE_DIR}"
msginit --no-translator --input=bot.pot --locale="${LOCALE_NAME}"
mv "${LOCALE_NAME}.po" "${LOCALE_DIR}/bot.po"