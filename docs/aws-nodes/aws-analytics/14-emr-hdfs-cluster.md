# EMR HDFS Cluster

## Tổng quan

EMR HDFS Cluster là node đại diện cho Amazon EMR cluster với Hadoop Distributed File System (HDFS) làm primary storage layer. HDFS cung cấp high-throughput access đến application data và fault-tolerant storage cho big data applications. Node này biểu thị kiến trúc EMR cluster tối ưu cho workloads đòi hỏi high-performance local storage và data locality.

## Chức năng chính

### 1. HDFS Storage System
- **Distributed Storage**: Phân tán dữ liệu trên multiple nodes
- **Fault Tolerance**: Automatic replication và recovery
- **High Throughput**: Optimized cho sequential read/write
- **Data Locality**: Co-locate computation với data

### 2. Cluster Architecture
- **NameNode**: Metadata management và namespace
- **DataNodes**: Actual data storage và retrieval
- **Secondary NameNode**: Checkpoint và backup metadata
- **Block Management**: Efficient data block distribution

### 3. Performance Features
- **Block-based Storage**: Large block sizes cho efficiency
- **Replication Strategy**: Configurable replication factor
- **Rack Awareness**: Optimize placement across racks
- **Compression**: Built-in compression support

### 4. Integration Capabilities
- **Hadoop Ecosystem**: Native integration với Hadoop tools
- **Spark Integration**: Direct HDFS access từ Spark
- **Hive/HBase**: Warehouse và NoSQL database support
- **MapReduce**: Optimized cho MapReduce workloads

## Use Cases phổ biến

1. **Data Warehousing**: Large-scale data warehouse storage
2. **Log Processing**: Centralized log storage và processing
3. **Batch Analytics**: High-throughput batch processing
4. **Data Archival**: Long-term data retention
5. **ETL Workloads**: Extract, transform, load operations

## Diagram Architecture

Kiến trúc EMR HDFS Cluster với distributed storage:

![EMR HDFS Cluster Architecture](/img/aws-analytics/emr-hdfs-cluster.png)

### Code để tạo diagram:

```python
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

with Diagram("EMR HDFS Cluster Architecture", show=False, direction="TB"):
    
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
```

## HDFS Architecture

### 1. NameNode Configuration
```xml
<!-- hdfs-site.xml for NameNode -->
<configuration>
  <property>
    <name>dfs.nameservices</name>
    <value>emr-cluster</value>
  </property>
  
  <property>
    <name>dfs.ha.namenodes.emr-cluster</name>
    <value>nn1,nn2</value>
  </property>
  
  <property>
    <name>dfs.namenode.rpc-address.emr-cluster.nn1</name>
    <value>master1:8020</value>
  </property>
  
  <property>
    <name>dfs.namenode.http-address.emr-cluster.nn1</name>
    <value>master1:50070</value>
  </property>
  
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/mnt/hdfs/namenode</value>
  </property>
  
  <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
  
  <property>
    <name>dfs.blocksize</name>
    <value>134217728</value> <!-- 128MB -->
  </property>
</configuration>
```

### 2. DataNode Configuration
```xml
<!-- hdfs-site.xml for DataNode -->
<configuration>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/mnt/hdfs/datanode1,/mnt/hdfs/datanode2</value>
  </property>
  
  <property>
    <name>dfs.datanode.handler.count</name>
    <value>40</value>
  </property>
  
  <property>
    <name>dfs.datanode.max.transfer.threads</name>
    <value>8192</value>
  </property>
  
  <property>
    <name>dfs.datanode.balance.bandwidthPerSec</name>
    <value>104857600</value> <!-- 100MB/s -->
  </property>
  
  <property>
    <name>dfs.datanode.failed.volumes.tolerated</name>
    <value>1</value>
  </property>
</configuration>
```

### 3. Block Management
```bash
# HDFS block management commands
# Check filesystem health
hdfs fsck / -files -blocks -locations

# Balance cluster
hdfs balancer -threshold 5

# Set replication factor
hdfs dfsadmin -setDefaultReplication 3

# Decommission nodes
hdfs dfsadmin -refreshNodes

# Safe mode operations
hdfs dfsadmin -safemode enter
hdfs dfsadmin -safemode leave
```

## Storage Optimization

