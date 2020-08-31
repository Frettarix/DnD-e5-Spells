FROM python:3.9-rc-buster

# Installing requiriments
RUN pip install python-telegram-bot --upgrade
RUN pip install git+https://gitlab.com/obuilds/public/pytube
RUN pip install validator-collection

WORKDIR /usr/src/dnd_spells
COPY . .

CMD [ "python", "/usr/src/dnd_spells/bot.py" ]