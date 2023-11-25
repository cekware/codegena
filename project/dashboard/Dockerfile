FROM python:3.10-alpine

RUN pip install rq-dashboard

# https://github.com/rq/rq/issues/1469
RUN pip uninstall -y click
RUN pip uninstall -y black
RUN pip install click
RUN pip install black
EXPOSE 9181

CMD ["rq-dashboard"]
