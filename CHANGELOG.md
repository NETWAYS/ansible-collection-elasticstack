# Netways\.Elasticstack Release Notes

**Topics**

- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary"></a>
### Release Summary

First release of this collection\. It installs and manages the Elastic Stack
on Linux\, with a role for every component and a self\-signed stack CA that wires TLS between
them\.

<a id="minor-changes"></a>
### Minor Changes

* The collection declares <code>community\.crypto</code> as a dependency now\, so installing it with <code>ansible\-galaxy</code> pulls in what the beats role needs to check certificate expiration\.
* The documentation was restructured along the collection template\. <code>docs/01\-requirements\.md</code> became <code>docs/requirements\.md</code>\, version pinning and upgrading moved to <code>docs/upgrades\.md</code>\, and the role pages under <code>docs/</code> that only linked to the role READMEs were removed\. Module documentation is read with <code>ansible\-doc</code> instead of from copies under <code>docs/</code>\.
* <code>elasticstack\_kibana\_host</code> is a declared and documented variable now\, defaulting to the fully qualified domain name of the Kibana host\. The Kibana template referenced it ad hoc before\, without a default of its own\.

<a id="new-modules"></a>
### New Modules

* netways\.elasticstack\.cert\_info \- Retrieve information from a PKCS12 certificate
* netways\.elasticstack\.elasticsearch\_role \- Manage Elasticsearch roles
* netways\.elasticstack\.elasticsearch\_user \- Manage Elasticsearch users
