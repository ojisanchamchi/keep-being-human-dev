#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import DataLakeResource, Glue, Athena, EMR, Kinesis
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Data Lake Resource Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/data-lake-resource",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Scientists")
    
    with Cluster("Data Ingestion"):
        rds = RDS("Operational DB")
        dynamodb = Dynamodb("NoSQL DB")
        kinesis = Kinesis("Streaming Data")
        batch_data = S3("Batch Files")
    
    with Cluster("Data Lake Storage"):
        raw_zone = S3("Raw Zone")
        processed_zone = S3("Processed Zone")
        curated_zone = S3("Curated Zone")
    
    with Cluster("Data Lake Resources"):
        data_lake = DataLakeResource("Data Lake\nResources")
        catalog = Glue("Data Catalog")
        etl_jobs = Glue("ETL Jobs")
    
    with Cluster("Processing & Analytics"):
        emr_cluster = EMR("EMR Cluster")
        lambda_fn = Lambda("Lambda Functions")
        athena = Athena("Query Engine")
        ml_model = SagemakerModel("ML Models")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Policies")
        queue = SQS("Processing Queue")
    
    # Data ingestion flow
    rds >> Edge(label="CDC") >> kinesis
    dynamodb >> Edge(label="Streams") >> kinesis
    batch_data >> raw_zone
    kinesis >> raw_zone
    
    # Data processing flow
    raw_zone >> data_lake
    data_lake >> etl_jobs >> processed_zone
    processed_zone >> data_lake >> curated_zone
    
    # Analytics flow
    curated_zone >> catalog >> athena
    curated_zone >> emr_cluster
    curated_zone >> ml_model
    
    # User interaction
    users >> Edge(label="Queries") >> athena
    users >> Edge(label="Jobs") >> emr_cluster
    users >> Edge(label="Training") >> ml_model
    
    # Monitoring and security
    data_lake >> Edge(label="Metrics") >> monitoring
    security >> Edge(label="Access Control") >> data_lake
    lambda_fn >> queue >> data_lake

print("Data Lake Resource diagram generated successfully!")
