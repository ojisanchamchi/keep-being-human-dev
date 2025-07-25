#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka, KinesisDataAnalytics, EMR
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import RDS, Dynamodb, Redshift
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon MSK Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/managed-streaming-for-kafka"):
    
    # Data producers
    with Cluster("Data Producers"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = EC2("IoT Devices")
        databases = RDS("Database CDC")
        microservices = Lambda("Microservices")
    
    # MSK cluster
    with Cluster("Amazon MSK Cluster"):
        msk_broker1 = ManagedStreamingForKafka("Broker 1 (AZ-1)")
        msk_broker2 = ManagedStreamingForKafka("Broker 2 (AZ-2)")
        msk_broker3 = ManagedStreamingForKafka("Broker 3 (AZ-3)")
    
    # MSK Connect
    with Cluster("MSK Connect"):
        s3_connector = Lambda("S3 Sink Connector")
        db_connector = Lambda("Database Source Connector")
        elasticsearch_connector = Lambda("OpenSearch Connector")
    
    # Stream processing
    with Cluster("Stream Processing"):
        kafka_streams = Spark("Kafka Streams")
        lambda_processor = Lambda("Lambda Processors")
        kinesis_analytics = KinesisDataAnalytics("Kinesis Analytics")
        emr_spark = EMR("EMR Spark Streaming")
    
    # Data destinations
    with Cluster("Data Destinations"):
        s3_datalake = S3("Data Lake")
        redshift_dw = Redshift("Data Warehouse")
        dynamodb_store = Dynamodb("Real-time Store")
        opensearch = Lambda("OpenSearch")
    
    # Monitoring and management
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        iam_security = IAM("IAM Security")
        notifications = SNS("Alerts")
    
    # Producer connections to MSK
    web_apps >> Edge(label="Events") >> msk_broker1
    mobile_apps >> Edge(label="User Actions") >> msk_broker2
    iot_devices >> Edge(label="Sensor Data") >> msk_broker3
    databases >> Edge(label="Change Events") >> msk_broker1
    microservices >> Edge(label="Domain Events") >> msk_broker2
    
    # MSK Connect integrations
    msk_broker1 >> Edge(label="Topics") >> s3_connector
    msk_broker2 >> Edge(label="Topics") >> elasticsearch_connector
    db_connector >> Edge(label="Source Data") >> msk_broker3
    
    # Stream processing consumers
    msk_broker1 >> Edge(label="Consumer Groups") >> kafka_streams
    msk_broker2 >> Edge(label="Event Triggers") >> lambda_processor
    msk_broker3 >> Edge(label="Analytics") >> kinesis_analytics
    msk_broker1 >> Edge(label="Batch Processing") >> emr_spark
    
    # Data flow to destinations
    s3_connector >> Edge(label="Bulk Load") >> s3_datalake
    kafka_streams >> Edge(label="Processed") >> dynamodb_store
    lambda_processor >> Edge(label="Real-time") >> dynamodb_store
    kinesis_analytics >> Edge(label="Aggregated") >> redshift_dw
    emr_spark >> Edge(label="Analytics") >> s3_datalake
    elasticsearch_connector >> Edge(label="Search Data") >> opensearch
    
    # Monitoring connections
    msk_broker1 >> Edge(label="Metrics") >> cloudwatch
    msk_broker2 >> Edge(label="Metrics") >> cloudwatch
    msk_broker3 >> Edge(label="Metrics") >> cloudwatch
    cloudwatch >> Edge(label="Alerts") >> notifications
    
    # Security
    iam_security >> Edge(label="Access Control") >> msk_broker1
    iam_security >> Edge(label="Access Control") >> msk_broker2
    iam_security >> Edge(label="Access Control") >> msk_broker3

print("MSK diagram generated successfully!")
