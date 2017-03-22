FROM python:3.6-alpine
COPY . /srv/save-image
RUN pip install -r /srv/save-image/src/requirements.txt
ENTRYPOINT ["/srv/save-image/src/save-image.py", "--loop"]
CMD ["http://agile.ro/urad"]
