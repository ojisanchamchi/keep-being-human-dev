#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import RedshiftDenseComputeNode, Redshift, Quicksight
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.generic.storage import Storage

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Redshift Dense Compute Node Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/redshift-dense-compute-node"):
    
    # Data sources
    with Cluster("Data Sources"):
        s3_staging = S3("S3 Staging")
        operational_db = RDS("Operational DB")
        real_time_data = Lambda("Real-time Feeds")
    
    # DC2 Cluster configuration
    with Cluster("Redshift DC2 Cluster"):
        leader_node = Redshift("Leader Node")
        
        with Cluster("Dense Compute Nodes"):
            dc_node1 = RedshiftDenseComputeNode("DC Node 1\n32 vCPU, 244GB RAM\n2.56TB SSD")
            dc_node2 = RedshiftDenseComputeNode("DC Node 2\n32 vCPU, 244GB RAM\n2.56TB SSD")
            dc_node3 = RedshiftDenseComputeNode("DC Node 3\n32 vCPU, 244GB RAM\n2.56TB SSD")
            dc_node4 = RedshiftDenseComputeNode("DC Node 4\n32 vCPU, 244GB RAM\n2.56TB SSD")
    
    # Performance features
    with Cluster("Performance Features"):
        local_ssd = Storage("Local SSD Storage")
        result_cache = Lambda("Result Caching")
        columnar_storage = Lambda("Columnar Storage")
        compression = Lambda("Automatic Compression")
    
    # Workload management
    with Cluster("Workload Management"):
        interactive_queue = Lambda("Interactive Queue\n5 slots, 30% memory")
        etl_queue = Lambda("ETL Queue\n2 slots, 60% memory")
        default_queue = Lambda("Default Queue\n3 slots, 10% memory")
    
    # Analytics applications
    with Cluster("Analytics Applications"):
        real_time_dashboard = Quicksight("Real-time Dashboards")
        interactive_queries = Users("Interactive Queries")
        ad_hoc_analysis = Users("Ad-hoc Analysis")
        reporting_tools = Users("Reporting Tools")
    
    # Monitoring and optimization
    with Cluster("Performance Monitoring"):
        query_performance = Cloudwatch("Query Performance")
        resource_utilization = Cloudwatch("Resource Utilization")
        concurrency_metrics = Cloudwatch("Concurrency Metrics")
    
    # Data loading
    s3_staging >> Edge(label="COPY\nHigh Throughput") >> leader_node
    operational_db >> Edge(label="ETL Pipeline") >> s3_staging
    real_time_data >> Edge(label="Micro-batches") >> s3_staging
    
    # Leader node distribution
    leader_node >> Edge(label="Query Distribution\nMPP Architecture") >> dc_node1
    leader_node >> Edge(label="Query Distribution\nMPP Architecture") >> dc_node2
    leader_node >> Edge(label="Query Distribution\nMPP Architecture") >> dc_node3
    leader_node >> Edge(label="Query Distribution\nMPP Architecture") >> dc_node4
    
    # Performance features integration
    dc_node1 >> Edge(label="Local I/O") >> local_ssd
    dc_node2 >> Edge(label="Local I/O") >> local_ssd
    dc_node3 >> Edge(label="Local I/O") >> local_ssd
    dc_node4 >> Edge(label="Local I/O") >> local_ssd
    
    leader_node >> Edge(label="Cache Results") >> result_cache
    dc_node1 >> Edge(label="Columnar Format") >> columnar_storage
    columnar_storage >> Edge(label="Compress") >> compression
    
    # Workload management
    leader_node >> Edge(label="Route Queries") >> interactive_queue
    leader_node >> Edge(label="Route Queries") >> etl_queue
    leader_node >> Edge(label="Route Queries") >> default_queue
    
    # Application connections
    interactive_queue >> Edge(label="Sub-second Response") >> real_time_dashboard
    interactive_queue >> Edge(label="Fast Queries") >> interactive_queries
    default_queue >> Edge(label="Exploratory") >> ad_hoc_analysis
    etl_queue >> Edge(label="Batch Reports") >> reporting_tools
    
    # Performance monitoring
    dc_node1 >> Edge(label="Metrics") >> query_performance
    dc_node2 >> Edge(label="Metrics") >> resource_utilization
    dc_node3 >> Edge(label="Metrics") >> concurrency_metrics
    
    # Query result flow
    dc_node1 >> Edge(label="Results") >> leader_node
    dc_node2 >> Edge(label="Results") >> leader_node
    dc_node3 >> Edge(label="Results") >> leader_node
    dc_node4 >> Edge(label="Results") >> leader_node
    
    # Cache utilization
    result_cache >> Edge(label="Cached Results") >> real_time_dashboard
    result_cache >> Edge(label="Cached Results") >> interactive_queries

print("Redshift Dense Compute Node diagram generated successfully!")
