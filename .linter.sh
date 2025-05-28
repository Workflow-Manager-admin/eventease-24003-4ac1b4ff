#!/bin/bash
cd /home/kavia/workspace/code-generation/eventease-24003-4ac1b4ff/eventease
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

