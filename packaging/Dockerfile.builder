FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV WINEDEBUG=-all
ENV WINEPREFIX=/root/.wine

RUN apt-get update && apt-get install -y \
    wine \
    wine64 \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Initialize wine prefix
RUN wineboot --init || true

# Setup Windows Python 3.11.9 64-bit
WORKDIR /opt/winpython
RUN curl -sSL https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip -o py.zip && \
    unzip -q py.zip && \
    rm py.zip

# Enable site-packages in embeddable python
RUN sed -i 's/#import site/import site/' python311._pth

# Install pip
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    wine python.exe get-pip.py --no-warn-script-location && \
    rm get-pip.py

# Install PyInstaller and dependencies
RUN wine Scripts/pip.exe install --no-warn-script-location \
    pyinstaller \
    fastapi==0.141.1 \
    uvicorn==0.52.4 \
    pydantic==2.13.5 \
    pydantic-settings==2.15.0 \
    pyyaml==6.0.3 \
    websockets==17.1 \
    httpx==0.28.1 \
    starlette==1.6.0

WORKDIR /workspace
