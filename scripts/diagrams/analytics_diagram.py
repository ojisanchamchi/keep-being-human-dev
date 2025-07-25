#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Analytics
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("AWS Analytics Ecosystem", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/analytics-ecosystem",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Business Users")
    
    with Cluster("Data Sources"):
        rds = RDS("Transactional DB")
        dynamodb = Dynamodb("NoSQL DB")
        s3_raw = S3("Raw Data")
    
    with Cluster("Data Processing"):
        queue = SQS("Message Queue")
        lambda_fn = Lambda("Data Processing")
        notification = SNS("Notifications")
    
    with Cluster("Analytics Platform"):
        analytics = Analytics("AWS Analytics\nServices")
        s3_processed = S3("Processed Data")
    
    with Cluster("ML & Insights"):
        ml_model = SagemakerModel("ML Models")
        monitoring = Cloudwatch("Monitoring")
    
    # Data flow
    rds >> Edge(label="CDC") >> queue
    dynamodb >> Edge(label="Streams") >> queue
    s3_raw >> Edge(label="Batch") >> queue
    
    queue >> lambda_fn >> analytics
    analytics >> s3_processed
    analytics >> ml_model
    
    ml_model >> Edge(label="Predictions") >> notification
    analytics >> Edge(label="Metrics") >> monitoring
    
    users >> Edge(label="Queries") >> analytics
    notification >> Edge(label="Alerts") >> users

print("Analytics ecosystem diagram generated successfully!")
