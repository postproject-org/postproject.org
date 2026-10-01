# postproject.org

Landing page for [PostProject](https://github.com/postproject-org/postproject),
published to `www.postproject.org` with GitHub Pages. The apex domain points to
GitHub Pages and redirects to `www`.

The page serves its stylesheet, logo, and Inter font from this repository.
It uses no third-party resource hosts. The variable font in `fonts/` is
[Inter 4.1](https://github.com/rsms/inter/tree/e3a3d4c57d5ecc01453a575621882a384c1995a3),
distributed under the included SIL Open Font License (`fonts/LICENSE.txt`).

`theme.css` follows the system's light/dark preference. Keep it and the font
assets synchronized with `postproject/docs/_static/`, which also supplies the
Sphinx and Rust API documentation palettes.
