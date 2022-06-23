# Contribution Guidelines

## Table of Contents

- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Contributing Code](#contributing-code)
- [Style Guides](#style-guides)

## Reporting Bugs

This section provides a set of guidelines for reporting bugs.

### Before Submitting a Bug Report

- Identify that the problem is with PyISAM and not the IBM Security Access Manager appliance you are trying to configure. This can be achieved by issuing a simple cURL request to the Web service endpoint in question.
- Check the [Usage](README.md#usage) guide and documentation to ensure that PyISAM is being invoked as intended.
- Search for both [**open** and **closed** issues](https://github.ibm.com/ibm-security/pyisva/issues?utf8=%E2%9C%93&q=is%3Aissue) as the problem may have already been reported. If it has and is open, add a comment to the existing issue instead of opening a new one.

### Submitting a Bug Report

Bugs are tracked as [GitHub Issues](https://guides.github.com/features/issues).

- Use a short and descriptive title to identify the problem.
- Describe the steps required to reproduce the problem. Supplementing the steps with code snippets is encouraged and can be formatted with [code blocks](https://help.github.com/articles/creating-and-highlighting-code-blocks).
- Describe the observed behavior of the steps above, and what the expected behavior should be.
- Provide simple cURL commands to demonstrate usage of the IBM Security Access Manager Web service endpoint, if applicable.
- Apply the `bug` label to the issue.

### Example Bug Report

**Title**: Reverse Proxy - Restarting an instance is never successful

**Labels**: `bug`

**Description**: A reverse proxy instance named `default` has been configured on the appliance. Using the Local Management Interface the instance can be successfully restarted.

When executing the code snippet stated below, the instance is restarted, however the Response success is set to `False`.
```python
>>> import pyisva
>>> factory = pyisva.Factory("https://isam.mmfa.ibm.com", "admin", "Passw0rd")
>>> web = factory.get_web_settings()
>>> response = web.reverse_proxy.restart_instance("default")
>>> print response
<Response [False, 200]>
```
The expected value of the Response success is `True`, as the instance has been restarted and the Response status code is `200`. The Web service endpoint was additionally tested with the following cURL command:
```shell
curl -kv -u 'admin:Passw0rd' -H 'Accept: application/json' -H 'Content-type: application/json' -X PUT https://isam.mmfa.ibm.com/wga/reverseproxy/default -d '{"operation":"restart"}'
```

## Suggesting Enhancements

This section provides a set of guidelines for suggesting enhancements.

### Before Submitting an Enhancement Request

- Identify whether the enhancement belongs in PyISAM (specific to new functionality). PyISAM's functionality targets:
    - wrapping the IBM Security Access Manager Web service endpoints, and
    - common configuration tasks that requires multiple endpoint requests.
- Check the PyISAM documentation to ensure the enhancement is not already available.
- Search for both [**open** and **closed** issues](https://github.ibm.com/ibm-security/pyisva/issues?utf8=%E2%9C%93&q=is%3Aissue) as the enhancement may have already been suggested. If it has and is open, add a comment to the existing issue instead of opening a new one.

### Submitting an Enhancement Request

Enhancement requests are tracked as [GitHub Issues](https://guides.github.com/features/issues).

- Use a short and descriptive title to identify the enhancement.
- Describe the purposed enhancement including any expected behavior. Supplementing the description with code snippets is encouraged, if applicable, and can be formatted with [code blocks](https://help.github.com/articles/creating-and-highlighting-code-blocks).
- Provide simple cURL commands to demonstrate usage of the IBM Security Access Manager Web service endpoint, if applicable.
- Apply the `enhancement` label to the issue.

### Example Enhancement Request

**Title**: Reverse Proxy - Unconfiguring an instance is not supported

**Labels**: `enhancement`

**Description**: PyISAM is missing functionality for unconfiguring Reverse Proxy instances.

This task can be achieved with the following cURL command:
```shell
curl -kv -u 'admin:Passw0rd' -H 'Accept: application/json' -H 'Content-type: application/json' -X PUT https://isam.mmfa.ibm.com/wga/reverseproxy/default -d '{"admin_id":"sec_master","admin_pwd":"Passw0rd","operation":"unconfigure"}'
```

## Contributing Code

This section provides a set of guidelines for contributing code. The procedure outlined below requires you to be a repository collaborator. To be added as a collaborator, contact a [repository moderator](AUTHORS.md).

### Identifying an Issue

All code contributions must be associated with a [GitHub Issue](https://guides.github.com/features/issues).

1. Identify an issue you would like to contribute code to. This can be achieved by:
    1. searching for [open issues](https://github.ibm.com/ibm-security/pyisva/issues), or
    2. create a new [bug report](#reporting-bugs) or [enhancement request](#suggesting-enhancements).
2. Assign yourself to the issue so others know you are working on it.

### Submitting Code Changes

1. [Clone the repository](https://help.github.com/articles/cloning-a-repository) to your local environment. Additional information: [cloning with SSH URLs](https://help.github.com/articles/which-remote-url-should-i-use/#cloning-with-ssh-urls).
2. [Create a branch](https://guides.github.com/introduction/flow) to contain your changes. Branch names should be descriptive.
3. Make your changes. *Add yourself to the [list of authors](AUTHORS.md), if not already.*
4. [Push your branch](https://help.github.com/articles/pushing-to-a-remote) to the remote GitHub repository.
5. Create a [GitHub Pull Request](https://help.github.com/articles/creating-a-pull-request) against the repository's `master` branch.

### Pull Requests

- Use a short and descriptive title to identify the GitHub Pull Request.
- Describe the purposed changes in sufficient detail. This helps the reviewer understand the direction you have taken and the reasoning behind it.
- Include appropriate [keyword and issue references](https://help.github.com/articles/closing-issues-via-commit-messages) in the GitHub Pull Request body to have the associated issue automatically closed when the GitHub Pull Request is merged.

### Code Reviews

Contributions will not be merged until a code review has been completed. Code reviews are handled within the GitHub Pull Request and must be completed by a [repository moderator](AUTHORS.md). Code review feedback must be implemented unless objected to, in which case an alternative must be devised or the contribution withdrawn.

### Deleting Branches

The moderator will delete the branch after merging **IF** the GitHub Pull Request automatically closes the GitHub Issue; refer to [Pull Requests](#pull-requests). This ensures the repository is kept in the most clean state at all times. Under the circumstances that the GitHub Issue **IS NOT** automatically closed, it is the responsibility of the person contributing the changes to both close the issue and delete the branch.

## Style Guides

### Git Commit Messages

- The first line must be a summary of changes
- The remaining text must be a detailed description of the changes
- Use the imperative, present tense: "Change" not "Changed"
- Limit each line to 72 characters or less

### Python Style Guide

Python code should be written with the guidance of [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008).

Additional guidelines include:
- *To be documented...*

### Documentation Style Guide

*To be documented...*
