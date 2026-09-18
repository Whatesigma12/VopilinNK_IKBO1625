#!/bin/bash

text="$1"
len=$((${#text} + 2))
border=$(printf '%*s' "$len" '' | tr ' ' '-')

echo "+${border}+"
echo "| ${text} |"
echo "+${border}+"