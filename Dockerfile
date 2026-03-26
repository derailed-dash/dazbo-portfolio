# Stage 1: Build the React frontend
# We use a Node image to build the frontend assets. These are later copied 
# into the final production image, keeping the final image lean.
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
# Copy package manifests first to leverage Docker layer caching for node_modules
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Final production image
# A slim Python image is Used for the final runtime environment.
FROM python:3.12-slim

# Install uv for fast, reliable Python package management.
RUN pip install --no-cache-dir uv==0.8.13

WORKDIR /code

# Copy dependency manifests and install.
# We use cache mounting to speed up builds and synchronization flags to:
# 1. --frozen: Ensure the environment matches the lockfile.
# 2. --no-dev: Exclude testing/dev tools from the production image.
# 3. --no-install-project: Skip installing the local packages until code is copied.
COPY ./pyproject.toml ./README.md ./uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# Copy the backend application code.
COPY ./app ./app

# Copy the built frontend static assets from Stage 1.
COPY --from=frontend-builder /app/frontend/dist /code/frontend/dist

# Inject build-time metadata.
ARG COMMIT_SHA=""
ENV COMMIT_SHA=${COMMIT_SHA}

ARG AGENT_VERSION=0.0.0
ENV AGENT_VERSION=${AGENT_VERSION}

# Create and switch to a non-root user for improved security (Principle of Least Privilege).
RUN useradd -m appuser
USER appuser

# Add the virtual environment's bin to PATH.
# We call uvicorn directly to avoid 'uv run' runtime sync checks, which 
# would otherwise fail on a cross-user/read-only .venv.
ENV PATH="/code/.venv/bin:$PATH"

EXPOSE 8080

CMD ["uvicorn", "app.fast_api_app:app", "--host", "0.0.0.0", "--port", "8080"]
