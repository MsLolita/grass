FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

LABEL maintainer="Jager <im@zhang.ge>"
LABEL description="Docker Image of Grass-mining"

WORKDIR /grass

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip install \
    --no-cache-dir \
    -r /tmp/requirements.txt

COPY . .

CMD ["python", "main.py"]

