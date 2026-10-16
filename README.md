# Zaman for Pegasus

The Pegasus home and game-library theme built for the
[Zaman retro console](https://zaman.kawnelectro.com/), by
[Kawn Electro](https://kawnelectro.com/).

Zaman pairs a television-friendly game library with a controller-operated system
menu. This repository contains the library theme: warm selection colors, large
headings, a featured game, recent games, collections, favorites and search.
The companion [system menu](https://github.com/citrineio/zaman-menu) handles
settings and notifications; [sessiond](https://github.com/citrineio/zaman-sessiond)
handles launching and returning from managed games.

**Status:** prototype source checkpoint, version 0.2.3. The Sprint 4 feedback
corrections are included; their on-device visual acceptance remains to be recorded.
The theme is designed for Zaman, while ordinary game browsing uses Pegasus's
metadata and configured input mappings.

## Existing features

| Screen | What is available |
| --- | --- |
| Home | Featured selected game, Play/Details actions, and up to 20 recently played games; alphabetical games for a fresh library |
| Library | All games, collection filter, title/recent sort, title search, four- or five-column grid |
| Favorites | The same browsing tools restricted to favorite games |
| Game details | Description, artwork, metadata, play time, Play and favorite toggle |
| Search | Controller on-screen keyboard and printable keyboard input |
| Preferences | Reduced/standard navigation motion, grid density and featured artwork toggle |

The theme remembers preferences and selected game identity through Pegasus memory.
Game artwork is loaded asynchronously. Failed images fall through to other roles;
logos and box art fit inside their area, and fallback titles disappear when art
loads. The ordinary game caption below a card remains visible.

Native-game hero screenshots come from the companion exporter when available;
otherwise fitted local identity art can fill the hero. The theme does not download
or scrape a new artwork catalog itself. Play only uses selected styling while it
is selected or pressed. Dialogs remove background selection highlights.

## Install

With Pegasus and its Qt runtime already installed:

```sh
git clone https://github.com/citrineio/zaman-pegasus.git
cd zaman-pegasus
sh install.sh
```

Select **Zaman** in Pegasus Settings → Theme. Press **F5** in Pegasus after
editing theme files. Installation copies only this theme and backs up an existing
`zaman` theme; it does not select the theme, install dependencies, change services,
rewrite ROM metadata or modify a game installation.

The default destination is `$XDG_CONFIG_HOME/pegasus-frontend/themes/zaman`, or
`~/.config/pegasus-frontend/themes/zaman`. For another location:

```sh
sh install.sh --themes-dir /absolute/path/to/pegasus/themes
```

The target is Pegasus with Qt 5.15+ / Qt Quick and the Qt Labs FolderListModel
module used by the Zaman refresh wrapper. No custom native theme plugin is required.

## Navigation

The footer uses arrows for movement and positional face/shoulder icons for
configured actions. It reads Pegasus's current bindings, including remapped
Details/Search buttons, rather than printing internal action names. Keyboard
hints use the bound key names after a keyboard action.

| Action | Behavior |
| --- | --- |
| D-pad / arrows | Move through tabs, controls and games |
| Accept | Activate the current control or play the current game |
| Cancel / Back | Leave dialogs, return toward tabs/Home, then Pegasus's native menu |
| Escape | Close a theme dialog; otherwise open Pegasus's native menu |
| Details | Open the current game's details |
| Filters | Open search |
| Previous/next page | Cycle Home, Library, Favorites and Preferences |
| Page up/down | Move two rows in the library |
| Guide | Left to Zaman's existing system-menu/session ownership |

On Home, Up from recent games reaches Play/Details. Left/right chooses an action;
Up again reaches tabs, and Down returns to recent games. Pointer users can click
artwork for details, use the action buttons, and select/double-click cards.

## Integration

Game launch calls Pegasus `game.launch()`. Your game metadata determines the
actual launch command; on Zaman it routes managed games through `zamanctl`.
The theme does not supervise processes, acquire controller leases or implement
emulator autosave.

The root wrapper watches a bounded `library-refresh/*.signal` token supplied by
Zaman's native-game sync helper and requests provider reload after a changed token.
It retains the refresh token in Pegasus memory. The installer preserves an
existing refresh-signal directory; frontend/provider support is required for live
refresh. For non-Zaman use without a producer, ordinary startup loading still uses
your existing Pegasus library.

The native exporter, shared catalog and artwork conventions are documented in
[zaman-sessiond](https://github.com/citrineio/zaman-sessiond/blob/main/docs/sprint3-pegasus-library.md).
No games, game screenshots, ROMs or BIOS files are included in this repository.

## Development and validation

`components/Shell.qml` owns views/navigation; `GameArtwork.qml` owns role fallback;
`lib/Hints.js` derives the legend from configured keys. `preview/` contains fictional
fixtures for exercising the actual QML, not a bundled game library.

With the existing optional Python Qt bindings and Node:

```sh
node tests/feedback.cjs
python3 preview/run.py --test --output /tmp/zaman-theme-preview.png
```

Preview bindings: arrows, Enter, Escape, I for details, F for search and Q/E for
tabs. These do not replace Pegasus's settings. The JavaScript checks run without
Qt; preview rendering requires installed PyQt5 (or `--qt6` with PySide6).

The previous layout screenshots are historical fixtures, not evidence that this
checkpoint has been rendered on the console. Check native hero art, transparent
logos, exclusive focus, remapped legends and 1080p/1440p layouts on the target.
See [validation](docs/VALIDATION.md) and [Sprint 4 changes](docs/SPRINT4.md).

## Rights and acknowledgements

The theme code is licensed under the [MIT License](LICENSE), copyright 2026
Kawn Electro. You may use, modify and redistribute the code under those terms.
Zaman/Kawn Electro branding artwork and trademarks are separate from the code
license. Bundled fonts retain their included SIL Open Font License notices; the
normal UI face uses the platform font. See [license scope](LICENSES.md).

GAMEOS was reviewed as a navigation reference; its source/assets are not included.
Pegasus and all dependencies retain their own licenses. Questions and licensing
requests: [kadhem.alabdulmuhsin@kawnelectro.com](mailto:kadhem.alabdulmuhsin@kawnelectro.com).
