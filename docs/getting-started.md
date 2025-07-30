# Getting Started with PSEnv

This guide will help you get up and running with PSEnv to manage your AWS Parameter Store environments.

## Prerequisites

- Python 3.10 or higher
- AWS credentials configured locally
- AWS account with permissions to access Parameter Store

## Installation

Install PSEnv using pip:

```bash
pip install psenv
```

## Initial Setup

1. Create a PSEnv configuration file:

   ```bash
   psenv config init
   ```

   This will create a `psenv.yml` file in your current directory.

2. Edit the configuration file to match your AWS environment structure:

   ```yaml
   envfile: .env
   root_path: /your-app
   environments:
     - name: dev
       account: "123456789012"
       envfile: .env.dev
     - name: prod
       account: "987654321098"
       envfile: .env.prod
   ```

3. Make sure your AWS credentials are properly configured for accessing the accounts defined in your configuration.

## Basic Usage

### Pull Parameters from AWS

```bash
psenv get --env dev
```

This will fetch parameters from the Parameter Store path specified in your configuration and save them to your `.env.dev` file.

### Push Parameters to AWS

```bash
psenv put --env dev --sync
```

This will sync your local `.env.dev` file with the Parameter Store.

### Execute Commands with Parameters

```bash
psenv exec --env dev -- npm start
```

This will run the command `npm start` with environment variables loaded from Parameter Store.

## Next Steps

Check out the detailed documentation on:

- [Configuration Options](usage/configuration.md)
- [Command Reference](usage/commands.md)
