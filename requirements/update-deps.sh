set -e
pip-compile --no-emit-index-url requirements/test.in > requirements/test.txt
pip-compile --no-emit-index-url requirements/dev.in > requirements/dev.txt
