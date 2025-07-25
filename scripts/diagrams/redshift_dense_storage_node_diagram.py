#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import RedshiftDenseStorageNode, Redshift, Quicksight
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

with Diagram("Redshift Dense Storage Node Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/redshift-dense-storage-node"):
    
    # Data sources
    with Cluster("Historical Data Sources"):
        s3_archive = S3("S3 Historical Archive")
        legacy_systems = RDS("Legacy Systems")
        data_warehouse = Lambda("External DW")
    
    # DS2 Cluster configuration
    with Cluster("Redshift DS2 Cluster"):
        leader_node = Redshift("Leader Node")
        
        with Cluster("Dense Storage Nodes"):
            ds_node1 = RedshiftDenseStorageNode("DS Node 1\n36 vCPU, 244GB RAM\n16TB HDD")
            ds_node2 = RedshiftDenseStorageNode("DS Node 2\n36 vCPU, 244GB RAM\n16TB HDD")
            ds_node3 = RedshiftDenseStorageNode("DS Node 3\n36 vCPU, 244GB RAM\n16TB HDD")
            ds_node4 = RedshiftDenseStorageNode("DS Node 4\n36 vCPU, 244GB RAM\n16TB HDD")
            ds_node5 = RedshiftDenseStorageNode("DS Node 5\n36 vCPU, 244GB RAM\n16TB HDD")
            ds_node6 = RedshiftDenseStorageNode("DS Node 6\n36 vCPU, 244GB RAM\n16TB HDD")
    
    # Storage features
    with Cluster("Storage Features"):
        magnetic_storage = Storage("Large HDD Storage\n16TB per node")
        compression = Lambda("Columnar Compression\n3:1 ratio")
        data_distribution = Lambda("Even Data Distribution")
        backup_snapshots = S3("Automated Snapshots")
    
    # Workload management for large datasets
    with Cluster("Workload Management"):
        etl_heavy_queue = Lambda("ETL Heavy Queue\n3 slots, 70% memory")
        reporting_queue = Lambda("Reporting Queue\n5 slots, 25% memory")
        maintenance_queue = Lambda("Maintenance Queue\n2 slots, 5% memory")
    
    # Analytics applications
    with Cluster("Analytics Applications"):
        historical_reports = Users("Historical Reports")
        trend_analysis = Quicksight("Trend Analysis")
        compliance_reporting = Users("Compliance Reports")
        data_archival = Lambda("Data Archival")
    
    # Data lifecycle management
    with Cluster("Data Lifecycle"):
        data_retention = Lambda("7-Year Retention")
        automated_archival = S3("S3 Glacier Archive")
        compliance_audit = Lambda("Compliance Auditing")
    
    # Performance monitoring
    with Cluster("Storage Monitoring"):
        storage_utilization = Cloudwatch("Storage Utilization")
        io_performance = Cloudwatch("I/O Performance")
        query_optimization = Cloudwatch("Query Optimization")
    
    # Data loading - optimized for large volumes
    s3_archive >> Edge(label="Bulk COPY\nLarge Files") >> leader_node
    legacy_systems >> Edge(label="Historical ETL") >> s3_archive
    data_warehouse >> Edge(label="Migration") >> s3_archive
    
    # Leader node distribution to DS nodes
    leader_node >> Edge(label="Distribute Large Queries") >> ds_node1
    leader_node >> Edge(label="Distribute Large Queries") >> ds_node2
    leader_node >> Edge(label="Distribute Large Queries") >> ds_node3
    leader_node >> Edge(label="Distribute Large Queries") >> ds_node4
    leader_node >> Edge(label="Distribute Large Queries") >> ds_node5
    leader_node >> Edge(label="Distribute Large Queries") >> ds_node6
    
    # Storage features integration
    ds_node1 >> Edge(label="Store") >> magnetic_storage
    ds_node2 >> Edge(label="Store") >> magnetic_storage
    ds_node3 >> Edge(label="Store") >> magnetic_storage
    ds_node4 >> Edge(label="Compress") >> compression
    ds_node5 >> Edge(label="Distribute") >> data_distribution
    ds_node6 >> Edge(label="Backup") >> backup_snapshots
    
    # Workload management for different use cases
    leader_node >> Edge(label="Route Heavy ETL") >> etl_heavy_queue
    leader_node >> Edge(label="Route Reports") >> reporting_queue
    leader_node >> Edge(label="Route Maintenance") >> maintenance_queue
    
    # Application connections optimized for large datasets
    etl_heavy_queue >> Edge(label="Long-running Queries") >> historical_reports
    reporting_queue >> Edge(label="Scheduled Reports") >> trend_analysis
    maintenance_queue >> Edge(label="Compliance Queries") >> compliance_reporting
    reporting_queue >> Edge(label="Archive Process") >> data_archival
    
    # Data lifecycle management
    data_archival >> Edge(label="Lifecycle Rules") >> data_retention
    data_retention >> Edge(label="Archive Old Data") >> automated_archival
    compliance_reporting >> Edge(label="Audit Trail") >> compliance_audit
    
    # Performance monitoring for storage
    ds_node1 >> Edge(label="Storage Metrics") >> storage_utilization
    ds_node2 >> Edge(label="I/O Metrics") >> io_performance
    ds_node3 >> Edge(label="Query Metrics") >> query_optimization
    
    # Results aggregation
    ds_node1 >> Edge(label="Query Results") >> leader_node
    ds_node2 >> Edge(label="Query Results") >> leader_node
    ds_node3 >> Edge(label="Query Results") >> leader_node
    ds_node4 >> Edge(label="Query Results") >> leader_node
    ds_node5 >> Edge(label="Query Results") >> leader_node
    ds_node6 >> Edge(label="Query Results") >> leader_node
    
    # Backup and disaster recovery
    magnetic_storage >> Edge(label="Snapshot") >> backup_snapshots
    backup_snapshots >> Edge(label="Long-term Storage") >> automated_archival

print("Redshift Dense Storage Node diagram generated successfully!")
