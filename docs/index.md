# PSEnv

A tool for managing AWS Parameter Store environments.

## Overview

PSEnv is a command-line tool that simplifies the management of environment variables across different AWS environments using Parameter Store. It provides an easy way to:

- Synchronize local `.env` files with AWS Parameter Store
- Pull parameters from AWS and update your local environment
- Execute commands with parameters from AWS injected into the environment
- Support multiple AWS environments (development, testing, production)

## Installation

```bash
pip install psenv
```

## Quick Start

```bash
# Initialize a new psenv configuration
psenv config init

# Get parameters from Parameter Store
psenv get --env dev

# Put parameters to Parameter Store
psenv put --env dev --sync

# Execute a command with environment variables from Parameter Store
psenv exec --env dev -- npm start
```

See the [Getting Started](getting-started.md) guide for more detailed instructions.
