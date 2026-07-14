# mobot-skills

## Dotfiles

Shell env setup lives in `dotfiles/`. Run once from that directory: `./setup.sh`
It symlinks the files into `~` and loads `~/startup.sh` from `~/.bashrc`.

## PI WEB plugins

Local plugins live in `pi-web-plugins/`. Link the directory into PI WEB:

```bash
mkdir -p ~/.pi-web
ln -sfn "$PWD/pi-web-plugins" ~/.pi-web/plugins
```

Hard reload PI WEB after plugin changes.
