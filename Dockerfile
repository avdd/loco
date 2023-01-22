FROM mcr.microsoft.com/devcontainers/python:3.11

RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get -qq -y upgrade \
  && DEBIAN_FRONTEND=noninteractive apt-get -qq -y --no-install-recommends install firefox-esr

USER vscode
RUN pip install --user werkzeug watchdog selenium
RUN echo /workspaces/loco/src > ~/.local/lib/python3.11/site-packages/loco.pth
COPY tools/install-geckodriver.sh /tmp/install-geckodriver.sh
RUN bash /tmp/install-geckodriver.sh
