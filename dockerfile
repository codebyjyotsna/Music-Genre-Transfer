# Backend
FROM python:3.9-slim as backend

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:14 as frontend
WORKDIR /frontend
COPY ./frontend/package.json .
RUN npm install
COPY ./frontend .
RUN npm run build

# Final Stage
FROM nginx:alpine
COPY --from=frontend /frontend/build /usr/share/nginx/html
