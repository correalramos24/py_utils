#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Enabling environment!"

function ensure_venv ()
{
    # Create virtualenv if missing and activate it
    if [[ ! -d "${PROJECT_ROOT}/.venv" ]]; then
        echo ".venv not found — creating virtualenv..."

        if ! command -v python3 >/dev/null 2>&1; then
            echo "python3 not found in PATH" >&2
            return 1
        fi

        python3 -m venv "${PROJECT_ROOT}/.venv" || {
            echo "Failed to create virtualenv" >&2
            return 1
        }

        "${PROJECT_ROOT}/.venv/bin/python" -m pip install --upgrade pip || {
            echo "Failed to upgrade pip inside virtualenv" >&2
            return 1
        }

        echo "Virtualenv created at ${PROJECT_ROOT}/.venv"
    fi

    # Activate the virtualenv
    # shellcheck disable=SC1090
    source "${PROJECT_ROOT}/.venv/bin/activate"
}

# Ensure and activate venv
ensure_venv || exit 1

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


echo "DONE!"