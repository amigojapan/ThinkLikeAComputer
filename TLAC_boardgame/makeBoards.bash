#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

# Resolve the real directory, including when called through the tutorial symlink.
board_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_dir="$(dirname -- "$board_dir")"
cd "$board_dir"

case "${1:-all}" in
    all|--advanced|--basics) ;;
    *) echo "Usage: bash makeBoards.bash [--advanced|--basics]" >&2; exit 2 ;;
esac

if [[ "${1:-all}" == "all" ]]; then
    for example in docs_loops_countdown docs_loops_do_while_new docs_loops_forloop \
        docs_loops_multiple_forloops docs_loops_foreachLoop docs_loops_nested_forloops \
        docs_operations_on_lists mazeTest; do
        python3 html_board_creaotr.py < "${example}-output.txt" > "${example}-output.html"
    done
    python3 "$repo_dir/build_pyramid_sort.py"
    python3 "$repo_dir/build_maze.py"
fi

# Execute each actual lesson source, then create its complete board replay.
# Both versions are kept separately so the loop and recursive runs can be compared.
if [[ "${1:-all}" != "--basics" ]]; then
    for problem in 4 5 6 7 8; do
        python3 "$repo_dir/build_TLAC_advanced_executions.py" "problem${problem}-loop"
        python3 "$repo_dir/build_TLAC_advanced_executions.py" "problem${problem}-recursive"
    done
    python3 "$repo_dir/build_TLAC_advanced_executions.py" classes-turtle
    python3 "$repo_dir/build_TLAC_advanced_executions.py" classes-two-turtles

# Embed their initial/final boards and execution links in all three languages.
    python3 "$repo_dir/build_TLAC_advanced_concepts.py"
fi

if [[ "${1:-all}" != "--advanced" ]]; then
    python3 "$repo_dir/build_TLAC_basics_executions.py"
    python3 "$repo_dir/build_TLAC_basics.py"
fi
