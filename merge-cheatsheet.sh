#!/usr/bin/env bash
# Merge the team's Canva deck with the part-2 additions into one printable PDF.
#
#   ./merge-cheatsheet.sh <canva-export.pdf> [portrait|landscape]
#
# Export the deck from Canva as  Share > Download > PDF Print.
# Do NOT route it through .pptx - that export is lossy (text overflows,
# titles get clipped).
set -euo pipefail

CANVA="${1:?usage: $0 <canva-export.pdf> [portrait|landscape]}"
MODE="${2:-landscape}"
DIR="$(cd "$(dirname "$0")" && pwd)"

case "$MODE" in
  landscape) PART2="$DIR/cheatsheet-part2-landscape.pdf" ;;
  portrait)  PART2="$DIR/cheatsheet-part2.pdf" ;;
  *) echo "mode must be portrait or landscape" >&2; exit 1 ;;
esac

[ -f "$CANVA" ]  || { echo "not found: $CANVA" >&2; exit 1; }
[ -f "$PART2" ]  || { echo "not found: $PART2" >&2; exit 1; }

OUT="$DIR/cheatsheet-COMPLETE.pdf"
pdfunite "$CANVA" "$PART2" "$OUT"

N=$(pdfinfo "$OUT" | awk '/^Pages:/{print $2}')
echo "wrote $OUT"
echo "pages: $N  (limit is 25)"
[ "$N" -le 25 ] || echo "WARNING: over the 25-page limit"
