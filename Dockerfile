
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/models/cache

WORKDIR /app

# Install CPU-only PyTorch first.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu

# Copy only the package source and required project metadata.
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir . fastapi uvicorn

COPY docker/app.py ./app.py

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
