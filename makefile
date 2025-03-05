ANSIBLE_LINTER = ansible-lint
YAMLLINT = yamllint

.PHONY: all
all: ansible-lint yamllint cleanup

.PHONY: ansible-lint
ansible-lint:
	@echo "Running ansible-lint..."
	$(ANSIBLE_LINTER) ./roles/*

.PHONY: yamllint
yamllint:
	@echo "Running yamllint..."
	$(YAMLLINT) .

.PHONY: cleanup
cleanup:
	@echo "Cleaning up..."
	rm -rf .ansible
