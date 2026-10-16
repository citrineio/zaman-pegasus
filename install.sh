#!/bin/sh
set -eu

# Install only the theme. Preview fixtures never enter the game library.
SOURCE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
THEMES_DIR=${XDG_CONFIG_HOME:-"$HOME/.config"}/pegasus-frontend/themes
if [ "$#" -gt 0 ]; then
    if [ "$#" -ne 2 ] || [ "$1" != "--themes-dir" ]; then
        echo "Usage: sh install.sh [--themes-dir /path/to/themes]" >&2
        exit 2
    fi
    THEMES_DIR=$2
fi
mkdir -p "$THEMES_DIR"
STAGING_DIR=$(mktemp -d "$THEMES_DIR/.zaman-install.XXXXXX")
trap 'rm -rf -- "$STAGING_DIR"' EXIT HUP INT TERM
for item in theme.qml theme.cfg components lib assets README.md LICENSE LICENSES.md docs; do
    cp -R -- "$SOURCE_DIR/$item" "$STAGING_DIR/"
done
mkdir -p "$STAGING_DIR/preview"
if [ -f "$SOURCE_DIR/preview/home.png" ]; then
    cp -- "$SOURCE_DIR/preview/home.png" "$STAGING_DIR/preview/home.png"
fi
# Preserve the deployed producer's refresh tokens while replacing theme code.
if [ -d "$THEMES_DIR/zaman/library-refresh" ] && [ ! -L "$THEMES_DIR/zaman/library-refresh" ]; then
    cp -R -- "$THEMES_DIR/zaman/library-refresh" "$STAGING_DIR/library-refresh"
fi
if [ -e "$THEMES_DIR/zaman" ] || [ -L "$THEMES_DIR/zaman" ]; then
    mkdir -p "$THEMES_DIR/../theme-backups"
    BACKUP_DIR=$(mktemp -d "$THEMES_DIR/../theme-backups/zaman.XXXXXX")
    rmdir -- "$BACKUP_DIR"
    mv -- "$THEMES_DIR/zaman" "$BACKUP_DIR"
    echo "Previous theme saved at: $BACKUP_DIR"
fi
mv -- "$STAGING_DIR" "$THEMES_DIR/zaman"
trap - EXIT HUP INT TERM
echo "Installed: $THEMES_DIR/zaman"
echo "Open Pegasus Settings, select Theme, then choose Zaman."
