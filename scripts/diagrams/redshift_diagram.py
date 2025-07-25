#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Redshift, Athena, Quicksight, EMR
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM, KMS
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Redshift Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/redshift"):
    
    # Data sources
    with Cluster("Data Sources"):
        s3_datalake = S3("S3 Data Lake")
        rds_oltp = RDS("OLTP Systems")
        dynamodb_nosql = Dynamodb("DynamoDB")
        streaming_data = Lambda("Streaming Data")
        external_data = Lambda("External Sources")
    
    # ETL and data preparation
    with Cluster("ETL & Data Preparation"):
        glue_etl = Lambda("AWS Glue ETL")
        emr_processing = EMR("EMR Processing")
        lambda_transform = Lambda("Lambda Transform")
        data_pipeline = Lambda("Data Pipeline")
    
    # Redshift cluster
    with Cluster("Amazon Redshift Cluster"):
        leader_node = Redshift("Leader Node")
        compute_node1 = Redshift("Compute Node 1")
        compute_node2 = Redshift("Compute Node 2")
        compute_node3 = Redshift("Compute Node 3")
    
    # Redshift features
    with Cluster("Redshift Features"):
        materialized_views = Lambda("Materialized Views")
        result_caching = Lambda("Result Caching")
        concurrency_scaling = Lambda("Concurrency Scaling")
        federated_queries = Lambda("Federated Queries")
    
    # Analytics and BI
    with Cluster("Analytics & BI Tools"):
        quicksight_bi = Quicksight("QuickSight")
        tableau = Users("Tableau")
        jupyter_notebooks = Spark("Jupyter Notebooks")
        custom_apps = Lambda("Custom Applications")
    
    # Data consumers
    with Cluster("Data Consumers"):
        business_analysts = Users("Business Analysts")
        data_scientists = Users("Data Scientists")
        executives = Users("Executives")
        automated_reports = Lambda("Automated Reports")
    
    # Security and monitoring
    with Cluster("Security & Monitoring"):
        iam_access = IAM("IAM Access Control")
        kms_encryption = KMS("KMS Encryption")
        cloudwatch_metrics = Cloudwatch("CloudWatch")
        audit_logging = Lambda("Audit Logging")
    
    # Data loading connections
    s3_datalake >> Edge(label="COPY Command") >> leader_node
    rds_oltp >> Edge(label="ETL") >> glue_etl
    dynamodb_nosql >> Edge(label="Export") >> glue_etl
    streaming_data >> Edge(label="Batch Load") >> data_pipeline
    external_data >> Edge(label="Import") >> lambda_transform
    
    # ETL to Redshift
    glue_etl >> Edge(label="Processed Data") >> s3_datalake
    emr_processing >> Edge(label="Big Data") >> s3_datalake
    lambda_transform >> Edge(label="Transformed") >> s3_datalake
    data_pipeline >> Edge(label="Scheduled Load") >> leader_node
    
    # Redshift cluster architecture
    leader_node >> Edge(label="Distribute Queries") >> compute_node1
    leader_node >> Edge(label="Distribute Queries") >> compute_node2
    leader_node >> Edge(label="Distribute Queries") >> compute_node3
    
    # Redshift features integration
    leader_node >> Edge(label="Optimize") >> materialized_views
    leader_node >> Edge(label="Cache") >> result_caching
    leader_node >> Edge(label="Scale") >> concurrency_scaling
    leader_node >> Edge(label="Federate") >> federated_queries
    
    # Federated query connections
    federated_queries >> Edge(label="Query") >> s3_datalake
    federated_queries >> Edge(label="Query") >> rds_oltp
    
    # Analytics tool connections
    leader_node >> Edge(label="SQL Queries") >> quicksight_bi
    leader_node >> Edge(label="JDBC/ODBC") >> tableau
    leader_node >> Edge(label="Python/R") >> jupyter_notebooks
    leader_node >> Edge(label="API") >> custom_apps
    
    # User access through tools
    business_analysts >> Edge(label="Dashboards") >> quicksight_bi
    data_scientists >> Edge(label="Analysis") >> jupyter_notebooks
    executives >> Edge(label="Reports") >> tableau
    automated_reports >> Edge(label="Scheduled") >> custom_apps
    
    # Security and monitoring
    leader_node >> Edge(label="Authenticate") >> iam_access
    leader_node >> Edge(label="Encrypt") >> kms_encryption
    leader_node >> Edge(label="Monitor") >> cloudwatch_metrics
    leader_node >> Edge(label="Audit") >> audit_logging
    
    # Cross-service integrations
    materialized_views >> Edge(label="Refresh") >> cloudwatch_metrics
    concurrency_scaling >> Edge(label="Auto Scale") >> cloudwatch_metrics

print("Redshift diagram generated successfully!")
