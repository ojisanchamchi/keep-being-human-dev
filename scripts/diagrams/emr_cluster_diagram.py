#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMRCluster, Glue, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("EMR Cluster Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr-cluster",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        rds = RDS("Operational DB")
        dynamodb = Dynamodb("NoSQL DB")
        s3_raw = S3("Raw Data Lake")
        streaming_data = SQS("Streaming Data")
    
    with Cluster("EMR Processing"):
        emr_cluster = EMRCluster("EMR Cluster")
        master_node = EC2("Master Node")
        core_nodes = [EC2("Core Node 1"), EC2("Core Node 2")]
        task_nodes = [EC2("Task Node 1"), EC2("Task Node 2")]
    
    with Cluster("Storage & Output"):
        s3_processed = S3("Processed Data")
        s3_results = S3("Analytics Results")
        glue_catalog = Glue("Data Catalog")
    
    with Cluster("Analytics & ML"):
        athena = Athena("Query Engine")
        ml_model = SagemakerModel("ML Pipeline")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data ingestion
    rds >> Edge(label="Extract") >> s3_raw
    dynamodb >> Edge(label="Export") >> s3_raw
    streaming_data >> Edge(label="Stream") >> emr_cluster
    
    # EMR cluster structure
    emr_cluster >> master_node
    master_node >> core_nodes
    master_node >> task_nodes
    
    # Data processing flow
    s3_raw >> Edge(label="Input Data") >> emr_cluster
    emr_cluster >> Edge(label="Processed") >> s3_processed
    emr_cluster >> Edge(label="Results") >> s3_results
    
    # Analytics integration
    s3_processed >> glue_catalog >> athena
    s3_results >> ml_model
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> emr_cluster
    users >> Edge(label="Query Results") >> athena
    
    # Monitoring and security
    emr_cluster >> Edge(label="Metrics") >> monitoring
    security >> Edge(label="Access Control") >> emr_cluster

print("EMR Cluster diagram generated successfully!")
