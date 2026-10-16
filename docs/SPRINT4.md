# Sprint 4 theme checkpoint

Version 0.2.3 contains the delivered theme-feedback source corrections:

- Use scene artwork for native heroes when supplied by the exporter; fit title
  artwork when no usable scene is available.
- Try another artwork role after an image fails, with role-based fit/crop.
- Hide the duplicate artwork-area fallback title once an image is ready.
- Remove the always-selected Play style; hide background selection in dialogs.
- Use the system menu's positional action/shoulder glyphs and arrows, deriving
  action glyphs from Pegasus's actual configured bindings.
- Retain the live library-refresh root wrapper used by the Zaman deployment.

The source is based on the delivered 0.2.2 theme and the later feedback package.
The library/exporter changes live in zaman-sessiond, not duplicated in this theme.
The source JavaScript regression checks passed; Qt/on-console visual acceptance
of the theme-feedback package has not yet been recorded for this release.
Older `preview/*.png` images illustrate the preceding layout and are retained as
historical development fixtures, not current release screenshots.
