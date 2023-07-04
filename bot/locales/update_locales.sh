#!/bin/bash

if [ ${PWD##*/} = "locales" ];
then
	function compile {
		cd './'$1'/LC_MESSAGES/'
		msgmerge --update --backup=none bot.po ../../bot.pot
		msgfmt bot.po -o bot.mo
		cd ../../
	};
else
	echo 'Only execute this in the "locales" directory'
	exit 1;
fi

xgettext ../*.py -o ./bot.pot -d bot --foreign-user \
  --package-name="bot" \
  --package-version="$currentVer" \
  --msgid-bugs-address='ivalykhin@gmail.com' \
  --keyword=__ \
  --keyword=_:1,2 \
  --keyword=__:1,2
compile en
compile ru