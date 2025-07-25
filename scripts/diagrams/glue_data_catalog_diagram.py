#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import GlueDataCatalog, GlueCrawlers, Athena, EMR
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Redshift, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("AWS Glue Data Catalog Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/glue-data-catalog",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Analysts")
    
    with Cluster("Data Sources"):
        s3_data_lake = S3("Data Lake")
        rds_db = RDS("RDS Database")
        redshift_dw = Redshift("Data Warehouse")
        dynamodb_table = Dynamodb("DynamoDB")
    
    with Cluster("Metadata Discovery"):
        crawlers = GlueCrawlers("Glue Crawlers")
        manual_entry = Lambda("Manual Entry")
        api_import = Lambda("API Import")
    
    with Cluster("Data Catalog Core"):
        data_catalog = GlueDataCatalog("Glue Data Catalog")
        
        with Cluster("Catalog Structure"):
            databases = GlueDataCatalog("Databases")
            tables = GlueDataCatalog("Tables")
            partitions = GlueDataCatalog("Partitions")
            connections = GlueDataCatalog("Connections")
    
    with Cluster("Analytics Services"):
        athena = Athena("Athena")
        emr_cluster = EMR("EMR")
        spark_jobs = Spark("Spark Jobs")
        etl_jobs = Lambda("Glue ETL")
    
    with Cluster("Data Governance"):
        data_lineage = GlueDataCatalog("Data Lineage")
        classification = GlueDataCatalog("Data Classification")
        security_tags = IAM("Security Tags")
    
    with Cluster("Monitoring & Events"):
        cloudwatch = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        event_queue = SQS("Event Queue")
    
    # Metadata discovery flow
    s3_data_lake >> crawlers
    rds_db >> crawlers
    redshift_dw >> crawlers
    dynamodb_table >> crawlers
    
    crawlers >> Edge(label="Discover Schema") >> data_catalog
    manual_entry >> Edge(label="Manual Input") >> data_catalog
    api_import >> Edge(label="API Import") >> data_catalog
    
    # Catalog structure
    data_catalog >> databases
    data_catalog >> tables
    data_catalog >> partitions
    data_catalog >> connections
    
    # Analytics consumption
    data_catalog >> Edge(label="Schema Info") >> athena
    data_catalog >> Edge(label="Metadata") >> emr_cluster
    data_catalog >> Edge(label="Table Definitions") >> spark_jobs
    data_catalog >> Edge(label="ETL Metadata") >> etl_jobs
    
    # Data governance
    data_catalog >> data_lineage
    data_catalog >> classification
    data_catalog >> security_tags
    
    # User interaction
    users >> Edge(label="Search & Browse") >> data_catalog
    users >> Edge(label="Query Data") >> athena
    users >> Edge(label="Run Analytics") >> emr_cluster
    
    # Monitoring and events
    data_catalog >> Edge(label="Metadata Events") >> cloudwatch
    cloudwatch >> notifications
    data_catalog >> event_queue

print("Glue Data Catalog diagram generated successfully!")