### 1. Block Size Tuning
```python
# Optimal block size calculation
def calculate_optimal_block_size(file_size_gb, cluster_size):
    """
    Calculate optimal HDFS block size based on file size and cluster
    """
    file_size_bytes = file_size_gb * 1024 * 1024 * 1024
    
    # Rule of thumb: aim for 100-1000 blocks per file
    target_blocks = min(1000, max(100, cluster_size * 2))
    optimal_block_size = file_size_bytes / target_blocks
    
    # Round to nearest power of 2, minimum 64MB, maximum 1GB
    block_size = max(64 * 1024 * 1024, 
                    min(1024 * 1024 * 1024, 
                        2 ** round(math.log2(optimal_block_size))))
    
    return block_size

# Example usage
file_size = 100  # GB
cluster_nodes = 20
optimal_size = calculate_optimal_block_size(file_size, cluster_nodes)
print(f"Optimal block size: {optimal_size / (1024*1024)} MB")
```

### 2. Compression Strategy
```java
// Hadoop compression configuration
Configuration conf = new Configuration();

// Enable compression
conf.setBoolean("mapreduce.map.output.compress", true);
conf.setClass("mapreduce.map.output.compress.codec", 
              SnappyCodec.class, CompressionCodec.class);

conf.setBoolean("mapreduce.output.fileoutputformat.compress", true);
conf.setClass("mapreduce.output.fileoutputformat.compress.codec",
              GzipCodec.class, CompressionCodec.class);

// Sequence file compression
conf.setClass("mapreduce.output.fileoutputformat.compress.type",
              SequenceFile.CompressionType.BLOCK, 
              SequenceFile.CompressionType.class);

// Parquet compression
conf.set("parquet.compression", "SNAPPY");
```

### 3. Data Placement Strategy
```bash
# Rack awareness configuration
# /etc/hadoop/conf/rack-topology.sh
#!/bin/bash
while [ $# -gt 0 ] ; do
  nodeArg=$1
  exec< /etc/hadoop/conf/rack-topology.data
  result=""
  while read line ; do
    ar=( $line )
    if [ "${ar[0]}" = "$nodeArg" ] ; then
      result="${ar[1]}"
    fi
  done
  shift
  if [ -z "$result" ] ; then
    echo -n "/default-rack "
  else
    echo -n "$result "
  fi
done

# rack-topology.data
ip-10-0-1-100 /rack1
ip-10-0-1-101 /rack1
ip-10-0-2-100 /rack2
ip-10-0-2-101 /rack2
```

## Performance Tuning

### 1. Memory Configuration
```xml
<!-- mapred-site.xml -->
<configuration>
  <property>
    <name>mapreduce.map.memory.mb</name>
    <value>4096</value>
  </property>
  
  <property>
    <name>mapreduce.reduce.memory.mb</name>
    <value>8192</value>
  </property>
  
  <property>
    <name>mapreduce.map.java.opts</name>
    <value>-Xmx3276m</value>
  </property>
  
  <property>
    <name>mapreduce.reduce.java.opts</name>
    <value>-Xmx6553m</value>
  </property>
  
  <property>
    <name>yarn.app.mapreduce.am.resource.mb</name>
    <value>2048</value>
  </property>
</configuration>
```

### 2. I/O Optimization
```xml
<!-- core-site.xml -->
<configuration>
  <property>
    <name>io.file.buffer.size</name>
    <value>131072</value> <!-- 128KB -->
  </property>
  
  <property>
    <name>fs.local.block.size</name>
    <value>134217728</value> <!-- 128MB -->
  </property>
  
  <property>
    <name>io.sort.mb</name>
    <value>512</value>
  </property>
  
  <property>
    <name>io.sort.factor</name>
    <value>100</value>
  </property>
</configuration>
```

### 3. Network Optimization
```bash
# Network tuning for HDFS
echo 'net.core.rmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_rmem = 4096 87380 134217728' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_wmem = 4096 65536 134217728' >> /etc/sysctl.conf
echo 'net.core.netdev_max_backlog = 5000' >> /etc/sysctl.conf

sysctl -p
```

## Data Management

