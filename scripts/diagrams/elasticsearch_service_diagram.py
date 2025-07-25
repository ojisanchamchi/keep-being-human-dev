#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ElasticsearchService, Kinesis
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Elasticsearch Service Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/elasticsearch-service",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Analysts & Developers")
    
    with Cluster("Data Sources"):
        app_servers = [EC2("App Server 1"), EC2("App Server 2")]
        database = RDS("Application DB")
        s3_logs = S3("Log Storage")
        kinesis_stream = Kinesis("Log Stream")
    
    with Cluster("Data Processing"):
        log_processor = Fluentbit("Log Processor")
        lambda_processor = Lambda("Log Processor")
        queue = SQS("Processing Queue")
    
    with Cluster("Elasticsearch Cluster"):
        elasticsearch = ElasticsearchService("Elasticsearch\nService")
        dashboard = Grafana("Analytics\nDashboard")
    
    with Cluster("Load Balancing & CDN"):
        load_balancer = ELB("Load Balancer")
        cdn = CloudFront("CloudFront")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data ingestion flow
    app_servers >> Edge(label="Application Logs") >> kinesis_stream
    database >> Edge(label="Query Logs") >> s3_logs
    s3_logs >> lambda_processor >> queue
    
    # Log processing
    kinesis_stream >> log_processor
    queue >> log_processor
    log_processor >> Edge(label="Structured Logs") >> elasticsearch
    
    # User access
    users >> cdn >> load_balancer >> dashboard
    dashboard >> Edge(label="Queries") >> elasticsearch
    elasticsearch >> Edge(label="Results") >> dashboard
    
    # Monitoring and security
    elasticsearch >> Edge(label="Cluster Metrics") >> monitoring
    security >> Edge(label="Access Control") >> elasticsearch
    security >> Edge(label="Dashboard Access") >> dashboard
    
    # Direct search access
    users >> Edge(label="Search API") >> elasticsearch

print("Elasticsearch Service diagram generated successfully!")
