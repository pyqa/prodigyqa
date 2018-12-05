FROM ubuntu

# Step 2
# Essential tools and xvfb
RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb \
    wget \
    libfontconfig \
    gnupg \
    --no-install-recommends apt-utils \
    python-pip \
    default-jre-headless \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    net-tools \
    default-jre \
    default-jdk \
    zip \
    unzip \
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    python-dev \
    git-core

# Install Chrome / Puppeteer dependencies
# https://github.com/GoogleChrome/puppeteer/issues/404#issuecomment-323555784
RUN apt-get install -y libpangocairo-1.0-0 libx11-xcb1 libxcomposite1 libxdamage1 libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 libgconf2-4 libasound2 libatk1.0-0 libgtk-3-0

# Step 3 - Setup Browsers
# Install PhantomJS
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 
RUN tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/ 
RUN ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin 

# Install Selenium driver dependency: Chrome
RUN echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list &&\
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
apt-get update &&\
apt-get -y install google-chrome-stable

# Install Selenium Chromedriver
RUN apt-get -y install unzip &&\
wget -q https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip &&\
unzip chromedriver_linux64.zip &&\
mv chromedriver /usr/bin/chromedriver &&\
chown root:root /usr/bin/chromedriver &&\
chmod +x /usr/bin/chromedriver &&\
rm chromedriver_linux64.zip

# Install selenium
RUN pip install selenium

# Install Selenium-based test automation dependences
RUN pip install setuptools 
RUN pip install pytest allure-pytest pytest-html

# Install load test dependencies
RUN apt-get install -y  
RUN pip install bzt

# Install eslint, etc
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g eslint eslint-plugin-html eslint-plugin-template stylelint stylelint-config-recommended jscpd eclint bower yarn
# Install htmllint-cli from github. npm has htmllint-cli@0.0.6 which uses htmllint@0.6.0 which does not support raw-ignore-regex
RUN git clone https://github.com/htmllint/htmllint-cli.git
RUN cd htmllint-cli && npm link && cd /
