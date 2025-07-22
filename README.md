### Network Security Project for Phising Data

### 📦 Dataset
📦 Dataset
The core dataset is stored in a MongoDB Atlas database. An ETL (Extract, Transform, Load) pipeline is used to process and load the data, which contains various features extracted from network traffic to be used for model training.
![Mongodb_Atlas_Collection_View](screenshots/mongodb_atlas_collection_view.png)


---

### 📊 Experiment Tracking & Versioning
We use MLflow for tracking experiments and DagsHub for versioning our code and data, and for comparing results.

## Single Experiment Run
Here is a view of a single experiment's details and metrics tracked in MLflow.
![Mlflow_Single_Run_Metrics](screenshots/mlflow_single_run_metrics.png)


## Comparing Experiments
DagsHub provides a powerful interface to compare different experiment runs side-by-side, helping us select the best-performing model.
![Dagshub_Experiment_Comparison](screenshots/dagshub_experiment_comparison.png)


---

### 🚀 Deployment & CI/CD
The project is deployed on AWS with a full CI/CD pipeline managed by GitHub Actions.

## Model Storage on S3
The trained model artifacts are stored in an AWS S3 bucket for persistence and versioning.
![s3-bucket-artifacts & final-model](screenshots/s3-bucket-artifacts%20&%20final-model.png)


## Successful CI/CD Pipeline
The GitHub Actions workflow automates the entire process from integration and delivery to final deployment.
![github-actions-successful-ci-cd](screenshots/github-actions-successful-ci-cd.png)


## EC2 Deployment Server
The application is served from an AWS EC2 instance.
![ec2-instance-details](screenshots/ec2-instance-details.png)


## Live API Endpoint
The final running application provides a FastAPI interface with interactive API documentation.
![fastapi-application](screenshots/fastapi-application.png)
![fastapi-application-running](screenshots/fastapi-application-running.png)

