#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Athena, Glue, Quicksight
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Athena Data Analytics", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/athena-analytics",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Analysts")
    
    with Cluster("Data Sources"):
        rds = RDS("Operational DB")
        logs = S3("Application Logs")
        raw_data = S3("Raw Data")
    
    with Cluster("Data Lake"):
        s3_bronze = S3("Bronze Layer\n(Raw)")
        s3_silver = S3("Silver Layer\n(Cleaned)")
        s3_gold = S3("Gold Layer\n(Aggregated)")
    
    with Cluster("Analytics Services"):
        glue_catalog = Glue("Glue Data Catalog")
        athena = Athena("Athena Query Engine")
        quicksight = Quicksight("QuickSight BI")
    
    with Cluster("Automation"):
        lambda_etl = Lambda("ETL Lambda")
        queue = SQS("Query Queue")
        monitoring = Cloudwatch("Query Monitoring")
    
    # Data ingestion flow
    rds >> Edge(label="Export") >> s3_bronze
    logs >> s3_bronze
    raw_data >> s3_bronze
    
    # ETL processing
    s3_bronze >> lambda_etl >> s3_silver
    s3_silver >> lambda_etl >> s3_gold
    
    # Catalog and query
    s3_gold >> glue_catalog
    glue_catalog >> athena
    
    # User interaction
    users >> Edge(label="SQL Queries") >> athena
    athena >> Edge(label="Results") >> quicksight
    quicksight >> Edge(label="Dashboards") >> users
    
    # Monitoring
    athena >> Edge(label="Query Metrics") >> monitoring
    queue >> Edge(label="Scheduled Queries") >> athena

print("Athena analytics diagram generated successfully!")
