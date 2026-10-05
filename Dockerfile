FROM docker.io/library/python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
COPY pyproject.toml .
RUN python -c "import subprocess,tomllib; p=tomllib.load(open('pyproject.toml','rb'))['project']; subprocess.check_call(['pip','install',*p['dependencies'],*p['optional-dependencies']['dev']])"
COPY app ./app
COPY tests ./tests
RUN pip install --no-deps ".[dev]"
RUN useradd --create-home biblioteca && chown -R biblioteca /app
USER biblioteca
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "app.main:create_app()"]
