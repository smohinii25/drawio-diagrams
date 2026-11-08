#!/bin/bash
#
# Export a .drawio file to an image that draw.io can still edit.
#
# Usage: export.sh <file.drawio> [svg|png] [--force]
#
# Writes <file>.drawio.svg (default) or <file>.drawio.png next to the source,
# with a copy of the diagram embedded. An image newer than its source is left
# alone, in case it was edited directly; --force replaces it anyway.
#
# Set DRAWIO_BIN to use a draw.io binary in a non-standard location.
#
# Exit codes: 0 exported, already up to date, or draw.io is not installed
#             1 the export failed
#             2 bad usage or unusable input

set -u

usage() {
  echo "Usage: export.sh <file.drawio> [svg|png] [--force]" >&2
  exit 2
}

find_drawio() {
  if [ -n "${DRAWIO_BIN:-}" ]; then
    [ -x "$DRAWIO_BIN" ] && echo "$DRAWIO_BIN"
    return
  fi
  local app
  for app in "/Applications/draw.io.app/Contents/MacOS/draw.io" \
             "$HOME/Applications/draw.io.app/Contents/MacOS/draw.io"; do
    if [ -x "$app" ]; then
      echo "$app"
      return
    fi
  done
  command -v drawio
}

input=""
format=""
force=0
for arg in "$@"; do
  case "$arg" in
    --force) force=1 ;;
    svg | png)
      [ -z "$format" ] || usage
      format="$arg"
      ;;
    -*) usage ;;
    *)
      [ -z "$input" ] || usage
      input="$arg"
      ;;
  esac
done
[ -n "$input" ] || usage
format="${format:-svg}"

case "$input" in
  *.drawio) ;;
  *)
    echo "Error: expected a .drawio file, got: $input" >&2
    exit 2
    ;;
esac
if [ ! -f "$input" ]; then
  echo "Error: file not found: $input" >&2
  exit 2
fi

drawio="$(find_drawio)"
if [ -z "$drawio" ]; then
  echo "draw.io desktop was not found, so no image was exported."
  echo "The diagram itself is fine: $input"
  echo "To enable export, install draw.io desktop from"
  echo "https://github.com/jgraph/drawio-desktop/releases"
  echo "or export from draw.io or app.diagrams.net with File > Export as."
  exit 0
fi

output="$input.$format"
if [ "$force" -eq 0 ] && [ "$output" -nt "$input" ]; then
  echo "Skipped: $output is newer than its source, so it is up to date or was edited directly."
  echo "Re-run with --force to replace it."
  exit 0
fi

# Export to a temp file, so a failed run cannot damage an existing image.
workdir="$(mktemp -d)" || exit 1
trap 'rm -rf "$workdir"' EXIT
temp="$workdir/export.$format"

scale=()
if [ "$format" = "png" ]; then
  scale=(--scale 2)
fi

if ! log="$("$drawio" --export --format "$format" --embed-diagram --border 10 \
  ${scale[@]+"${scale[@]}"} --output "$temp" "$input" 2>&1)"; then
  echo "Error: draw.io could not export $input" >&2
  echo "$log" >&2
  exit 1
fi
if [ ! -s "$temp" ]; then
  echo "Error: draw.io produced no output for $input" >&2
  echo "$log" >&2
  exit 1
fi

if ! mv "$temp" "$output"; then
  echo "Error: could not write $output" >&2
  exit 1
fi
echo "Exported: $output"

pages="$(grep -c '<diagram[ >]' "$input")"
if [ "$pages" -gt 1 ]; then
  echo "Note: the image shows page 1 of $pages. All $pages pages stay editable in draw.io."
fi
