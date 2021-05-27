FROM python:3.7.10-stretch

RUN apt-get update && apt-get install -yq \
    git-core \
    unzip \
    xclip \
    libnss3-dev

# GeckoDriver v0.29.1
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz" -O /tmp/geckodriver.tgz \
    && tar zxf /tmp/geckodriver.tgz -C /usr/bin/ \
    && rm /tmp/geckodriver.tgz

# chromeDriver v91.0.4472.19
RUN wget -q "https://chromedriver.storage.googleapis.com/91.0.4472.19/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip

# create symlinks to chromedriver and geckodriver (to the PATH)
RUN ln -s /usr/bin/geckodriver /usr/bin/chromium-browser \
    && chmod 777 /usr/bin/geckodriver \
    && chmod 777 /usr/bin/chromium-browser

RUN mkdir -p /src
