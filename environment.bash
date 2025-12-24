#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function launch_tests ()
{
    local test_dir="${PROJECT_ROOT}/tests"
    local logs_dir="${PROJECT_ROOT}/logs"
    echo "Launching tests in '${test_dir}'..."

    if [[ ! -d "${test_dir}" ]]; then
        echo "Test directory '${test_dir}' not found" >&2
        return 2
    fi
    
    cd ${PROJECT_ROOT}
    mkdir -p ${logs_dir}

    shopt -s nullglob
    local rc=0

    for f in "${test_dir}"/test_*.py; do
        base=$(basename "$f" .py)
        logfile="${logs_dir}/${base}.log"
        module="tests.${base}"
        
        echo "Running ${module} -> ${logfile}"
        python3 -m unittest -v "${module}" &> "${logfile}"
        status=$?

        if [[ $status -ne 0 ]]; then
            rc=1
            echo "Test ${module} failed (see ${logfile})"
        fi
    done

    shopt -u nullglob

    if [[ $rc -eq 0 ]]; then
        echo "All tests passed"
    else
        echo "Some tests failed; see corresponding .log files"
    fi

    return $rc
}