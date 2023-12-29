#!/bin/bash

# Check if a commit message is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 <commit_message>"
  exit 1
fi

commit_message="$1"

git add .
git commit -m "$commit_message"
git push 