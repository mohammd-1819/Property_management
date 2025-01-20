FROM python:3.11
WORKDIR /Property_management
COPY requirements.txt /Property_management/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . /Property_management/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Property_management.wsgi:application"]
