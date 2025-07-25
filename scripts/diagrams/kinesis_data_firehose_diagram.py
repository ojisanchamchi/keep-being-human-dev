#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataFirehose, KinesisDataStreams, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Redshift, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Kinesis Data Firehose Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/kinesis-data-firehose",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Applications")
    
    with Cluster("Data Sources"):
        web_logs = Lambda("Web Server Logs")
        app_events = Lambda("Application Events")
        iot_sensors = Lambda("IoT Sensors")
        clickstream = Lambda("Clickstream Data")
        kinesis_streams = KinesisDataStreams("Kinesis Data Streams")
    
    with Cluster("Firehose Delivery Streams"):
        firehose_s3 = KinesisDataFirehose("S3 Delivery Stream")
        firehose_redshift = KinesisDataFirehose("Redshift Delivery Stream")
        firehose_opensearch = KinesisDataFirehose("OpenSearch Delivery Stream")
        firehose_spark = KinesisDataFirehose("Spark Delivery Stream")
    
    with Cluster("Data Transformation"):
        lambda_transform = Lambda("Data Transformation")
        format_converter = Lambda("Format Converter")
        data_enrichment = Lambda("Data Enrichment")
    
    with Cluster("Destinations"):
        s3_data_lake = S3("S3 Data Lake")
        redshift_dw = Redshift("Redshift DW")
        opensearch = Lambda("OpenSearch Service")
        spark_cluster = Spark("Spark Cluster")
    
    with Cluster("Error Handling"):
        error_bucket = S3("Error Records")
        processing_errors = S3("Processing Errors")
        dlq = SQS("Dead Letter Queue")
    
    with Cluster("Analytics & Monitoring"):
        athena = Athena("Athena Queries")
        cloudwatch = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        security = IAM("IAM Roles")
    
    # Data ingestion flow
    web_logs >> Edge(label="Direct PUT") >> firehose_s3
    app_events >> Edge(label="SDK/API") >> firehose_redshift
    iot_sensors >> Edge(label="IoT Core") >> firehose_opensearch
    clickstream >> Edge(label="Analytics") >> firehose_spark
    kinesis_streams >> Edge(label="Stream Consumer") >> firehose_s3
    
    # Data transformation
    firehose_s3 >> lambda_transform
    firehose_redshift >> format_converter
    firehose_opensearch >> data_enrichment
    
    lambda_transform >> firehose_s3
    format_converter >> firehose_redshift
    data_enrichment >> firehose_opensearch
    
    # Data delivery
    firehose_s3 >> Edge(label="Parquet/ORC") >> s3_data_lake
    firehose_redshift >> Edge(label="COPY Command") >> redshift_dw
    firehose_opensearch >> Edge(label="Bulk API") >> opensearch
    firehose_spark >> Edge(label="HTTP Protocol") >> spark_cluster
    
    # Error handling
    firehose_s3 >> Edge(label="Failed Records") >> error_bucket
    lambda_transform >> Edge(label="Processing Errors") >> processing_errors
    firehose_redshift >> Edge(label="Failed Loads") >> dlq
    
    # Analytics integration
    s3_data_lake >> athena
    users >> Edge(label="Query Data") >> athena
    
    # Monitoring
    firehose_s3 >> Edge(label="Metrics") >> cloudwatch
    cloudwatch >> notifications
    security >> Edge(label="Access Control") >> firehose_s3

print("Kinesis Data Firehose diagram generated successfully!")
