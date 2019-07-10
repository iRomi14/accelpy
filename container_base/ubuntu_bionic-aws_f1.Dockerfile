FROM ubuntu:bionic AS build
SHELL ["/bin/bash", "-c"]

# Install AWS F1 runtimes from sources (No package availables)
RUN apt-get update && \
apt-get install -y --no-install-recommends \
    ca-certificates \
    gcc \
    git \
    libc-dev \
    make \
    python3 \
    sudo && \
git clone https://github.com/aws/aws-fpga /tmp/aws-fpga --depth 1 && \
source /tmp/aws-fpga/sdk_setup.sh && \
rm -Rf /tmp/aws-fpga && \
apt-get remove -y --purge \
    gcc \
    git \
    libc-dev \
    make && \
apt-get clean && \
apt-get autoremove -y --purge && \
rm -rf /var/lib/apt/lists/*

# Copy built AWS F1 runtime libraries on a fresh Ubuntu image
FROM ubuntu:bionic
SHELL ["/bin/bash", "-c"]
COPY --from=build /usr/local/lib /usr/local/lib

# Create a new unpriviliged user to run the application
# UID and GID are kept the same as the unprivileged user on host.
RUN groupadd -g 1001 fpgauser && \
useradd -mNs /bin/bash -u 1001 -g fpgauser appuser
USER appuser
WORKDIR /home/appuser
