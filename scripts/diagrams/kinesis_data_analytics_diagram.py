#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataAnalytics, KinesisDataStreams, KinesisDataFirehose
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Flink

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Kinesis Data Analytics Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/kinesis-data-analytics",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Business Users")
    
    with Cluster("Data Sources"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = Lambda("IoT Devices")
        log_sources = Lambda("Log Sources")
    
    with Cluster("Streaming Ingestion"):
        data_streams = KinesisDataStreams("Kinesis Data Streams")
        firehose = KinesisDataFirehose("Kinesis Data Firehose")
        kafka_source = SQS("Apache Kafka/MSK")
    
    with Cluster("Stream Processing"):
        analytics_app = KinesisDataAnalytics("Kinesis Data Analytics")
        
        with Cluster("Processing Engines"):
            sql_runtime = KinesisDataAnalytics("SQL Runtime")
            flink_runtime = Flink("Flink Runtime")
            beam_runtime = Lambda("Beam Runtime")
    
    with Cluster("Reference Data"):
        s3_reference = S3("Reference Data")
        lookup_tables = Dynamodb("Lookup Tables")
    
    with Cluster("Real-time Outputs"):
        real_time_dashboard = Lambda("Real-time Dashboard")
        alerts = SNS("Real-time Alerts")
        lambda_functions = Lambda("Lambda Functions")
        kinesis_output = KinesisDataStreams("Output Streams")
    
    with Cluster("Batch Outputs"):
        s3_results = S3("Analytics Results")
        data_warehouse = RDS("Data Warehouse")
        firehose_output = KinesisDataFirehose("Delivery Streams")
    
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data ingestion flow
    web_apps >> Edge(label="Events") >> data_streams
    mobile_apps >> Edge(label="Analytics") >> data_streams
    iot_devices >> Edge(label="Sensor Data") >> data_streams
    log_sources >> Edge(label="Logs") >> firehose
    
    # Stream processing input
    data_streams >> Edge(label="Stream Data") >> analytics_app
    firehose >> Edge(label="Buffered Data") >> analytics_app
    kafka_source >> Edge(label="Kafka Topics") >> analytics_app
    
    # Processing engines
    analytics_app >> sql_runtime
    analytics_app >> flink_runtime
    analytics_app >> beam_runtime
    
    # Reference data joins
    s3_reference >> Edge(label="Static Data") >> analytics_app
    lookup_tables >> Edge(label="Lookups") >> analytics_app
    
    # Real-time outputs
    sql_runtime >> real_time_dashboard
    flink_runtime >> alerts
    beam_runtime >> lambda_functions
    analytics_app >> kinesis_output
    
    # Batch outputs
    analytics_app >> firehose_output >> s3_results
    analytics_app >> Edge(label="Aggregated Results") >> data_warehouse
    
    # User interaction
    users >> Edge(label="View Dashboards") >> real_time_dashboard
    users >> Edge(label="Receive Alerts") >> alerts
    
    # Monitoring and security
    analytics_app >> Edge(label="Metrics") >> cloudwatch
    security >> Edge(label="Access Control") >> analytics_app

print("Kinesis Data Analytics diagram generated successfully!")
