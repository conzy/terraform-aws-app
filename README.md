# App

A module that encapsulates an app or service. With integration tests against a real AWS account via OIDC
auth.

Uses [terraform-python-testing-helper](https://github.com/GoogleCloudPlatform/terraform-python-testing-helper)
which works with pytest and can be used to create test fixtures which are real resources created by terraform
i.e we can execute the `init`, `plan` and `apply` phase and then assert that certain resources
are created with certain configuration. The teardown phase will then `destroy` the resources under test.

## TODO

Use the git commit sha / GitHub Actions run ID to namespace the resources under test.
