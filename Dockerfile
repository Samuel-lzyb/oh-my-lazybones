# All-in-one Dockerfile — builds API + frontend, serves via uvicorn + StaticFiles
FROM node:22-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev pkg-config curl \
    && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt aiomysql

COPY server/ ./server/
COPY cli/ ./cli/
COPY --from=frontend-builder /frontend/dist ./cli/lazybones/frontend_dist/

RUN pip install -e ./cli/

EXPOSE 9527
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:9527/api/v1/health || exit 1

CMD ["lazy", "serve", "--port", "9527"]
