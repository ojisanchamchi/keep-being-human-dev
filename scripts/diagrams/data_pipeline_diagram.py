#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import DataPipeline, EMR
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Redshift
from diagrams.aws.compute import EC2
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.database import MySQL
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("AWS Data Pipeline Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/data-pipeline",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        on_prem_db = MySQL("On-premises DB")
        rds_source = RDS("RDS Source")
        s3_raw = S3("Raw Data")
    
    with Cluster("Pipeline Orchestration"):
        data_pipeline = DataPipeline("Data Pipeline\nService")
        pipeline_queue = SQS("Pipeline Queue")
        notifications = SNS("Notifications")
    
    with Cluster("Processing Resources"):
        ec2_instances = [EC2("EC2 Worker 1"), EC2("EC2 Worker 2")]
        emr_cluster = EMR("EMR Cluster")
    
    with Cluster("Data Destinations"):
        s3_processed = S3("Processed Data")
        redshift = Redshift("Data Warehouse")
        rds_target = RDS("RDS Target")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Pipeline definition and scheduling
    users >> Edge(label="Define Pipeline") >> data_pipeline
    data_pipeline >> Edge(label="Schedule Tasks") >> pipeline_queue
    
    # Data extraction
    on_prem_db >> Edge(label="Extract") >> ec2_instances
    rds_source >> Edge(label="Extract") >> ec2_instances
    s3_raw >> Edge(label="Read") >> emr_cluster
    
    # Pipeline execution
    pipeline_queue >> ec2_instances
    pipeline_queue >> emr_cluster
    
    # Data processing and loading
    ec2_instances >> Edge(label="Transform") >> s3_processed
    emr_cluster >> Edge(label="Process") >> s3_processed
    s3_processed >> Edge(label="Load") >> redshift
    s3_processed >> Edge(label="Load") >> rds_target
    
    # Monitoring and notifications
    data_pipeline >> Edge(label="Status") >> monitoring
    data_pipeline >> Edge(label="Alerts") >> notifications
    notifications >> Edge(label="Notifications") >> users
    
    # Security
    security >> Edge(label="Access Control") >> data_pipeline
    security >> Edge(label="Resource Permissions") >> ec2_instances

print("Data Pipeline diagram generated successfully!")
