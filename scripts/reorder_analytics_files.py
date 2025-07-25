#!/usr/bin/env python3

import os
import shutil

# Define the correct order based on diagrams.aws.analytics
file_order = [
    ("01-amazon-opensearch-service.md", "opensearch-architecture.md"),
    ("02-analytics.md", "analytics.md"),
    ("03-athena.md", "athena-analytics.md"),
    ("04-cloudsearch-search-documents.md", "cloudsearch-search-documents.md"),
    ("05-cloudsearch.md", "cloudsearch-architecture.md"),
    ("06-data-lake-resource.md", "data-lake-resource.md"),
    ("07-data-pipeline.md", "data-pipeline.md"),
    ("08-elasticsearch-service.md", "elasticsearch-service.md"),
    ("09-emr-cluster.md", "emr-cluster.md"),
    ("10-emr-engine-mapr-m3.md", "emr-engine-mapr-m3.md"),
    ("11-emr-engine-mapr-m5.md", "emr-engine-mapr-m5.md"),
    ("12-emr-engine-mapr-m7.md", "emr-engine-mapr-m7.md"),
    ("13-emr-engine.md", "emr-engine.md"),
    ("14-emr-hdfs-cluster.md", "emr-hdfs-cluster.md"),
    ("15-emr.md", "emr.md"),
    ("16-glue-crawlers.md", "glue-crawlers.md"),
    ("17-glue-data-catalog.md", "glue-data-catalog.md"),
    ("18-glue.md", "glue.md"),
    ("19-kinesis-data-analytics.md", "kinesis-data-analytics.md"),
    ("20-kinesis-data-firehose.md", "kinesis-data-firehose.md"),
    ("21-kinesis-data-streams.md", "kinesis-data-streams.md"),
    ("22-kinesis-video-streams.md", "kinesis-video-streams.md"),
    ("23-kinesis.md", "kinesis.md"),
    ("24-lake-formation.md", "lake-formation.md"),
    ("25-managed-streaming-for-kafka.md", "managed-streaming-for-kafka.md"),
    ("26-quicksight.md", "quicksight.md"),
    ("27-redshift-dense-compute-node.md", "redshift-dense-compute-node.md"),
    ("28-redshift-dense-storage-node.md", "redshift-dense-storage-node.md"),
    ("29-redshift.md", "redshift.md"),
]

base_path = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/docs/aws-nodes/aws-analytics"

def rename_files():
    """Rename files with order prefixes"""
    
    # First, rename all files to temporary names to avoid conflicts
    temp_files = []
    for new_name, current_name in file_order:
        current_path = os.path.join(base_path, current_name)
        temp_path = os.path.join(base_path, f"temp_{new_name}")
        
        if os.path.exists(current_path):
            shutil.move(current_path, temp_path)
            temp_files.append((temp_path, os.path.join(base_path, new_name)))
            print(f"Moved {current_name} to temp_{new_name}")
    
    # Then rename temp files to final names
    for temp_path, final_path in temp_files:
        shutil.move(temp_path, final_path)
        print(f"Renamed {os.path.basename(temp_path)} to {os.path.basename(final_path)}")

if __name__ == "__main__":
    rename_files()
    print("File renaming completed!")
