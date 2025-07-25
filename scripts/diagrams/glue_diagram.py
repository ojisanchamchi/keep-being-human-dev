#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Glue, GlueCrawlers, GlueDataCatalog, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Redshift, Dynamodb
from diagrams.aws.integration import SQS, SNS, StepFunctions
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.database import MySQL

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("AWS Glue Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/glue",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        s3_raw = S3("Raw Data")
        rds_db = RDS("RDS Database")
        mysql_db = MySQL("On-premises DB")
        dynamodb_table = Dynamodb("DynamoDB")
        streaming_data = SQS("Streaming Data")
    
    with Cluster("AWS Glue Services"):
        glue_service = Glue("AWS Glue")
        
        with Cluster("Core Components"):
            crawlers = GlueCrawlers("Glue Crawlers")
            data_catalog = GlueDataCatalog("Data Catalog")
            etl_jobs = Glue("ETL Jobs")
            workflows = StepFunctions("Glue Workflows")
    
    with Cluster("Job Execution"):
        spark_jobs = Glue("Spark ETL Jobs")
        python_shell = Lambda("Python Shell Jobs")
        streaming_jobs = Glue("Streaming Jobs")
        ray_jobs = Glue("Ray Jobs")
    
    with Cluster("Data Targets"):
        s3_processed = S3("Processed Data")
        redshift_dw = Redshift("Data Warehouse")
        analytics_db = RDS("Analytics DB")
        data_lake = S3("Data Lake")
    
    with Cluster("Analytics Integration"):
        athena = Athena("Athena")
        quicksight = Glue("QuickSight")
        sagemaker = Lambda("SageMaker")
    
    with Cluster("Orchestration & Monitoring"):
        step_functions = StepFunctions("Step Functions")
        cloudwatch = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        security = IAM("IAM Roles")
    
    # Data discovery flow
    s3_raw >> crawlers
    rds_db >> crawlers
    mysql_db >> crawlers
    dynamodb_table >> crawlers
    
    crawlers >> data_catalog
    
    # ETL processing
    glue_service >> etl_jobs
    etl_jobs >> spark_jobs
    etl_jobs >> python_shell
    etl_jobs >> streaming_jobs
    etl_jobs >> ray_jobs
    
    # Data consumption from catalog
    data_catalog >> etl_jobs
    data_catalog >> athena
    
    # Data transformation flow
    s3_raw >> spark_jobs >> s3_processed
    rds_db >> python_shell >> redshift_dw
    streaming_data >> streaming_jobs >> data_lake
    
    # Workflow orchestration
    workflows >> etl_jobs
    step_functions >> workflows
    
    # Analytics integration
    s3_processed >> athena
    redshift_dw >> quicksight
    data_lake >> sagemaker
    
    # User interaction
    users >> Edge(label="Develop Jobs") >> glue_service
    users >> Edge(label="Monitor") >> cloudwatch
    users >> Edge(label="Query Data") >> athena
    
    # Monitoring and security
    etl_jobs >> cloudwatch
    cloudwatch >> notifications
    security >> glue_service

print("AWS Glue diagram generated successfully!")
