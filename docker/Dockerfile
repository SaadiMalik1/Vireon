# Stage 1: Build dependencies & Rust extension
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain nightly
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade pip maturin build

COPY pyproject.toml README.md Makefile ./
COPY crates ./crates
COPY vireon ./vireon

RUN cd crates/neurodsl/python_ext && maturin build --release --out /tmp/wheels
RUN python -m build --wheel --outdir /tmp/wheels

# Stage 2: Final runtime image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -r vireon && useradd -r -g vireon -d /app vireon

COPY --from=builder /tmp/wheels/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm -rf /tmp/*.whl

USER vireon

ENTRYPOINT ["vireon"]
CMD ["info"]
