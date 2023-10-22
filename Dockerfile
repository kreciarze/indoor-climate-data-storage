FROM python:3.11-slim-bullseye

# Only in Docker on Mac M1
RUN if [ "$(uname -m)" = 'aarch64' ] ; then \
    update-ca-certificates ; \
    fi

# Install compilation dependencies
RUN apt update && apt install -y \
    build-essential \
    gcc \
    git \
    make \
    netcat \
    openssl \
    pkg-config \
    python3-dev \
    wget \
    zstd \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Poetry installation

ENV POETRY_VERSION=1.6.1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/src

RUN wget -O- https://install.python-poetry.org | python - --version ${POETRY_VERSION}
ENV PATH="/root/.local/bin:$PATH"
# Allows docker to cache installed dependencies between builds
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
# Installing "standard" dependencies only, without dev. Done before getting commit sha to cache this layer
RUN poetry config virtualenvs.create false \
  && poetry install --only=main --no-interaction --no-ansi


ARG BUILD_COMMIT_SHA
ENV BUILD_COMMIT_SHA ${BUILD_COMMIT_SHA:-}

# Installing dev dependencies only (on top of standard dependencies installed above). Triggered only for test image.
RUN if [ "$BUILD_COMMIT_SHA" = "localdev" ]; then \
    poetry install --only=dev --no-interaction --no-ansi; \
    fi

# Adds our application code to the image
COPY . /code
WORKDIR /code/src

ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Runs the production server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

