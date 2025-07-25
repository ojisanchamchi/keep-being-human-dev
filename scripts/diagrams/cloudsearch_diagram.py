#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Cloudsearch, CloudsearchSearchDocuments
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon CloudSearch Complete Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/cloudsearch-architecture",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Website Visitors")
    
    with Cluster("DNS & CDN Layer"):
        dns = Route53("Route 53")
        cdn = CloudFront("CloudFront")
    
    with Cluster("Application Layer"):
        load_balancer = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    
    with Cluster("Search Infrastructure"):
        cloudsearch_domain = Cloudsearch("CloudSearch Domain")
        search_api = CloudsearchSearchDocuments("Search API")
    
    with Cluster("Data Sources"):
        primary_db = RDS("Primary Database")
        nosql_db = Dynamodb("Product Catalog")
        content_storage = S3("Content Storage")
    
    with Cluster("Data Processing"):
        index_queue = SQS("Indexing Queue")
        indexer_lambda = Lambda("Document Indexer")
        search_lambda = Lambda("Search Processor")
        notification = SNS("Search Notifications")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # User search flow
    users >> dns >> cdn >> load_balancer
    load_balancer >> web_servers
    web_servers >> Edge(label="Search Query") >> search_lambda
    search_lambda >> search_api
    search_api >> cloudsearch_domain
    cloudsearch_domain >> Edge(label="Results") >> search_api
    search_api >> search_lambda >> web_servers
    
    # Data indexing flow
    primary_db >> Edge(label="Data Changes") >> index_queue
    nosql_db >> Edge(label="Product Updates") >> index_queue
    content_storage >> Edge(label="New Content") >> index_queue
    
    index_queue >> indexer_lambda
    indexer_lambda >> Edge(label="Index Documents") >> cloudsearch_domain
    indexer_lambda >> Edge(label="Status Updates") >> notification
    
    # Monitoring and security
    cloudsearch_domain >> Edge(label="Metrics") >> monitoring
    search_lambda >> Edge(label="Search Analytics") >> monitoring
    security >> Edge(label="Access Control") >> cloudsearch_domain
    security >> Edge(label="API Permissions") >> search_api

print("CloudSearch complete architecture diagram generated successfully!")
