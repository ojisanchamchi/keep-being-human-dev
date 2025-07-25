#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataAnalytics, KinesisDataFirehose
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Dynamodb, RDS
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Kinesis Data Streams Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/kinesis-data-streams",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Producers")
    
    with Cluster("Data Producers"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = Lambda("IoT Devices")
        log_agents = EC2("Log Agents")
        databases = RDS("Database CDC")
    
    with Cluster("Kinesis Data Streams"):
        stream = KinesisDataStreams("Data Stream")
        
        with Cluster("Shards"):
            shard1 = KinesisDataStreams("Shard 1")
            shard2 = KinesisDataStreams("Shard 2")
            shard3 = KinesisDataStreams("Shard 3")
            shard4 = KinesisDataStreams("Shard 4")
    
    with Cluster("Stream Consumers"):
        lambda_consumer = Lambda("Lambda Consumer")
        kda_app = KinesisDataAnalytics("KDA Application")
        firehose_consumer = KinesisDataFirehose("Firehose Consumer")
        custom_consumer = EC2("Custom Consumer")
    
    with Cluster("Processing & Storage"):
        real_time_db = Dynamodb("Real-time Results")
        s3_storage = S3("Data Lake")
        analytics_db = RDS("Analytics DB")
        search_index = Lambda("Search Index")
    
    with Cluster("Downstream Applications"):
        dashboard = Lambda("Real-time Dashboard")
        alerts = SNS("Alert System")
        ml_pipeline = Lambda("ML Pipeline")
        reporting = Lambda("Reporting System")
    
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
        scaling = Lambda("Auto Scaling")
    
    # Data ingestion
    web_apps >> Edge(label="Events") >> stream
    mobile_apps >> Edge(label="Analytics") >> stream
    iot_devices >> Edge(label="Sensor Data") >> stream
    log_agents >> Edge(label="Logs") >> stream
    databases >> Edge(label="Change Events") >> stream
    
    # Shard distribution
    stream >> shard1
    stream >> shard2
    stream >> shard3
    stream >> shard4
    
    # Stream consumption
    shard1 >> lambda_consumer
    shard2 >> kda_app
    shard3 >> firehose_consumer
    shard4 >> custom_consumer
    
    # Data processing and storage
    lambda_consumer >> real_time_db
    kda_app >> analytics_db
    firehose_consumer >> s3_storage
    custom_consumer >> search_index
    
    # Downstream applications
    real_time_db >> dashboard
    analytics_db >> alerts
    s3_storage >> ml_pipeline
    search_index >> reporting
    
    # User interaction
    users >> Edge(label="View Dashboards") >> dashboard
    users >> Edge(label="Receive Alerts") >> alerts
    
    # Monitoring and management
    stream >> Edge(label="Metrics") >> cloudwatch
    cloudwatch >> scaling >> stream
    security >> Edge(label="Access Control") >> stream

print("Kinesis Data Streams diagram generated successfully!")
