#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import CloudsearchSearchDocuments, Cloudsearch
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.integration import SQS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("CloudSearch Document Search Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/cloudsearch-search-documents",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("End Users")
    
    with Cluster("Frontend Layer"):
        cdn = CloudFront("CloudFront CDN")
        load_balancer = ELB("Application Load Balancer")
        web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    
    with Cluster("Search Layer"):
        search_docs = CloudsearchSearchDocuments("Search Documents API")
        cloudsearch = Cloudsearch("CloudSearch Domain")
    
    with Cluster("Data Sources"):
        database = RDS("Product Database")
        content_storage = S3("Content Storage")
        search_queue = SQS("Index Queue")
    
    with Cluster("Processing Layer"):
        indexer = Lambda("Document Indexer")
        search_analytics = Lambda("Search Analytics")
        monitoring = Cloudwatch("Search Monitoring")
    
    # User search flow
    users >> Edge(label="Search Query") >> cdn
    cdn >> load_balancer
    load_balancer >> web_servers
    web_servers >> Edge(label="Search Request") >> search_docs
    search_docs >> Edge(label="Query Processing") >> cloudsearch
    cloudsearch >> Edge(label="Search Results") >> search_docs
    search_docs >> Edge(label="Formatted Results") >> web_servers
    
    # Data indexing flow
    database >> Edge(label="Data Changes") >> search_queue
    content_storage >> Edge(label="New Content") >> search_queue
    search_queue >> indexer
    indexer >> Edge(label="Index Documents") >> cloudsearch
    
    # Analytics and monitoring
    search_docs >> Edge(label="Search Metrics") >> search_analytics
    search_analytics >> monitoring
    cloudsearch >> Edge(label="Performance Metrics") >> monitoring

print("CloudSearch Search Documents diagram generated successfully!")
