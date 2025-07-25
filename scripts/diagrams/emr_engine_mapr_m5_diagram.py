#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMREngineMaprM5, Kinesis, Glue
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("EMR Engine MapR M5 Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr-engine-mapr-m5",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Business Users")
    
    with Cluster("Data Ingestion Layer"):
        kinesis_streams = Kinesis("Kinesis Data Streams")
        s3_data_lake = S3("Data Lake")
        rds_oltp = RDS("OLTP Systems")
        external_apis = Lambda("External APIs")
    
    with Cluster("MapR M5 Cluster"):
        mapr_m5 = EMREngineMaprM5("MapR M5 Platform")
        
        with Cluster("Cluster Tiers"):
            master_tier = [EC2("Master 1"), EC2("Master 2"), EC2("Master 3")]
            data_tier = [EC2("Data Node 1"), EC2("Data Node 2"), EC2("Data Node 3")]
            compute_tier = [EC2("Compute 1"), EC2("Compute 2"), EC2("Compute 3")]
    
    with Cluster("Processing Engines"):
        spark_engine = Spark("Spark 3.0")
        drill_engine = EC2("Apache Drill")
        flink_engine = EC2("Apache Flink")
        ml_engine = SagemakerModel("ML Engine")
    
    with Cluster("Data Services"):
        mapr_fs = S3("MapR-FS")
        mapr_db = Dynamodb("MapR-DB")
        mapr_streams = Kinesis("MapR Event Store")
        data_catalog = Glue("Data Catalog")
    
    with Cluster("Analytics & Serving"):
        real_time_api = ELB("Real-time API")
        batch_results = S3("Batch Results")
        cdn = CloudFront("Analytics CDN")
        dashboard = EC2("Analytics Dashboard")
    
    with Cluster("Monitoring & Governance"):
        monitoring = Cloudwatch("Monitoring")
        security = IAM("Security & Governance")
    
    # Data ingestion flow
    kinesis_streams >> Edge(label="Stream") >> mapr_m5
    s3_data_lake >> Edge(label="Batch") >> mapr_m5
    rds_oltp >> Edge(label="CDC") >> mapr_m5
    external_apis >> Edge(label="API Data") >> mapr_m5
    
    # Cluster architecture
    mapr_m5 >> master_tier
    mapr_m5 >> data_tier
    mapr_m5 >> compute_tier
    
    # Data services
    mapr_m5 >> mapr_fs
    mapr_m5 >> mapr_db
    mapr_m5 >> mapr_streams
    mapr_m5 >> data_catalog
    
    # Processing engines
    mapr_m5 >> spark_engine
    mapr_m5 >> drill_engine
    mapr_m5 >> flink_engine
    mapr_m5 >> ml_engine
    
    # Output and serving
    spark_engine >> batch_results
    flink_engine >> real_time_api
    drill_engine >> dashboard
    ml_engine >> real_time_api
    
    # User access
    users >> cdn >> dashboard
    users >> real_time_api
    users >> Edge(label="Ad-hoc Queries") >> drill_engine
    
    # Monitoring and governance
    mapr_m5 >> monitoring
    security >> mapr_m5

print("EMR Engine MapR M5 diagram generated successfully!")
