FROM mcr.microsoft.com/devcontainers/python:3.11

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get -qq -y upgrade \
  && DEBIAN_FRONTEND=noninteractive apt-get -qq -y --no-install-recommends install firefox-esr

USER vscode
