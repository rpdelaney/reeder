FROM python:3.13-slim-bookworm
RUN apt-get update && apt-get upgrade -y \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/*
RUN addgroup --system reeder \
&&  adduser --system --ingroup reeder reeder

WORKDIR /app
RUN chown -R reeder:reeder /app

COPY --chown=reeder:reeder README.rst ./uv.lock ./pyproject.toml ./
COPY --chown=reeder:reeder  ./reed ./reed

USER reeder
RUN python3 --version && python3 -m pip --version \
&&  python3 -m venv venv \
&&  . ./venv/bin/activate \
&&  python3 -m pip install --disable-pip-version-check --isolated --no-input --no-cache-dir uv==0.8.2 \
&&  uv sync --no-dev --no-cache --locked \
&&  python3 -m pip install --disable-pip-version-check --isolated --no-input --no-cache-dir .

EXPOSE 8000
ENV PYTHONOPTIMIZE=1
ENV PATH="/app/venv/bin/:${PATH}"
ENTRYPOINT ["python3", "-m", "reed"]
