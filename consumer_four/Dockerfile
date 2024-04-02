FROM python

WORKDIR /app
COPY ./consumer_four .
RUN pip install -r requirements.txt

CMD [ "python", "order_processing.py" ]
