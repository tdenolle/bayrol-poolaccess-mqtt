ARG BUILD_FROM
FROM $BUILD_FROM
# Copy toml file
COPY pyproject.toml /
# Copy requirements.txt file
COPY requirements.txt /
# Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Working dir setup
WORKDIR /data
## Copy app
COPY /app /app/
## Default entrypoint
COPY Docker.entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh
# Run app
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
