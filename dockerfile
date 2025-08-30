FROM python:3.11-slim

WORKDIR /app
COPY kraken_dca.py /app/kraken_dca.py
RUN pip install schedule requests pytz

CMD ["python", "-u", "kraken_dca.py"]
