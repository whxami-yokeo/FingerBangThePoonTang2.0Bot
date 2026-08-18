FROM python:3.14

WORKDIR /app

# Install Deno for yt-dlp JS runtime support, and native Linux ffmpeg
RUN apt-get update && apt-get install -y curl unzip ffmpeg \
    && curl -fsSL https://deno.land/install.sh | DENO_INSTALL=/usr/local sh \
    && apt-get remove -y curl unzip \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

# Use system-installed ffmpeg (Linux) instead of the bundled macOS binary
ENV PATH="/usr/bin:$PATH"

CMD ["python", "-u", "main.py"]
