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
