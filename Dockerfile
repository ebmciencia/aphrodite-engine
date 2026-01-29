# Usando base CUDA 12.4
FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/bin/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala o Aphrodite Engine do GitHub
RUN uv pip install --system --no-cache --force-reinstall \
    git+https://github.com/ebmciencia/aphrodite-engine.git

# Aplica patch para aceitar campos extras (scale_dtype, zp_dtype)
RUN python3 -c "import pathlib, aphrodite; \
    f = pathlib.Path(aphrodite.__file__).parent / 'config' / 'aphrodite.py'; \
    f.write_text(f.read_text().replace('extra=\"ignore\"', 'extra=\"allow\"'))"

# Limpa cache Python
RUN find /usr/local/lib -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib -name "*.pyc" -delete 2>/dev/null || true

# Instala dependencias
RUN uv pip install --system \
    --extra-index-url https://downloads.pygmalion.chat/whl \
    aphrodite-kernels==0.0.1

RUN uv pip install --system --upgrade \
    git+https://github.com/huggingface/transformers.git

RUN uv pip install --system --force-reinstall \
    transformers==4.56.0 \
    numba==0.61.2

EXPOSE 8000