### 1. Data Lifecycle Management
```python
# HDFS data lifecycle automation
import subprocess
import datetime
from pathlib import Path

class HDFSLifecycleManager:
    def __init__(self, hdfs_client):
        self.hdfs_client = hdfs_client
    
    def archive_old_data(self, path, days_old=90):
        """Archive data older than specified days"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
        
        # List files in path
        files = self.hdfs_client.list(path, status=True)
        
        for file_info in files:
            if file_info.modification_time < cutoff_date.timestamp():
                # Move to archive
                archive_path = f"/archive/{file_info.path}"
                self.hdfs_client.rename(file_info.path, archive_path)
                print(f"Archived: {file_info.path} -> {archive_path}")
    
    def compress_data(self, path, compression='gzip'):
        """Compress data in specified path"""
        cmd = [
            'hadoop', 'jar', 
            '/opt/hadoop/share/hadoop/tools/lib/hadoop-archive-*.jar',
            '-archiveName', f'archive_{datetime.date.today()}.har',
            '-p', path, '/compressed/'
        ]
        subprocess.run(cmd, check=True)
    
    def cleanup_temp_data(self, temp_path='/tmp'):
        """Clean up temporary data"""
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
        
        files = self.hdfs_client.list(temp_path, status=True)
        for file_info in files:
            if file_info.modification_time < cutoff.timestamp():
                self.hdfs_client.delete(file_info.path, recursive=True)
```

### 2. Data Quality Monitoring
```python
# HDFS data quality checks
class HDFSDataQualityMonitor:
    def __init__(self, spark_session):
        self.spark = spark_session
    
    def check_data_freshness(self, path, max_age_hours=24):
        """Check if data is fresh enough"""
        df = self.spark.read.parquet(path)
        
        # Assuming there's a timestamp column
        latest_timestamp = df.agg({"timestamp": "max"}).collect()[0][0]
        age_hours = (datetime.datetime.now() - latest_timestamp).total_seconds() / 3600
        
        return {
            'path': path,
            'latest_timestamp': latest_timestamp,
            'age_hours': age_hours,
            'is_fresh': age_hours <= max_age_hours
        }
    
    def check_data_completeness(self, path, expected_partitions):
        """Check if all expected partitions exist"""
        df = self.spark.read.parquet(path)
        actual_partitions = df.select("date_partition").distinct().count()
        
        return {
            'path': path,
            'expected_partitions': expected_partitions,
            'actual_partitions': actual_partitions,
            'completeness_ratio': actual_partitions / expected_partitions
        }
    
    def check_schema_consistency(self, paths):
        """Check schema consistency across multiple paths"""
        schemas = {}
        for path in paths:
            df = self.spark.read.parquet(path)
            schemas[path] = df.schema
        
        # Compare schemas
        base_schema = list(schemas.values())[0]
        inconsistencies = []
        
        for path, schema in schemas.items():
            if schema != base_schema:
                inconsistencies.append({
                    'path': path,
                    'schema_diff': self.compare_schemas(base_schema, schema)
                })
        
        return inconsistencies
```

## Backup và Recovery

### 1. HDFS Backup Strategy
```bash
#!/bin/bash
# HDFS backup script

BACKUP_DATE=$(date +%Y%m%d)
BACKUP_PATH="/backup/$BACKUP_DATE"
SOURCE_PATH="/data"

# Create backup directory
hdfs dfs -mkdir -p $BACKUP_PATH

# Backup using distcp
hadoop distcp \
  -update \
  -delete \
  -skipcrccheck \
  $SOURCE_PATH \
  $BACKUP_PATH

# Backup to S3
hadoop distcp \
  -update \
  -delete \
  hdfs://cluster$SOURCE_PATH \
  s3a://backup-bucket/hdfs-backup/$BACKUP_DATE/

# Verify backup
hdfs fsck $BACKUP_PATH -files -blocks

echo "Backup completed: $BACKUP_PATH"
```

