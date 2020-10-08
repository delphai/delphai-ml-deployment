# ml-deployment-action


<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/scottydocs/README-template.md)
![GitHub contributors](https://img.shields.io/github/contributors/scottydocs/README-template.md)

Ml-deployment-action is a pipeline that allows Ml team to train, deploy and test the models.

This is a GitHub Action can be a full pipeline or a part of pipeline
## Prerequisites

Before you begin, ensure you have met the following requirements:
<!--- These are just example requirements. Add, duplicate or remove as required --->
* You have the workflow file from the [boilerplate](https://github.com/delphai/delphai-boilerplate)

## How it works
**Training**

A VM will be created by executing some Terraform commands on Azure Cloud.
The Model will be cloned in the vm and downloads with it the training data from Azure Blob.
Training runs in the vm until it finishes.
The register directory will be also cloned in the vm after and gets executed to register the model in Azure 

**Note**

The wished training model must in in a directory called [model] in the root of the repo.
```
.
├── model
│   └── dont_delete.txt
├── register.sh
└── src
    ├── conda.yml
    ├── entry.py
    ├── register.py
    └── train.py
```


**Deploying**

Deployment will happen to delphai's Clusters through src/train.py **only if train was marked as yes**.

## How to use this pipeline 


``` yaml
# ml-deployment.yml
name: ML Deployment

on:
  push:
    branches:
      - "master"
jobs:
  Deploy_ML:

    runs-on: ubuntu-latest
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - name: checkout repo
      uses: actions/checkout@v2
    - run: echo ::set-env name=REPOSITORY_NAME::$(echo "$GITHUB_REPOSITORY" | awk -F / '{print $2}' | sed -e "s/:refs//")
      shell: bash

    - name: deploy and train 
      uses: delphai/delphai-ml-deployment@<VERSION OR BRANCH>
      with:
        # Choose Jobs 
        train            : 'yes' or 'no'
        deploy           : 'yes' or 'no'
        # Fill please
        model_name       : "<model_name>"
        model_version    : "<version_number>"
        deployment_name  : ${{ env.REPOSITORY_NAME }}
        # Optional 
        replicas         : "3"
        entry_file       : "entry.py"
        conda_file       : "conda.yml"
        #source_dir       : "<if your source file is not src in the root >"
        # DevOps 
        azure_credentials: ${{ secrets.AZURE_CREDENTIALS_ML }}
        namespace        : "azureml-delphai-development"
        resource_group   : "machine-learning"
        workspace        : "delphai-development"
        compute_target   : "delphai-ml"

```


## Contributing
<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->
To contribute, follow these steps:


1. Create a branch: `git checkout -b <branch_name>`.
2. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

* [@ahmedmahmo](https://github.com/ahmedmahmo) 📖
