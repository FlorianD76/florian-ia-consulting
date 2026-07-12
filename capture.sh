#!/bin/bash
GITHUB_REPO=~/florian-ia-consulting
OBSIDIAN_FOLDER="/Users/floriandierckx/Documents/Obsidian Vault/FLOWA_BRAIN/03_IA_CONSULTING"
if [ -z "$1" ]; then
  echo "Utilisation: ./capture.sh chemin/vers/mon-fichier.md [dossier-github]"
  exit 1
fi
FILE="$1"
FOLDER="${2:-strategy}"
FILENAME=$(basename "$FILE")
if [ ! -f "$FILE" ]; then
  echo "Fichier introuvable: $FILE"
  exit 1
fi
mkdir -p "$GITHUB_REPO/$FOLDER"
cp "$FILE" "$GITHUB_REPO/$FOLDER/$FILENAME"
cd "$GITHUB_REPO"
git add "$FOLDER/$FILENAME"
git commit -m "Add $FILENAME"
git push
cp "$FILE" "$OBSIDIAN_FOLDER/$FILENAME"
echo "Termine ! GitHub: $FOLDER/$FILENAME | Obsidian: 03_IA_CONSULTING/$FILENAME"
