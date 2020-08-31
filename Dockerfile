FROM python:3.9-rc-buster

# Installing requiriments
RUN pip install python-telegram-bot --upgrade
RUN pip install git+https://gitlab.com/obuilds/public/pytube
RUN pip install validator-collection

WORKDIR /usr/src/dnd_spells
COPY common.py .
COPY bot.py .
COPY dnd_spells.py .
COPY setup.py .
COPY .cached-spells .

CMD [ "python", "/usr/src/dnd_spells/bot.py" ]
