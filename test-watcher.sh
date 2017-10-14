#!/usr/bin/env bash
# This script will start a watcher which will run the tests every time a python file is saved.

fswatch -e ".*" -i ".*/[^.]*\\.py$" . | xargs -n1 ./test.sh
