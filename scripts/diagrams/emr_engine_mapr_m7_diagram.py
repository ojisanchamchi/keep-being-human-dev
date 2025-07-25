#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMREngineMaprM7, Kinesis, Glue
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb, Timestream
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.network import ELB, CloudFront, DirectConnect
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS, SNS
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("EMR Engine MapR M7 Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr-engine-mapr-m7",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Enterprise Users")
    
    with Cluster("Multi-Source Data Ingestion"):
        edge_devices = EC2("Edge Devices")
        kinesis_streams = Kinesis("Kinesis Data Streams")
        direct_connect = DirectConnect("Direct Connect")
        s3_data_lake = S3("Multi-Petabyte Data Lake")
        time_series = Timestream("Time Series DB")
    
    with Cluster("MapR M7i Cluster"):
        mapr_m7 = EMREngineMaprM7("MapR M7i Platform")
        
        with Cluster("High-Performance Tiers"):
            control_plane = [EC2("Control 1"), EC2("Control 2"), EC2("Control 3")]
            data_plane = [EC2("Data Node 1"), EC2("Data Node 2"), EC2("Data Node 3"), EC2("Data Node 4")]
            compute_plane = [EC2("Compute 1"), EC2("Compute 2"), EC2("Compute 3"), EC2("Compute 4")]
            gpu_plane = [EC2("GPU Node 1"), EC2("GPU Node 2")]
    
    with Cluster("Advanced Processing Engines"):
        spark_engine = Spark("Spark 3.3+")
        flink_engine = EC2("Flink 1.15+")
        ray_engine = EC2("Ray Cluster")
        quantum_engine = EC2("Quantum Simulator")
    
    with Cluster("AI/ML Platform"):
        ml_pipeline = SagemakerModel("ML Pipeline")
        model_serving = ELB("Model Serving")
        feature_store = Dynamodb("Feature Store")
        experiment_tracking = EC2("MLflow")
    
    with Cluster("Data Services & Catalog"):
        mapr_fs = S3("MapR-FS v7")
        mapr_db = Dynamodb("MapR-DB NoSQL")
        event_store = Kinesis("Event Store")
        data_catalog = Glue("Unified Catalog")
    
    with Cluster("Real-time & Batch Outputs"):
        real_time_api = ELB("Real-time API")
        batch_warehouse = S3("Data Warehouse")
        streaming_analytics = Lambda("Stream Analytics")
        notification_system = SNS("Alerts & Notifications")
    
    with Cluster("Observability & Governance"):
        monitoring = Cloudwatch("Advanced Monitoring")
        security = IAM("Zero-Trust Security")
        data_lineage = EC2("Data Lineage")
        cost_optimization = EC2("Cost Intelligence")
    
    # Multi-source data ingestion
    edge_devices >> Edge(label="IoT Data") >> kinesis_streams
    direct_connect >> Edge(label="Enterprise Data") >> mapr_m7
    s3_data_lake >> Edge(label="Historical Data") >> mapr_m7
    time_series >> Edge(label="Metrics") >> mapr_m7
    kinesis_streams >> Edge(label="Streaming") >> mapr_m7
    
    # Cluster architecture
    mapr_m7 >> control_plane
    mapr_m7 >> data_plane
    mapr_m7 >> compute_plane
    mapr_m7 >> gpu_plane
    
    # Advanced processing
    mapr_m7 >> spark_engine
    mapr_m7 >> flink_engine
    mapr_m7 >> ray_engine
    mapr_m7 >> quantum_engine
    
    # AI/ML integration
    gpu_plane >> ml_pipeline
    ml_pipeline >> model_serving
    ml_pipeline >> feature_store
    ml_pipeline >> experiment_tracking
    
    # Data services
    mapr_m7 >> mapr_fs
    mapr_m7 >> mapr_db
    mapr_m7 >> event_store
    mapr_m7 >> data_catalog
    
    # Output systems
    flink_engine >> real_time_api
    spark_engine >> batch_warehouse
    ray_engine >> streaming_analytics
    model_serving >> notification_system
    
    # User interactions
    users >> Edge(label="Analytics Queries") >> real_time_api
    users >> Edge(label="ML Models") >> model_serving
    users >> Edge(label="Data Exploration") >> data_catalog
    
    # Governance and monitoring
    mapr_m7 >> monitoring
    security >> mapr_m7
    mapr_m7 >> data_lineage
    mapr_m7 >> cost_optimization

print("EMR Engine MapR M7 diagram generated successfully!")
