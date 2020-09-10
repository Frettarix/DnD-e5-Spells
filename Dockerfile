FROM python:3.9-rc-buster

# Installing requiriments
RUN pip install python-telegram-bot --upgrade
RUN pip install requests

WORKDIR /usr/src/dnd_spells
COPY resources/class_icons.json common.py bot.py dnd_spells.py setup.py .cached-spells ./

CMD [ "python", "/usr/src/dnd_spells/bot.py" ]
