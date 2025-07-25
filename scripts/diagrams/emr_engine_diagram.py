#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMREngine, Kinesis, Glue
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("EMR Engine Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr-engine",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        s3_data = S3("Data Lake")
        rds_db = RDS("Transactional DB")
        kinesis_stream = Kinesis("Streaming Data")
        external_data = EC2("External APIs")
    
    with Cluster("EMR Cluster"):
        emr_engine = EMREngine("EMR Processing\nEngines")
        
        with Cluster("Processing Frameworks"):
            spark_engine = Spark("Apache Spark")
            hadoop_engine = EC2("Hadoop MapReduce")
            flink_engine = EC2("Apache Flink")
            presto_engine = EC2("Presto")
            hive_engine = EC2("Apache Hive")
    
    with Cluster("Resource Management"):
        yarn_rm = EC2("YARN ResourceManager")
        yarn_nm = [EC2("NodeManager 1"), EC2("NodeManager 2")]
        k8s_master = EC2("Kubernetes Master")
    
    with Cluster("Storage Layer"):
        hdfs_storage = S3("HDFS Storage")
        s3_storage = S3("S3 Storage")
        local_storage = EC2("Local Storage")
    
    with Cluster("Output & Analytics"):
        processed_data = S3("Processed Data")
        ml_models = SagemakerModel("ML Models")
        data_catalog = Glue("Data Catalog")
        analytics_api = EC2("Analytics API")
    
    with Cluster("Monitoring & Management"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("Security")
    
    # Data ingestion
    s3_data >> Edge(label="Batch Data") >> emr_engine
    rds_db >> Edge(label="CDC") >> emr_engine
    kinesis_stream >> Edge(label="Streaming") >> emr_engine
    external_data >> Edge(label="API Data") >> emr_engine
    
    # Processing engines
    emr_engine >> spark_engine
    emr_engine >> hadoop_engine
    emr_engine >> flink_engine
    emr_engine >> presto_engine
    emr_engine >> hive_engine
    
    # Resource management
    emr_engine >> yarn_rm
    yarn_rm >> yarn_nm
    emr_engine >> k8s_master
    
    # Storage integration
    spark_engine >> hdfs_storage
    hadoop_engine >> s3_storage
    flink_engine >> local_storage
    
    # Output generation
    spark_engine >> processed_data
    flink_engine >> analytics_api
    hive_engine >> data_catalog
    spark_engine >> ml_models
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> emr_engine
    users >> Edge(label="Query Data") >> presto_engine
    users >> Edge(label="Stream Processing") >> flink_engine
    
    # Monitoring
    emr_engine >> monitoring
    security >> emr_engine

print("EMR Engine diagram generated successfully!")
