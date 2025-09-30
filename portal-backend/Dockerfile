FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y wget gnupg lsb-release \
    && echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O /usr/share/keyrings/postgresql-archive-keyring.gpg https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    && apt-get update \
    && apt-get install -y postgresql-client-15 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose Flask port
EXPOSE 5001

# Run Flask app
CMD ["python", "app.py"]