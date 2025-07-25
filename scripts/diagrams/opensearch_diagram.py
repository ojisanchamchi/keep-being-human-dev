#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import AmazonOpensearchService
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3
from diagrams.aws.network import ELB
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon OpenSearch Service Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/opensearch-architecture",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    with Cluster("Data Sources"):
        app_logs = EC2("Application Logs")
        database = RDS("Database")
        s3_data = S3("S3 Data Lake")
    
    with Cluster("Processing Layer"):
        queue = SQS("Message Queue")
        load_balancer = ELB("Load Balancer")
    
    with Cluster("Analytics Layer"):
        opensearch = AmazonOpensearchService("OpenSearch Cluster")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data flow
    app_logs >> Edge(label="Stream logs") >> queue
    database >> Edge(label="Change streams") >> queue
    s3_data >> Edge(label="Batch data") >> queue
    
    queue >> Edge(label="Process & Index") >> opensearch
    load_balancer >> Edge(label="Search queries") >> opensearch
    
    opensearch >> Edge(label="Metrics") >> monitoring
    security >> Edge(label="Access control") >> opensearch

print("OpenSearch diagram generated successfully!")
