# Infrastructure

Deployment and submission artifacts for Assignment 3.

- `cloudformation-template.yaml`: basic template for both S3 buckets, both Lambdas, API Gateway, IAM roles, CORS, and API key resources.
- `openapi.yaml`: Swagger-style API documentation for the implemented `/search` and `/photos/{object}` API.
- `buildspec-backend.yml`: CodeBuild commands for a backend CodePipeline.
- `buildspec-frontend.yml`: CodeBuild commands for a frontend CodePipeline.
- `deployment-guide.md`: AWS deployment steps for Lambda updates, frontend hosting, CloudFormation, and CodePipeline.
- `backend-deployment-checklist.md`: original backend deployment checklist.
- `team-handoff.md`: current deployed backend notes from the teammate.
