FROM python:slim

RUN pip3 install https://github.com/Upsolver/cli/releases/download/v0.1.7/upsolver-cli.tar.gz

COPY cliconfig /config
COPY entrypoint.sh /entrypoint.sh
COPY executeworksheet.py /executeworksheet.py

RUN chmod +x /entrypoint.sh
RUN chmod +x /executeworksheet.py

ENTRYPOINT ["/entrypoint.sh"]
