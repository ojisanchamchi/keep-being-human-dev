#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import GlueCrawlers, GlueDataCatalog, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch, CloudwatchEventTimeBased
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.database import MySQL

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("AWS Glue Crawlers Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/glue-crawlers",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        s3_raw = S3("Raw Data Lake")
        s3_processed = S3("Processed Data")
        rds_db = RDS("RDS Database")
        mysql_db = MySQL("On-premises DB")
        dynamodb_table = Dynamodb("DynamoDB Tables")
    
    with Cluster("Glue Crawlers"):
        crawlers = GlueCrawlers("Glue Crawlers")
        
        with Cluster("Crawler Types"):
            s3_crawler = GlueCrawlers("S3 Crawler")
            jdbc_crawler = GlueCrawlers("JDBC Crawler")
            dynamodb_crawler = GlueCrawlers("DynamoDB Crawler")
    
    with Cluster("Data Catalog"):
        data_catalog = GlueDataCatalog("Glue Data Catalog")
        
        with Cluster("Catalog Components"):
            databases = GlueDataCatalog("Databases")
            tables = GlueDataCatalog("Tables")
            partitions = GlueDataCatalog("Partitions")
    
    with Cluster("Scheduling & Triggers"):
        cloudwatch_events = CloudwatchEventTimeBased("CloudWatch Events")
        s3_events = S3("S3 Events")
        lambda_trigger = Lambda("Trigger Function")
        scheduler = SQS("Scheduler Queue")
    
    with Cluster("Analytics Integration"):
        athena = Athena("Athena Queries")
        etl_jobs = Lambda("ETL Jobs")
        ml_pipeline = Lambda("ML Pipeline")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        security = IAM("IAM Roles")
    
    # Data source connections
    s3_raw >> Edge(label="Crawl") >> s3_crawler
    s3_processed >> Edge(label="Crawl") >> s3_crawler
    rds_db >> Edge(label="JDBC") >> jdbc_crawler
    mysql_db >> Edge(label="JDBC") >> jdbc_crawler
    dynamodb_table >> Edge(label="Scan") >> dynamodb_crawler
    
    # Crawler orchestration
    crawlers >> s3_crawler
    crawlers >> jdbc_crawler
    crawlers >> dynamodb_crawler
    
    # Metadata creation
    s3_crawler >> Edge(label="Create Tables") >> data_catalog
    jdbc_crawler >> Edge(label="Create Tables") >> data_catalog
    dynamodb_crawler >> Edge(label="Create Tables") >> data_catalog
    
    # Catalog structure
    data_catalog >> databases
    data_catalog >> tables
    data_catalog >> partitions
    
    # Scheduling and triggers
    cloudwatch_events >> Edge(label="Schedule") >> crawlers
    s3_events >> lambda_trigger >> crawlers
    scheduler >> Edge(label="Queue Jobs") >> crawlers
    
    # Analytics consumption
    data_catalog >> athena
    data_catalog >> etl_jobs
    data_catalog >> ml_pipeline
    
    # User interaction
    users >> Edge(label="Configure") >> crawlers
    users >> Edge(label="Query Catalog") >> data_catalog
    users >> Edge(label="Run Analytics") >> athena
    
    # Monitoring and notifications
    crawlers >> Edge(label="Metrics") >> monitoring
    crawlers >> Edge(label="Alerts") >> notifications
    security >> Edge(label="Access Control") >> crawlers

print("Glue Crawlers diagram generated successfully!")
