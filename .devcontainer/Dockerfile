FROM ubuntu:24.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set locale
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Create vscode user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Essential build tools
    build-essential \
    curl \
    wget \
    git \
    gnupg \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    lsb-release \
    # Python build dependencies
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    tk-dev \
    uuid-dev \
    zlib1g-dev \
    # Additional tools
    unzip \
    zip \
    tree \
    jq \
    vim \
    nano \
    htop \
    # For Temporal/Docker services
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12 (Ubuntu 24.04 has Python 3.12 by default)
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Make python3.12 the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Install Bazelisk (manages Bazel versions)
RUN curl -fsSL https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64 \
    -o /usr/local/bin/bazel \
    && chmod +x /usr/local/bin/bazel

# Install Buildifier (Bazel formatter)
RUN curl -fsSL https://github.com/bazelbuild/buildtools/releases/latest/download/buildifier-linux-amd64 \
    -o /usr/local/bin/buildifier \
    && chmod +x /usr/local/bin/buildifier

# Install pre-commit
RUN pip3 install pre-commit

# Create non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Install UV for the vscode user as well
USER $USERNAME
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/$USERNAME/.cargo/bin:$PATH"

# Set up workspace directory
WORKDIR /workspaces/the-company-os

# Configure git safe directory (needed for dev containers)
RUN git config --global --add safe.directory /workspaces/the-company-os

# Set environment variables for development
ENV PYTHONPATH=/workspaces/the-company-os
ENV UV_CACHE_DIR=/workspaces/the-company-os/.uv-cache
ENV BAZEL_CACHE_DIR=/home/$USERNAME/.cache/bazel

# Create cache directories with proper permissions
RUN mkdir -p /home/$USERNAME/.cache/bazel \
    && mkdir -p /workspaces/the-company-os/.uv-cache \
    && chown -R $USERNAME:$USERNAME /home/$USERNAME/.cache

# Default command
CMD ["/bin/bash"]
