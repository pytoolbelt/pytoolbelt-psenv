# Configuration Reference

This page provides detailed information about the `psenv.yml` configuration file, which is the central configuration for your PSEnv environment.

## Overview

The `psenv.yml` file defines:

- Default environment file location
- Parameter Store path structure
- AWS environment configurations
- Environment-specific settings

## File Structure

A typical `psenv.yml` file has the following structure:

```yaml
envfile: .env
root_path: /my-app
kms_key: alias/aws/ssm
environments:
  - name: dev
    account: "123456789012"
    envfile: .env.dev
  - name: test
    account: "123456789012"
    envfile: .env.test
  - name: prod
    account: "987654321098"
    envfile: .env.prod
```

## Configuration Options

### Top-Level Options

| Option | Description | Default | Required |
| ------ | ----------- | ------- | -------- |
| `envfile` | Default .env file location | `.env` | Yes |
| `root_path` | Root path for Parameter Store parameters | `/` | Yes |
| `kms_key` | KMS key for parameter encryption | `alias/aws/ssm` | No |
| `environments` | List of environment configurations | - | Yes |

### Environment Options

Each entry in the `environments` list supports the following options:

| Option | Description | Default | Required |
| ------ | ----------- | ------- | -------- |
| `name` | Environment name (e.g., dev, prod) | - | Yes |
| `account` | AWS account ID for this environment | - | Yes |
| `envfile` | Environment-specific .env file location | Inherits from top-level `envfile` | No |
| `parameter_path` | Environment-specific parameter path | `{root_path}/{name}` | No |
| `kms_key` | Environment-specific KMS key | Inherits from top-level `kms_key` | No |

## Parameter Path Structure

By default, parameters are stored in Parameter Store using the following path structure:

```
{root_path}/{environment_name}/{parameter_name}
```

For example, with `root_path: /my-app` and environment `dev`, the parameter `DATABASE_URL` would be stored at:

```
/my-app/dev/DATABASE_URL
```

## Example Configurations

### Basic Configuration

```yaml
envfile: .env
root_path: /my-app
environments:
  - name: dev
    account: "123456789012"
  - name: prod
    account: "987654321098"
```

### Multi-Environment Configuration with Custom Files

```yaml
envfile: .env
root_path: /my-app
environments:
  - name: dev
    account: "123456789012"
    envfile: .env.development
  - name: test
    account: "123456789012"
    envfile: .env.test
  - name: stage
    account: "567890123456"
    envfile: .env.staging
  - name: prod
    account: "987654321098"
    envfile: .env.production
```

### Configuration with Custom KMS Keys

```yaml
envfile: .env
root_path: /my-app
kms_key: alias/my-app-default-key
environments:
  - name: dev
    account: "123456789012"
  - name: prod
    account: "987654321098"
    kms_key: alias/my-app-prod-key
```

### Configuration with Custom Parameter Paths

```yaml
envfile: .env
root_path: /my-app
environments:
  - name: dev
    account: "123456789012"
    parameter_path: /development/my-app
  - name: prod
    account: "987654321098"
    parameter_path: /production/my-app
```

## Best Practices

1. **Use consistent naming**: Keep environment names consistent (dev, test, prod) throughout your organization.

2. **Use specific environment files**: Define environment-specific .env files (like `.env.dev`, `.env.prod`) to avoid accidentally mixing parameters from different environments.

3. **Validate AWS accounts**: Always double-check AWS account IDs to ensure you're targeting the correct account for each environment.

4. **Parameter path organization**: Structure your parameter paths logically, typically organizing by application and environment.

5. **KMS key management**: For production environments, consider using a dedicated KMS key with stricter access controls.

## Creating or Updating the Configuration

You can create a new configuration file using the init command:

```bash
psenv config init
```

This will create a template `psenv.yml` file in your current directory that you can customize to your needs.
