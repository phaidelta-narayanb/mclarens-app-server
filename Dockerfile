# Note: This is NOT a production-ready docker image.
# Please create your own Dockerfile along with your app and install
# this package as a dependency (`pip install <package-host-url>@1.0.0`)

FROM python:3.10.13-slim

ARG PACKAGE_INSTALL=.

# Use a non-root user
RUN ["useradd", "-u", "1001", "app"]
USER app

WORKDIR /app

# Copy project files
COPY . .

RUN ["python3", "-m", "pip", "install", "-U", "pip"]

# Install package
RUN ["python3", "-m", "pip", "install", "$PACKAGE_INSTALL"]

CMD ["start.sh"]
