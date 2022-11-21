# psenv -- (Parameter Store Environment)
### a cli tool for managing environments stored in the AWS parameter store

When working on teams with multiple developers, who may each have their own local development environment, 
it can be challenging to make sure that each environment has the same set of base parameter values in a `.env` 
file to get the base project up and running. It can be common that as a project grows over time, there can be 100s 
of environment variables which contain everything from project configuration values, to database connection strings, 
or even secret API keys and tokens. 

Sometimes developers may need to keep multiple `.env` files locally for different projects, each of which may have a 
different set of parameters. This can become quite difficult to manage across multiple medium to large size teams. 
This is where `psenv` comes in, to help those of us who are working within the AWS cloud ecosystem. 


## Getting Started
``pip install psenv``

However, since `psenv` works well as a globally available command, the preferred method of installation is to use `pipx`

``pipx install psenv --include-deps``

For those of you who are unfamiliar with `pipx`, it can be thought of as a "Homebrew for python applications".

Check out the amazing project here ---->>> https://pypa.github.io/pipx/docs/

### Initialization 
After installation, `psenv` needs to be initialized and configured. To speed this up you can run
```shell
psenv init
```

This will create a directory at ``~/.psenv`` and a config file at `~/.psenv/psenv.yml` as well as an environment file 
`~/.psenv/psenv.env`


### Setting Up An Environment
Open the `~/.psenv/psenv.yml` file in your editor of choice and make an entry.
```yaml
environments:
  my_project_name:
    path: /the/path/used/in-the/aws/parameter-store
    env: /path/to/local/env/file/.env

```
The `environments` key is a list, which can take as many environment definitions as you like.


## Commands
At any time you can type `psenv --help` for a list of commands.
```shell
psenv --help
psenv <command> --help
```


### Displaying Configured Environments
To display the environments configured 
```shell
psenv show
```
You should see a list of all available environments formatted in your terminal as a table. This can come in handy as we
will later need to reference the configured environments for the other commands


## Fetch an Environment from the AWS Parameter Store
This command will fetch all the parameters on the path configured in the ``path`` section of the `psenv.yml` file
```shell
psenv fetch --env my_project_name
```

## Push and Environment to the AWS Parameter Store
Sometimes you need to set up new environments. This is easy with `psenv`
add an entry in `psenv.yml`

```yaml
environments:
  new_env:
    path: /some/parameter-store/path
    env: /path/to/.env
```

populate the .env file with the secrets and parameters you need for your environment and then run
```shell
psenv push --env new_env
```

## Private Environment Variables
Sometimes a project my have some environment variable where the value is known up-front. (eg. Project Configs), however there
may be some values which need to remain secret. After all, it would not make much sense for a developer to store there personal
github token in the parameter store for others to copy and use. For this case we have the `#<private>` section in the `.env` file. 

All variables declared under the `#<private>` section in the `.env` file will be ignored automatically by `psenv`

### Credential Injection
Sometimes you might want to copy some environment variables from your current terminal session environment to a .env file.
Example when you use temp AWS credentials and need to load them into more than one project / environment. To do this, get your creds however you normally would
and then

```shell
psenv inject --prefix aws --env some_env
```

all your aws credentials will be injected to your .env file! Like Magic!

## Variable Templating
When configuring an environment to be shared, it is sometimes helpful to give developers hints as to what type of private
credentials will be needed to get the code to behave as expected. This is where templating comes in. 

`psenv` allows you to define a placeholder in your `.env` file using the prefix `PSENV__TEMPLATE__`that will be templated upon running the `fetch` command.
For example, we have a project that requires a github token, and we want to make this obvious for the next developer we onboard. In our source `.env` file, 
we simply declare a variable called `PSENV__TEMPLATE__GITHUB_TOKEN`. We then run `psenv push --env <your-env>` to push these values to the parameter store. 

```dotenv
SOME_VARIABLE1=123
SOME_VARIABLE2=234

PSENV__TEMPLATE__GITHUB_TOKEN=<REPLACE-WITH-YOUR-PERSONAL-GH-TOKEN>
```

The next developer we on-board simply needs to run `psenv fetch --env <your-env>` and the below will be created. 
```dotenv
SOME_VARIABLE1=123
SOME_VARIABLE2=234

#<private>
GITHUB_TOKEN=<REPLACE-WITH-YOUR-PERSONAL-GH-TOKEN>
```

If you would like to fetch the environment values without using the template function, you can pass the `--no-template` flag to the fetch
command, which will then fetch the raw parameters as they were created. This is useful if an admin needs to add, or remove some parameter
from an environment. 
