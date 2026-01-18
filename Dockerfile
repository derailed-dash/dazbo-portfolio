# Stage 1: Build the React frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Final production image
FROM python:3.12-slim

RUN pip install --no-cache-dir uv==0.8.13

WORKDIR /code

# Copy backend requirements and install
COPY ./pyproject.toml ./README.md ./uv.lock* ./
RUN uv sync --frozen

# Copy backend code
COPY ./app ./app

# Copy built frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist /code/frontend/dist

ARG COMMIT_SHA=""
ENV COMMIT_SHA=${COMMIT_SHA}

ARG AGENT_VERSION=0.0.0
ENV AGENT_VERSION=${AGENT_VERSION}

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app.fast_api_app:app", "--host", "0.0.0.0", "--port", "8080"]
