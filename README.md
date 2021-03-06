# Cloudsmith Command Line Interface (CLI)

[![Python Versions](https://img.shields.io/pypi/pyversions/cloudsmith-cli.svg)](https://pypi.python.org/pypi/cloudsmith-cli)
[![PyPI Version](https://img.shields.io/pypi/v/cloudsmith-cli.svg)](https://pypi.python.org/pypi/cloudsmith-cli)
[![Travis](https://travis-ci.org/cloudsmith-io/cloudsmith-cli.svg?branch=master)](https://travis-ci.org/cloudsmith-io/cloudsmith-cli)
[![Codecov](https://codecov.io/gh/cloudsmith-io/cloudsmith-cli/branch/master/graph/badge.svg?branch=master)](https://codecov.io/gh/cloudsmith-io/cloudsmith-cli)
[![Gemnasium](https://gemnasium.com/badges/github.com/cloudsmith-io/cloudsmith-cli.svg)](https://gemnasium.com/github.com/cloudsmith-io/cloudsmith-cli)
[![Codacy](https://api.codacy.com/project/badge/Grade/7ce010a44fd249329dab8959ca09142a)](https://www.codacy.com/app/Cloudsmith/cloudsmith-cli)

The [Cloudsmith](https://cloudsmith.io) Command Line Interface (CLI) is a Py2/Py3 text-based interface to the [API](https://api.cloudsmith.io). This allows users, machines and other services to access and integrate smoothly with Cloudsmith without requiring explicit plugins or tools. Be awesome. [Automate Everything](https://corp.cloudsmith.io/tao/).

The following (slightly out of date) GIF demonstrates a small slice of the CLI - [View the full video on YouTube](https://youtu.be/8nlstYU9J5M):

[![CLI Demonstration](https://user-images.githubusercontent.com/2248287/33522274-c88416be-d7e0-11e7-86ab-518c53d6bf61.gif)](https://youtu.be/8nlstYU9J5M)

You can also read our [blog article](https://blog.cloudsmith.io/2017/11/25/automation-as-simple-as-a-b-cli/) that introduced the first version of the CLI and the Cloudsmith RESTful API.


## Changelog

Please see the [changelog](https://github.com/cloudsmith-io/cloudsmith-cli/blob/master/CHANGELOG.md) for the list of changes by version. The current version is displayed in the PyPi badge at the top.


## Features

The CLI currently supports the following commands (and sub-commands):

- `check`:  Check the status/version of the service.
- `delete`: Delete a package from a repository.
- `docs`:   Launch the help website in your browser.
- `help`:   Display the help message and exit.
- `list`:   List distributions, packages and repos.
  - `distros`:  List available distributions.
  - `packages`: List packages for a repository.
  - `repos`:    List repositories for a namespace (owner).
- `push`:   Push/upload a new package to a repository.
  - `deb`:     Push/upload a new Deb package upstream.
  - `maven`:   Push/upload a new Maven package upstream.
  - `python`:  Push/upload a new Python package upstream.
  - `raw`:     Push/upload a new Raw package upstream.
  - `rpm`:     Push/upload a new Rpm package upstream.
  - `ruby`:    Push/upload a new Ruby package upstream.
  - `vagrant`: Push/upload a new Vagrant package upstream.
- `status`: Get the synchronisation status for a package.
- `token`:  Retrieve your API authentication token/key.
- `whoami`: Retrieve your current authentication status.


## Installation

You can install the latest CLI application from:

- [Official CLI Repository @ PyPi](https://pypi.python.org/pypi/cloudsmith-cli)
- [Official CLI Repository @ Cloudsmith](https://cloudsmith.io/package/ns/cloudsmith/repos/cli/packages/)

The simplest way is to use `pip`, such as:

```
pip install --upgrade cloudsmith-cli
```

Or you can get the latest pre-release version from Cloudsmith:

```
pip install --upgrade cloudsmith-cli --extra-index-url=https://dl.cloudsmith.io/public/cloudsmith/cli/python/index/
```

## Configuration

There are two configuration files used by the CLI:

- `config.ini`: For non-credentials configuration.
- `credentials.ini`: For credentials (authentication) configuration.

By default, the CLI will look for these in the following locations:

- The current working directory.
- A directory called `cloudsmith` in the OS-defined application directory. For example:
  - Linux: `$HOME/.config/cloudsmith`
    - Windows: `C:\Users\YourName\AppData\cloudsmith`

Both configuration files use the simple INI format, such as:

```
[default]
api_key=1234567890abcdef1234567890abcdef
```

### Non-Credentials (config.ini)

See the [default config](https://raw.githubusercontent.com/cloudsmith-io/cloudsmith-cli/master/cloudsmith/data/config.ini) in GitHub:

You can specify the following configuration options:

- `api_host`: The API host to connect to.
- `api_proxy`: The API proxy to connect through.
- `api_user_agent`: The user agent to use for requests.

### Credentials (credentials.ini)

See the [default config](https://raw.githubusercontent.com/cloudsmith-io/cloudsmith-cli/master/cloudsmith/data/credentials.ini) in GitHub:

You can specify the following configuration options:

- `api_key`: The API key for authenticating with the API.


### Getting Your API Key

You'll need to provide authentication to Cloudsmith for any CLI actions that result in accessing private data or making changes to resources (such as pushing a new package to a repository)..

With the CLI this is simple to do. You can retrieve your API key using the `cloudsmith token` command:

```
cloudsmith token
Login: you@example.com
Password:
Repeat for confirmation:
```

*Note:* Please ensure you use your email for the 'Login' prompt and not your user slug/identifier.

The resulting output looks something like:

```
Retrieving API token for 'you@example.com' ... OK
Your API token is: 1234567890abcdef1234567890abcdef
```

Once you have your API key you can then put this into your `credentials.ini`, use it as an environment variable `export CLOUDSMITH_API_KEY=your_key_here` or pass it to the CLI using the `-k your_key_here` flag.

For convenience the CLI will ask you if you want to install the default configuration files, complete with your API key, if they don't already exist. Say 'y' or 'yes' to create the configuration files.

If the configuration files already exist, you'll have to manually put the API key into the configuration files, but the CLI will print out their locations.


## Examples

**Note:** All of the examples in this section are uploading to the **lskillen** user and the **test** repository. Please replace these with your own user/org and repository names.

### Upload a Debian Package

Assuming you have a package filename **libxml2-2.9.4-2.x86_64.deb**, representing **libxml 2.9.4**, for the **Ubuntu 16.04** distribution (which has a cloudsmith identifier of **ubuntu/xenial**):

```
cloudsmith push deb lskillen/test/ubuntu/xenial libxml2-2.9.4-2.x86_64.deb
```

### Upload a RedHat Package

Assuming you have a package filename **libxml2-2.9.4-2.el5.x86_64.rpm**, representing **libxml 2.9.4**, for the **RedHat Enterprise 5.0** distribution (which has a cloudsmith identifier of **el/5**):

```
cloudsmith push rpm lskillen/test/el/5 libxml2-2.9.4-2.el5.x86_64.rpm
```

### Upload a Python Package

Assuming you have a package filename **boto3-1.4.4.py2.p3-none-any.whl**, representing **boto3 1.4.4**, for **Python 2/3**:

```
cloudsmith push python lskillen/test boto3-1.4.4.py2.p3-none-any.whl
```

### Upload a Ruby Package

Assuming you have a package filename **safe_yaml-1.0.4.gem**, representing **safe_yaml 1.0.4**, for **Ruby 2.3+**:

```
cloudsmith push ruby lskillen/test safe_yaml-1.0.4.gem
```

### Upload a Maven Package

Assuming you have a package filename **validation-api-1.0.0.GA.jar**, representing **validation-api 1.0.0**, for **Maven/Java**:

```
cloudsmith push maven lskillen/test validation-api-1.0.0.GA.jar --pom-file=validation-api-1.0.0.GA.pom
```

### Upload a Raw Package

Assuming you have a package filename **assets.zip**, representing **packaged assets**:

```
cloudsmith push raw lskillen/test assets.zip
```

### Upload a Vagrant Package

Assuming you have a package filename **awesome.box**, representing a Vagrant image for the **Awesome OS** (fictional, probably):

```
cloudsmith push vagrant lskillen/test awesome.box
```

### Upload multiple Debian Packages

You can also upload multiple packages in one go (all of the same distribution):

```
cloudsmith push deb lskillen/test/ubuntu/xenial libxml2-2.9.1-2.x86_64.deb libxml2-2.9.2-2.x86_64.deb libxml2-2.9.3-2.x86_64.deb
```

## Contributing

Yes! Please do contribute, this is why we love open source.  Please see [CONTRIBUTING](https://github.com/cloudsmith-io/cloudsmith-cli/blob/master/CONTRIBUTING.md) for contribution guidelines when making code changes or raising issues for bug reports, ideas, discussions and/or questions (i.e. help required).


## License

Copyright 2017 Cloudsmith Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


## EOF

This quality product was brought to you by [Cloudsmith](https://cloudsmith.io) and the [fine folks who have contributed](https://github.com/cloudsmith-io/cloudsmith-cli/blob/master/CONTRIBUTORS.md).
