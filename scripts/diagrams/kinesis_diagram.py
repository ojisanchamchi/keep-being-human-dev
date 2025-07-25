#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Kinesis, KinesisDataStreams, KinesisDataFirehose, KinesisDataAnalytics, KinesisVideoStreams
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Dynamodb, RDS, Redshift
from diagrams.aws.ml import Rekognition, SagemakerModel
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Kinesis Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/kinesis",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Applications & Users")
    
    with Cluster("Data Sources"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = Mobile("IoT Devices")
        databases = RDS("Databases")
        video_sources = Lambda("Video Sources")
    
    with Cluster("Amazon Kinesis Platform"):
        kinesis_platform = Kinesis("Amazon Kinesis")
        
        with Cluster("Kinesis Services"):
            data_streams = KinesisDataStreams("Data Streams")
            data_firehose = KinesisDataFirehose("Data Firehose")
            data_analytics = KinesisDataAnalytics("Data Analytics")
            video_streams = KinesisVideoStreams("Video Streams")
    
    with Cluster("Stream Processing"):
        lambda_processor = Lambda("Lambda Functions")
        custom_apps = EC2("Custom Applications")
        analytics_apps = Lambda("Analytics Apps")
        ml_inference = SagemakerModel("ML Inference")
    
    with Cluster("Data Destinations"):
        s3_data_lake = S3("Data Lake")
        redshift_dw = Redshift("Data Warehouse")
        dynamodb_table = Dynamodb("Real-time DB")
        opensearch = Lambda("OpenSearch")
    
    with Cluster("Analytics & Insights"):
        real_time_dashboard = Lambda("Real-time Dashboards")
        bi_tools = Lambda("BI Tools")
        ml_models = SagemakerModel("ML Models")
        alerts = SNS("Alert System")
    
    with Cluster("Video Processing"):
        rekognition = Rekognition("Video Analysis")
        video_archive = S3("Video Archive")
        live_streaming = Lambda("Live Streaming")
    
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM & Security")
    
    # Data ingestion
    web_apps >> Edge(label="Events") >> data_streams
    mobile_apps >> Edge(label="Analytics") >> data_streams
    iot_devices >> Edge(label="Sensor Data") >> data_streams
    databases >> Edge(label="CDC") >> data_streams
    video_sources >> Edge(label="Video Feed") >> video_streams
    
    # Kinesis platform
    kinesis_platform >> data_streams
    kinesis_platform >> data_firehose
    kinesis_platform >> data_analytics
    kinesis_platform >> video_streams
    
    # Stream processing
    data_streams >> lambda_processor
    data_streams >> custom_apps
    data_analytics >> analytics_apps
    video_streams >> rekognition
    
    # Data delivery
    data_firehose >> s3_data_lake
    data_firehose >> redshift_dw
    lambda_processor >> dynamodb_table
    analytics_apps >> opensearch
    
    # Analytics and insights
    dynamodb_table >> real_time_dashboard
    s3_data_lake >> bi_tools
    opensearch >> ml_models
    rekognition >> alerts
    
    # Video processing
    video_streams >> video_archive
    video_streams >> live_streaming
    
    # User interaction
    users >> Edge(label="View Analytics") >> real_time_dashboard
    users >> Edge(label="BI Reports") >> bi_tools
    users >> Edge(label="Live Video") >> live_streaming
    
    # Monitoring
    kinesis_platform >> cloudwatch
    security >> kinesis_platform

print("Amazon Kinesis diagram generated successfully!")
