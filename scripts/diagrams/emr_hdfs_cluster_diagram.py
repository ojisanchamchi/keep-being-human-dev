#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMRHdfsCluster, Glue
from diagrams.aws.storage import S3, EBS
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Hadoop

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("EMR HDFS Cluster Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/emr-hdfs-cluster",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Ingestion"):
        s3_raw = S3("Raw Data")
        rds_source = RDS("Operational DB")
        external_data = EC2("External Sources")
    
    with Cluster("EMR HDFS Cluster"):
        hdfs_cluster = EMRHdfsCluster("HDFS Cluster")
        
        with Cluster("Master Services"):
            namenode = Hadoop("NameNode")
            secondary_nn = Hadoop("Secondary NameNode")
            resource_manager = EC2("ResourceManager")
        
        with Cluster("Worker Nodes"):
            datanode1 = EC2("DataNode 1\n+ NodeManager")
            datanode2 = EC2("DataNode 2\n+ NodeManager")
            datanode3 = EC2("DataNode 3\n+ NodeManager")
            datanode4 = EC2("DataNode 4\n+ NodeManager")
        
        with Cluster("Local Storage"):
            ebs1 = EBS("EBS Volume 1")
            ebs2 = EBS("EBS Volume 2")
            ebs3 = EBS("EBS Volume 3")
            ebs4 = EBS("EBS Volume 4")
    
    with Cluster("Processing Frameworks"):
        mapreduce = Hadoop("MapReduce")
        spark_hdfs = EC2("Spark on HDFS")
        hive_hdfs = EC2("Hive")
        hbase = EC2("HBase")
    
    with Cluster("Output & Analytics"):
        processed_hdfs = S3("Processed Data")
        s3_backup = S3("HDFS Backup")
        data_catalog = Glue("Data Catalog")
        analytics_api = ELB("Analytics API")
    
    with Cluster("Monitoring & Management"):
        monitoring = Cloudwatch("Cluster Monitoring")
        security = IAM("Security & Access")
        hdfs_ui = EC2("HDFS Web UI")
    
    # Data ingestion
    s3_raw >> Edge(label="Import") >> hdfs_cluster
    rds_source >> Edge(label="Sqoop Import") >> hdfs_cluster
    external_data >> Edge(label="Batch Load") >> hdfs_cluster
    
    # HDFS cluster structure
    hdfs_cluster >> namenode
    hdfs_cluster >> secondary_nn
    hdfs_cluster >> resource_manager
    
    # DataNodes and storage
    hdfs_cluster >> datanode1 >> ebs1
    hdfs_cluster >> datanode2 >> ebs2
    hdfs_cluster >> datanode3 >> ebs3
    hdfs_cluster >> datanode4 >> ebs4
    
    # NameNode coordination
    namenode >> Edge(label="Block Metadata") >> [datanode1, datanode2, datanode3, datanode4]
    
    # Processing frameworks
    hdfs_cluster >> mapreduce
    hdfs_cluster >> spark_hdfs
    hdfs_cluster >> hive_hdfs
    hdfs_cluster >> hbase
    
    # Output and backup
    spark_hdfs >> processed_hdfs
    hdfs_cluster >> Edge(label="Backup") >> s3_backup
    hive_hdfs >> data_catalog
    mapreduce >> analytics_api
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> resource_manager
    users >> Edge(label="Query Data") >> hive_hdfs
    users >> Edge(label="Monitor") >> hdfs_ui
    
    # Monitoring and security
    hdfs_cluster >> monitoring
    security >> hdfs_cluster

print("EMR HDFS Cluster diagram generated successfully!")
