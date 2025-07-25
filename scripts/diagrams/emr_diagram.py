#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMR, Kinesis, Glue, Athena
from diagrams.aws.storage import S3, EBS
from diagrams.aws.compute import EC2, EKS, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.ml import SagemakerModel, SagemakerNotebook
from diagrams.aws.network import ELB, VPC
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon EMR Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Teams")
    
    with Cluster("Data Sources"):
        s3_data_lake = S3("Data Lake")
        rds_oltp = RDS("OLTP Systems")
        kinesis_streams = Kinesis("Streaming Data")
        external_apis = Lambda("External APIs")
    
    with Cluster("EMR Ecosystem"):
        emr_service = EMR("Amazon EMR")
        
        with Cluster("Deployment Options"):
            emr_ec2 = EC2("EMR on EC2")
            emr_eks = EKS("EMR on EKS")
            emr_serverless = Lambda("EMR Serverless")
        
        with Cluster("Processing Frameworks"):
            spark = EC2("Apache Spark")
            hadoop = EC2("Apache Hadoop")
            flink = EC2("Apache Flink")
            presto = EC2("Presto")
            hbase = EC2("Apache HBase")
    
    with Cluster("Development Environment"):
        emr_studio = SagemakerNotebook("EMR Studio")
        emr_notebooks = SagemakerNotebook("EMR Notebooks")
        jupyter = EC2("Jupyter Hub")
    
    with Cluster("Storage Layer"):
        s3_storage = S3("S3 Storage")
        hdfs_storage = EBS("HDFS Storage")
        efs_storage = EBS("EFS Storage")
    
    with Cluster("Analytics & ML"):
        athena = Athena("Athena")
        sagemaker = SagemakerModel("SageMaker")
        glue_catalog = Glue("Data Catalog")
        quicksight = EC2("QuickSight")
    
    with Cluster("Infrastructure"):
        vpc = VPC("VPC")
        load_balancer = ELB("Load Balancer")
        monitoring = Cloudwatch("Monitoring")
        security = IAM("Security")
    
    # Data ingestion
    s3_data_lake >> Edge(label="Batch Data") >> emr_service
    rds_oltp >> Edge(label="CDC") >> emr_service
    kinesis_streams >> Edge(label="Streaming") >> emr_service
    external_apis >> Edge(label="API Data") >> emr_service
    
    # EMR deployment options
    emr_service >> emr_ec2
    emr_service >> emr_eks
    emr_service >> emr_serverless
    
    # Processing frameworks
    emr_ec2 >> spark
    emr_ec2 >> hadoop
    emr_eks >> flink
    emr_serverless >> spark
    
    # Development environment
    users >> emr_studio
    users >> emr_notebooks
    emr_studio >> emr_service
    emr_notebooks >> jupyter
    
    # Storage integration
    spark >> s3_storage
    hadoop >> hdfs_storage
    flink >> efs_storage
    
    # Analytics integration
    spark >> athena
    emr_service >> sagemaker
    hadoop >> glue_catalog
    emr_service >> quicksight
    
    # Infrastructure
    emr_service >> vpc
    emr_service >> load_balancer
    emr_service >> monitoring
    security >> emr_service
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> emr_service
    users >> Edge(label="Monitor") >> monitoring

print("Amazon EMR diagram generated successfully!")
