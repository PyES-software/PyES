#!/bin/sh
# Path to the requirements file
REQUIREMENTS_FILE="requirements/base.txt"

# Run the command to export the requirements
uv export -o "$REQUIREMENTS_FILE" --no-hashes --no-dev -q

# Create a temporary file
TMP_FILE=$(mktemp)

# Process the file using sed with global flag (g)
# This matches both https and ssh URLs
sed -E 's/([a-zA-Z0-9_-]+) @ git\+(https:\/\/github\.com|ssh:\/\/git@github\.com)\/([^\/]+)\/([^\/]+)\.git@([a-f0-9]+)/git\+https:\/\/github\.com\/\3\/\4\.git#egg=\1/g' "$REQUIREMENTS_FILE" > "$TMP_FILE"

# Replace the original file with the modified content
mv "$TMP_FILE" "$REQUIREMENTS_FILE"
