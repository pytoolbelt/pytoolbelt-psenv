# Command Reference

This page provides detailed information about all PSEnv commands, their options, and usage examples.

## Global Options

These options are available for most commands:

- `--env`: Specify the environment to work with (e.g., dev, prod)
- `--config`: Path to the psenv.yml configuration file (defaults to ./psenv.yml)

## Command: `get`

Retrieves parameters from AWS Parameter Store and updates your local .env file.

### Usage

```bash
psenv get --env <environment>
```

### Options

- `--env`: Required. The environment to get parameters for.

### Examples

```bash
# Get parameters for the dev environment
psenv get --env dev

# Get parameters using a specific config file
psenv get --env prod --config /path/to/psenv.yml
```

## Command: `put`

Puts parameters from your local .env file into AWS Parameter Store.

### Usage

```bash
psenv put --env <environment> [--add|--update|--sync] [--dry-run]
```

### Options

- `--env`: Required. The environment to put parameters for.
- `--add`: Add new parameters only, without modifying existing ones.
- `--update`: Add new parameters and update existing ones.
- `--sync`: Add new, update existing, and remove parameters not in the local file.
- `--dry-run`: Show what would be done without making any changes.

### Examples

```bash
# Add new parameters only
psenv put --env dev --add

# Update existing parameters and add new ones
psenv put --env dev --update

# Fully synchronize (add, update, delete)
psenv put --env dev --sync

# Preview changes without applying them
psenv put --env dev --sync --dry-run
```

## Command: `exec`

Execute a command with environment variables from Parameter Store.

### Usage

```bash
psenv exec --env <environment> -- <command> [arguments]
```

> **Important**: You do not need the .env file locally to run a command with `exec`. The parameters will be pulled directly from AWS Parameter Store.

### Options

- `--env`: Required. The environment to get parameters from.
- `--`: Separates psenv options from the command to execute.

### Examples

```bash
# Run a Node.js application with dev environment variables
psenv exec --env dev -- node server.js

# Run a Docker container with prod environment variables
psenv exec --env prod -- docker-compose up

# Run a Python script with test environment variables
psenv exec --env test -- python process_data.py
```

## Command: `inject`

Inject environment variables from your current shell session into a .env file.

### Usage

```bash
psenv inject [--prefix <prefix>]
```

### Options

- `--prefix`: Filter environment variables by prefix.

### Examples

```bash
# Inject all environment variables
psenv inject

# Inject only AWS_* environment variables
psenv inject --prefix AWS_
```

## Command: `init`

Initialize a psenv project by creating a configuration file and environment directory structure.

### Usage

```bash
psenv init
```

### Options

No specific options for this command.

### Examples

```bash
# Initialize a new psenv project
psenv init
```

## Best Practices

PSEnv is designed with the following workflow in mind:

1. **Use .env files for synchronization only**: The .env files are intended as temporary synchronization points between your local environment and Parameter Store, not for long-term local storage.

2. **Prefer `exec` for running commands**: Rather than sourcing .env files in your shell, use `psenv exec` to run commands with the environment variables loaded directly from Parameter Store.

3. **Use `put` with `--sync` for complete synchronization**: When updating parameters, the `--sync` option ensures that your Parameter Store state exactly matches your local .env file.

4. **Preview changes with `--dry-run`**: Before making changes to Parameter Store, use the `--dry-run` flag to preview what would be added, updated, or removed.