### 2. Disaster Recovery
```python
# HDFS disaster recovery automation
class HDFSDisasterRecovery:
    def __init__(self, primary_cluster, backup_cluster):
        self.primary = primary_cluster
        self.backup = backup_cluster
    
    def create_recovery_plan(self, critical_paths):
        """Create disaster recovery plan"""
        recovery_plan = {
            'timestamp': datetime.datetime.now(),
            'critical_paths': critical_paths,
            'recovery_steps': []
        }
        
        for path in critical_paths:
            # Check data size and replication
            size_info = self.get_path_size(path)
            recovery_plan['recovery_steps'].append({
                'path': path,
                'size_gb': size_info['size_gb'],
                'estimated_recovery_time': size_info['size_gb'] / 10,  # 10GB/min
                'priority': self.get_path_priority(path)
            })
        
        return recovery_plan
    
    def execute_recovery(self, recovery_plan):
        """Execute disaster recovery"""
        # Sort by priority
        steps = sorted(recovery_plan['recovery_steps'], 
                      key=lambda x: x['priority'], reverse=True)
        
        for step in steps:
            print(f"Recovering {step['path']}...")
            
            # Restore from backup
            self.restore_from_backup(step['path'])
            
            # Verify data integrity
            if self.verify_data_integrity(step['path']):
                print(f"✓ Successfully recovered {step['path']}")
            else:
                print(f"✗ Failed to recover {step['path']}")
    
    def restore_from_backup(self, path):
        """Restore data from backup"""
        backup_path = f"s3a://backup-bucket/hdfs-backup/latest{path}"
        
        cmd = [
            'hadoop', 'distcp',
            '-overwrite',
            backup_path,
            f'hdfs://cluster{path}'
        ]
        
        subprocess.run(cmd, check=True)
```

## Monitoring và Alerting

### 1. HDFS Health Monitoring
```python
# HDFS health monitoring
import requests
import json

class HDFSHealthMonitor:
    def __init__(self, namenode_host, namenode_port=50070):
        self.base_url = f"http://{namenode_host}:{namenode_port}"
    
    def get_cluster_info(self):
        """Get cluster information"""
        response = requests.get(f"{self.base_url}/jmx?qry=Hadoop:service=NameNode,name=FSNamesystemState")
        data = response.json()
        
        return {
            'total_capacity': data['beans'][0]['CapacityTotal'],
            'used_capacity': data['beans'][0]['CapacityUsed'],
            'remaining_capacity': data['beans'][0]['CapacityRemaining'],
            'capacity_used_percent': data['beans'][0]['PercentUsed'],
            'live_nodes': data['beans'][0]['NumLiveDataNodes'],
            'dead_nodes': data['beans'][0]['NumDeadDataNodes']
        }
    
    def check_datanode_health(self):
        """Check DataNode health"""
        response = requests.get(f"{self.base_url}/jmx?qry=Hadoop:service=NameNode,name=FSNamesystem")
        data = response.json()
        
        under_replicated = data['beans'][0]['UnderReplicatedBlocks']
        corrupt_blocks = data['beans'][0]['CorruptBlocks']
        missing_blocks = data['beans'][0]['MissingBlocks']
        
        return {
            'under_replicated_blocks': under_replicated,
            'corrupt_blocks': corrupt_blocks,
            'missing_blocks': missing_blocks,
            'health_status': 'healthy' if (under_replicated + corrupt_blocks + missing_blocks) == 0 else 'unhealthy'
        }
    
    def generate_health_report(self):
        """Generate comprehensive health report"""
        cluster_info = self.get_cluster_info()
        datanode_health = self.check_datanode_health()
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'cluster_info': cluster_info,
            'datanode_health': datanode_health,
            'alerts': []
        }
        
        # Generate alerts
        if cluster_info['capacity_used_percent'] > 80:
            report['alerts'].append('High disk usage: {}%'.format(cluster_info['capacity_used_percent']))
        
        if cluster_info['dead_nodes'] > 0:
            report['alerts'].append('{} DataNodes are dead'.format(cluster_info['dead_nodes']))
        
        if datanode_health['corrupt_blocks'] > 0:
            report['alerts'].append('{} corrupt blocks detected'.format(datanode_health['corrupt_blocks']))
        
        return report
```

## Best Practices

1. **Capacity Planning**: Monitor disk usage và plan expansion
2. **Replication Strategy**: Set appropriate replication factor
3. **Block Size Optimization**: Choose optimal block size cho workload
4. **Rack Awareness**: Configure rack topology
5. **Regular Maintenance**: Schedule regular fsck và balancer
6. **Backup Strategy**: Implement comprehensive backup plan
7. **Security**: Enable Kerberos và encryption
8. **Monitoring**: Set up proactive monitoring và alerting

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Backup và archival storage
- **Amazon EBS**: High-performance local storage
- **AWS Direct Connect**: High-bandwidth data transfer
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Access control và security
- **Amazon VPC**: Network isolation
- **AWS KMS**: Encryption key management
- **AWS Glue**: Data catalog integration
- **Amazon EMR**: Managed Hadoop ecosystem
- **Amazon Kinesis**: Real-time data ingestion
