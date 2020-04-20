# AI Platform Notebooks via Terraform installation 

Create an AI Platform Notebooks in GCP via Terraform. This will deploy a
AI Platform Notebooks instance.

## Prerequisites

* Terraform 0.12+ 

```bash
 terraform -v
```

* Google Cloud account

## Installation

1. Clone the repository.
```bash
git clone https://github.com/GoogleCloudPlatform/ai-platform-samples.git
cd ai-platform-samples/notebooks/tools/terraform
``` 

2. Modify your variables 
Modify [variables.tf](variables.tf) and setup Google Cloud Project and
instance specific settings.


3. Deploy instance using Terraform

Initialize configuration
```bash
 terraform init 
```
Validate configuration
```bash
 terraform plan 
```
Deploy instance

```bash
 terraform apply
```

## References

https://cloud.google.com/community/tutorials/getting-started-on-gcp-with-terraform
