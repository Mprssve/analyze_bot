version: "3.9"

services:
  panicbot:
    build: .
    container_name: panic-telegram-bot
    env_file:
      - .env
    restart: unless-stopped
