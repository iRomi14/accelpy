FROM accelize/base:ubuntu_bionic-aws_f1
SHELL ["/bin/bash", "-c"]

EXPOSE 8080

USER root

RUN apt-get update && \
apt-get install -y --no-install-recommends \
    apt-transport-https \
    software-properties-common \
    lsb-release \
    gnupg \
    curl \
    python3 && \
curl -fsSL https://accelize.s3.amazonaws.com/gpg | apt-key add - && \
add-apt-repository "deb https://accelize.s3.amazonaws.com/deb $(lsb_release -cs) stable" && \
apt update && \
apt-get install -y --no-install-recommends \
    python3-accelize-drm && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
COPY app_server.py .
USER appuser
CMD ["./app_server.py"]
