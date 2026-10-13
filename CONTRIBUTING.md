# Contributing

Reproduce one narrow problem with Python 3.10+ before proposing a change.
Run `python3 -m unittest discover -s tests -v` and `python3 tests/offline_demo.py`.
These tests use synthetic inputs and do not need provider credentials or network access.
Keep a change scoped to a single issue; describe expected versus actual behaviour.
Do not commit API keys, real buyer messages, audit histories, private URLs or customer data.
Provider integration tests need your own account, explicit spend approval and sanitized output.
Use the security contact rather than a public issue for a vulnerability.
Maintainers review on a best-effort basis; no response-time or free implementation promise.
