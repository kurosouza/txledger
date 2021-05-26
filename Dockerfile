FROM python:3.8.3-slim-buster
WORKDIR /app
RUN mkdir /app/__tests__
COPY requirements.txt fileloader.py ledger.py cli.py transactions.csv /app/
COPY __tests__ /app/__tests__
RUN pip install -r requirements.txt
CMD ["pytest","-v"]