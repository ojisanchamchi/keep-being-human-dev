#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import LakeFormation, Athena, Glue, EMR
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb, Redshift
from diagrams.aws.security import IAM, KMS
from diagrams.aws.management import Cloudwatch, Cloudtrail
from diagrams.aws.ml import SagemakerModel
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("AWS Lake Formation Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/lake-formation"):
    
    # Users and applications
    with Cluster("Data Consumers"):
        analysts = Users("Data Analysts")
        data_scientists = Users("Data Scientists")
        bi_tools = Users("BI Applications")
    
    # Lake Formation core
    with Cluster("AWS Lake Formation"):
        lf_service = LakeFormation("Lake Formation")
        data_catalog = Glue("Data Catalog")
        permissions = IAM("Fine-grained Permissions")
    
    # Data sources
    with Cluster("Data Sources"):
        s3_raw = S3("Raw Data Lake")
        rds_source = RDS("Operational DB")
        dynamodb_source = Dynamodb("NoSQL Data")
        streaming_data = Lambda("Streaming Sources")
    
    # ETL and processing
    with Cluster("Data Processing"):
        glue_etl = Glue("ETL Jobs")
        emr_processing = EMR("Big Data Processing")
        lambda_transform = Lambda("Data Transformation")
    
    # Analytics services
    with Cluster("Analytics & ML"):
        athena_query = Athena("Interactive Queries")
        redshift_dw = Redshift("Data Warehouse")
        sagemaker_ml = SagemakerModel("ML Models")
    
    # Security and governance
    with Cluster("Security & Governance"):
        kms_encryption = KMS("Encryption")
        cloudtrail_audit = Cloudtrail("Audit Logs")
        cloudwatch_monitor = Cloudwatch("Monitoring")
    
    # Data flow connections
    rds_source >> Edge(label="CDC") >> glue_etl
    dynamodb_source >> Edge(label="Export") >> glue_etl
    streaming_data >> Edge(label="Real-time") >> s3_raw
    
    # ETL to data lake
    glue_etl >> Edge(label="Processed Data") >> s3_raw
    emr_processing >> Edge(label="Big Data") >> s3_raw
    lambda_transform >> Edge(label="Transformed") >> s3_raw
    
    # Lake Formation governance
    s3_raw >> Edge(label="Register") >> lf_service
    lf_service >> Edge(label="Catalog") >> data_catalog
    lf_service >> Edge(label="Access Control") >> permissions
    
    # Analytics access through Lake Formation
    analysts >> Edge(label="Query") >> lf_service
    data_scientists >> Edge(label="Access") >> lf_service
    bi_tools >> Edge(label="Connect") >> lf_service
    
    # Lake Formation to analytics services
    lf_service >> Edge(label="Secure Access") >> athena_query
    lf_service >> Edge(label="Governed Data") >> redshift_dw
    lf_service >> Edge(label="ML Features") >> sagemaker_ml
    
    # Security integrations
    lf_service >> Edge(label="Encrypt") >> kms_encryption
    lf_service >> Edge(label="Audit") >> cloudtrail_audit
    lf_service >> Edge(label="Monitor") >> cloudwatch_monitor

print("Lake Formation diagram generated successfully!")
