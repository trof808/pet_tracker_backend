# FROM python:3.13-slim

# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Копируем только файлы зависимостей сначала
# COPY pyproject.toml poetry.lock ./

# RUN pip install poetry && \
#     poetry config virtualenvs.create false && \
#     poetry install --no-interaction --no-ansi --without dev

# # Копируем остальные файлы
# COPY pet_tracker_backend/ ./pet_tracker_backend/

# # Применяем миграции
# RUN if [ -f "alembic.ini" ]; then \
#     poetry run alembic upgrade head; \
#     fi

# EXPOSE 8000

FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Create __init__.py if it doesn't exist (safety check)
RUN mkdir -p app && touch app/__init__.py

# Install the application in editable mode
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000