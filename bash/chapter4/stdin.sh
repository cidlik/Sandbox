#!/usr/bin/env bash

set -eu
TMP_FILE=tmp.txt

../block.sh "Read from file instead of stdin"
echo foo > $TMP_FILE
cat < $TMP_FILE
rm $TMP_FILE

../block.sh "Put plain text into file"
cat > $TMP_FILE << EOF
first line
second 'line

forth "line"
EOF
cat $TMP_FILE
rm $TMP_FILE
