#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMREngineMaprM3, Kinesis
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import ELB
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.database import Cassandra

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("EMR Engine MapR M3 Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr-engine-mapr-m3",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Scientists")
    
    with Cluster("Data Ingestion"):
        kinesis_stream = Kinesis("Kinesis Streams")
        s3_raw = S3("Raw Data")
        rds_source = RDS("Operational DB")
        external_db = Cassandra("External DB")
    
    with Cluster("MapR M3 Cluster"):
        mapr_cluster = EMREngineMaprM3("MapR M3 Cluster")
        
        with Cluster("Cluster Nodes"):
            master_nodes = [EC2("Master 1"), EC2("Master 2")]
            data_nodes = [EC2("Data Node 1"), EC2("Data Node 2"), EC2("Data Node 3")]
            compute_nodes = [EC2("Compute 1"), EC2("Compute 2")]
    
    with Cluster("MapR Services"):
        mapr_fs = S3("MapR-FS")
        mapr_db = Dynamodb("MapR-DB")
        mapr_streams = Kinesis("MapR Streams")
    
    with Cluster("Processing Frameworks"):
        spark_engine = EC2("Spark Engine")
        drill_engine = EC2("Apache Drill")
        storm_engine = EC2("Apache Storm")
    
    with Cluster("Output & Analytics"):
        s3_processed = S3("Processed Data")
        load_balancer = ELB("Analytics API")
        dashboard = EC2("Analytics Dashboard")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM & MapR Security")
    
    # Data ingestion flow
    kinesis_stream >> Edge(label="Stream Data") >> mapr_cluster
    s3_raw >> Edge(label="Batch Data") >> mapr_cluster
    rds_source >> Edge(label="CDC") >> mapr_cluster
    external_db >> Edge(label="Replicate") >> mapr_cluster
    
    # Cluster internal structure
    mapr_cluster >> master_nodes
    mapr_cluster >> data_nodes
    mapr_cluster >> compute_nodes
    
    # MapR services
    mapr_cluster >> mapr_fs
    mapr_cluster >> mapr_db
    mapr_cluster >> mapr_streams
    
    # Processing engines
    mapr_cluster >> spark_engine
    mapr_cluster >> drill_engine
    mapr_cluster >> storm_engine
    
    # Output flow
    mapr_cluster >> s3_processed
    mapr_cluster >> load_balancer >> dashboard
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> mapr_cluster
    users >> Edge(label="Query Data") >> drill_engine
    users >> Edge(label="View Dashboard") >> dashboard
    
    # Monitoring and security
    mapr_cluster >> Edge(label="Metrics") >> monitoring
    security >> Edge(label="Access Control") >> mapr_cluster

print("EMR Engine MapR M3 diagram generated successfully!")
