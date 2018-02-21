#!/bin/bash
set -eo pipefail

function lint () {
    echo "Checking the code syntax"
    pycodestyle --first chaosext
}

function build () {
    echo "Building the chaostoolkit-humio package"
    python setup.py build
}

function run-test () {
    echo "Running the tests"
    python setup.py test
}

function main () {
    lint || return 1
    build || return 1
    run-test || return 1
}

main "$@" || exit 1
exit 0
