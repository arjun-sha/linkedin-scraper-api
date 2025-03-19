FROM python:3.10-slim
ENV PYTHONPATH .

RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libxcomposite1 libxrandr2 libxdamage1 libxkbcommon0 libpango1.0-0 \
    libgbm1 libasound2 libwayland-client0 libwayland-server0 libgtk-3-0 \
    xvfb && \
    rm -rf /var/lib/apt/lists/*

# Setting Up the Display server Port
ENV DISPLAY=:99

# Installing Curl-CFFI dependencies
RUN apt-get update && apt-get install -y libnss3 nss-plugin-pem ca-certificates

# Installing requirements
ADD requirements.txt /
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copying necessary files
RUN mkdir /code
ADD . /code/
WORKDIR /code

ENTRYPOINT [ "sh", "start_server.sh" ]
EXPOSE 5000
