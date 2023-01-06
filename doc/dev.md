---
modified: 2023-01-07
---

# Development notes

Roughly contemporaneous notes about general development.  I imagine I will thank
myself later.

## Setup

I use Windows 11, WSL2, Docker Desktop, Windows Terminal, and Visual Studio Code
with the Dev Containers extension.  (It is a delicious irony that the "year of
the Linx desktop" was possibly 2020, the year that both WSL 2 and the Windows
Terminal reached general availability.)

The combination feels like a sweet spot.  The development tools are robustly 
encapsulated in a Linux environment via Docker, but with a first class user
interface via VS Code and Dev Containers.

**TODO: ensure the workflow works outside of Dev Containers**

Generally, things work pretty much out of the box, but some notes follow.

### WSL 2 setup

Install WSL 2, Windows Terminal, Docker Desktop and VS Code.

WSL2 allows for multiple "distros" (e.g. Ubuntu, Debian), but is a bit funny
about how they are managed and assumes that you will only install a distro
once.  As each distro is like a "lightweight VM" I wanted the option of
installing a distro multiple times.  Here are basic instructions for that.

- Install the distro from the store
- Do any basic configuration (e.g. user, password, sudo, apt)
- Export the distro to a tar file with `wsl --export <distro> <tarfile>`
- Stop the distro: `wsl -t <distro>`
- Unregister the distro `wsl --unregister <distro>`
- Disable the Windows Terminal profile for `<distro>`
- Import the distro with a new name: `wsl --import <newname> <folder> <tarfile>`

By default, the distro will use the host's hostname and start as root, so fix
that in `/etc/wsl.conf`:

```ini
[user]
default = <username>

[network]
hostname = <newname>
```

### Windows Terminal

My Windows Terminal has some light configuration for keyboard shortcuts and
theme.  (I found the "Tango Dark" theme the most legible.)

### Docker

For Docker, ensure that it uses the WSL 2 backend, and that WSL 2 integration is
enable for the distro/instance(s) you plan to use.

### VS Code

In VS code, install the Remote Development extension pack.  This enables working
with both the WSL2 environment and the docker container.

### SSH

I tried to use the `ControlMaster` feature of SSH to keep the SSH connection
open to github and avoid having to enter my SSH key passphrase, but it seems
github doesn't like that.  Use the `keychain` package to manage ssh-agent, and
run it in your `~/.bashrc`.

```bash
sudo apt install keychain
eval $(keychain -q -Q)
```

Per https://pscheit.medium.com/use-an-ssh-agent-in-wsl-with-your-ssh-setup-in-windows-10-41756755993e

## Dev Containers and bootstrapping

I spent quite some time researching the options and eventually realised that the
simplest config would work: just create a `.devcontainer.json` with an image
reference and port forward:

```json
{
    "image": "mcr.microsoft.com/devcontainers/python:3.11",
    "forwardPorts": [
        8000
    ]
}
```

That image includes the VS Code Python extension and various python tools, and
is based on the "official" Python docker image.  It also includes node.js, which
will be useful later for testing javascript.

In VS Code, run "Dev Containers: Open folder in container" and it will create
the docker container and install the VS Code components.

Next, I added a basic HTTP server on port 8000 and ran the file by pressing F5.
VS Code detects the listening server and prompts to open a browser.  I confirm
it works.

And bootstrapping is complete!

## Next steps

The VS Code python extension complained about missing docstrings, so configure
pylint in `.pylintrc`:

```ini
[MAIN]
persistent = no

[MESSAGES CONTROL]
disable = missing-module-docstring,
        missing-function-docstring,
        missing-class-docstring
```

In general I prefer to avoid dependencies where possible, but the HTTP library
in Python is far too basic to be usable, so I needed to choose a better option.
`Werkzeug` is the server behind `Flask` so I use that.

First, I `exec` into the docker container and install the dependency:

```bash
docker ps -a # get the container name or id
docker exec -itu vscode <container> pip install werkzeug
```

Now the bootstrap code is much simpler:

```python
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

@Request.application
def hello(_):
    return Response('Hello, world!')

def main():
    run_simple('0.0.0.0', 8000, hello, use_reloader=True, use_debugger=True)

if __name__ == '__main__':
    main()
```

Run again with F5 and confirm it is working.

Now we need to ensure the dev container installs the dependency.  While the
install command could be added to the `.devcontainer.json`, I feel that the
project should function without requiring VS Code at all, so it is better to use
a `Dockerfile` and build the dependency into the image

In `.devcontainer.json`:

```diff
-    "image": "mcr.microsoft.com/devcontainers/python:3.11",
+    "build": {
+        "dockerfile": "./Dockerfile"
+    },
```

And add a `Dockerfile`:

```Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11
USER vscode
RUN pip install --user werkzeug
```
