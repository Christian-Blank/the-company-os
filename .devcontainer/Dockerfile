################################################################################
# --- Stage 0: base system ----------------------------------------------------#
################################################################################
ARG TARGETPLATFORM
FROM ubuntu:24.04 AS base

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set locale
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install system dependencies and pipx
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    # Python and pipx
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    pipx \
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
    sudo \
    # For Temporal/Docker services
    postgresql-client \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Make python3.12 the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Configure pipx to install binaries in /usr/local/bin (accessible to all users)
ENV PIPX_BIN_DIR=/usr/local/bin
ENV PIPX_HOME=/usr/local/pipx
RUN pipx ensurepath

# Install UV globally via pipx (pinned version for reproducibility)
ARG UV_VERSION=0.1.40
RUN pipx install uv==${UV_VERSION}

# Install Bazelisk (manages Bazel versions) - pinned version for reproducibility
ARG BAZELISK_VERSION=v1.19.0
RUN set -eux; \
    ARCH=$(uname -m); \
    case "$ARCH" in \
        x86_64) ARCH=amd64 ;; \
        aarch64|arm64) ARCH=arm64 ;; \
        *) echo "Unsupported arch: $ARCH" && exit 1 ;; \
    esac; \
    curl -fsSL https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-${ARCH} \
        -o /usr/local/bin/bazel && chmod +x /usr/local/bin/bazel

# Install Buildifier (Bazel formatter) - pinned version for reproducibility
ARG BUILDTOOLS_VERSION=v6.4.0
RUN set -eux; \
    ARCH=$(uname -m); \
    case "$ARCH" in \
        x86_64) ARCH=amd64 ;; \
        aarch64|arm64) ARCH=arm64 ;; \
        *) echo "Unsupported arch: $ARCH" && exit 1 ;; \
    esac; \
    curl -fsSL https://github.com/bazelbuild/buildtools/releases/download/${BUILDTOOLS_VERSION}/buildifier-linux-${ARCH} \
        -o /usr/local/bin/buildifier && chmod +x /usr/local/bin/buildifier

# Install developer CLI tools via pipx
RUN pipx install pre-commit \
    && pipx install ruff \
    && pipx install mypy

################################################################################
# --- Stage 1: dev image with user setup and project prep --------------------#
################################################################################
FROM base AS dev

# Create vscode user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create user and group (robust logic handles Ubuntu 24.04 UID 1000 conflicts)
RUN set -eux; \
    # 1. ensure group \
    if ! getent group "${USER_GID}" >/dev/null; then \
        groupadd --gid "${USER_GID}" "${USERNAME}"; \
    fi; \
    # 2. create user or rename existing uid=1000 \
    if id -u "${USER_UID}" >/dev/null 2>&1; then \
        OLD_USER="$(getent passwd "${USER_UID}" | cut -d: -f1)"; \
        if [ "${OLD_USER}" != "${USERNAME}" ]; then \
            OLD_GROUP="$(id -gn "${OLD_USER}")"; \
            usermod -l "${USERNAME}" \
                    -d "/home/${USERNAME}" -m \
                    "${OLD_USER}"; \
            groupmod -n "${USERNAME}" "${OLD_GROUP}"; \
        fi; \
    else \
        useradd --uid  "${USER_UID}" \
                --gid  "${USER_GID}" \
                --create-home --shell /bin/bash "${USERNAME}"; \
    fi; \
    # 3. guarantee ownership of the home hierarchy \
    chown -R "${USERNAME}:${USERNAME}" "/home/${USERNAME}"; \
    # 4. password-less sudo \
    echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}; \
    chmod 0440 /etc/sudoers.d/${USERNAME}

# Set up workspace directory (as root)
WORKDIR /workspaces/the-company-os

# Configure git safe directory (as root)
RUN git config --global --add safe.directory /workspaces/the-company-os

# Set environment variables for development
ENV PYTHONPATH=/workspaces/the-company-os
ENV UV_CACHE_DIR=/workspaces/the-company-os/.uv-cache
ENV BAZEL_CACHE_DIR=/home/${USERNAME}/.cache/bazel
ENV VIRTUAL_ENV=/workspaces/the-company-os/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create cache directories with proper permissions for vscode user
RUN mkdir -p /home/${USERNAME}/.cache/bazel \
    && mkdir -p /workspaces/the-company-os/.uv-cache \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.cache \
    && chown -R ${USERNAME}:${USERNAME} /workspaces/the-company-os/.uv-cache

# Guarantee VS Code server can write even when we bind-mount deeper paths
RUN mkdir -p /home/${USERNAME}/.vscode-server/data/User/globalStorage \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.vscode-server

# Switch to vscode user for runtime
USER $USERNAME

# Default command
CMD ["/bin/bash"]
