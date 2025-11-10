FROM python:3.13-slim

WORKDIR /app
COPY . /app

# Install this package (editable) and dev tools for tests
RUN pip install --no-cache-dir -r dev-requirements.txt

# Default command runs tests; override in downstream usage as needed
CMD ["pytest", "-q"]
