FROM mcr.microsoft.com/devcontainers/python:3.11
USER vscode
RUN pip install --user werkzeug watchdog
