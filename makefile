ANSIBLE_LINTER = ansible-lint
YAMLLINT = yamllint

.PHONY: all
all: venv ansible-lint yamllint cleanup

.PHONY: ansible-lint
ansible-lint:
	@echo "Running ansible-lint..."
	. .venv/bin/activate && $(ANSIBLE_LINTER) ./roles/*

.PHONY: yamllint
yamllint:
	@echo "Running yamllint..."
	. .venv/bin/activate && $(YAMLLINT) .

.PHONY: cleanup
cleanup:
	@echo "Cleaning up..."
	rm -rf .ansible

.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	python3 -m venv .venv
	@echo "Activating virtual environment and installing test requirements..."
	. .venv/bin/activate && pip install -r requirements-test.txt
