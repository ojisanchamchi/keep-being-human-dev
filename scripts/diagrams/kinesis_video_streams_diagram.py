#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisVideoStreams
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.ml import Rekognition, SagemakerModel
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon Kinesis Video Streams Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/kinesis-video-streams",
             graph_attr={"fontsize": "16", "bgcolor": "white"}):
    
    users = Users("Operators")
    
    with Cluster("Video Sources"):
        security_cameras = Mobile("Security Cameras")
        mobile_devices = Lambda("Mobile Devices")
        drones = Mobile("Drones")
        iot_cameras = Mobile("IoT Cameras")
        webcams = EC2("Web Cameras")
    
    with Cluster("Kinesis Video Streams"):
        video_stream = KinesisVideoStreams("Video Stream")
        
        with Cluster("Stream Components"):
            fragments = KinesisVideoStreams("Video Fragments")
            metadata = KinesisVideoStreams("Metadata")
            index = KinesisVideoStreams("Time Index")
    
    with Cluster("Real-time Processing"):
        rekognition = Rekognition("Video Analysis")
        lambda_processor = Lambda("Custom Processing")
        ml_inference = SagemakerModel("ML Inference")
    
    with Cluster("Storage & Archival"):
        s3_archive = S3("Video Archive")
        s3_thumbnails = S3("Thumbnails")
        s3_analytics = S3("Analytics Results")
    
    with Cluster("Playback & Streaming"):
        hls_endpoint = Lambda("HLS Endpoint")
        dash_endpoint = Lambda("DASH Endpoint")
        webrtc_endpoint = Lambda("WebRTC Endpoint")
        custom_player = EC2("Custom Player")
    
    with Cluster("Alerts & Notifications"):
        alert_system = SNS("Alert System")
        notification_queue = SQS("Notification Queue")
        dashboard = Lambda("Monitoring Dashboard")
    
    with Cluster("Monitoring & Security"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Video ingestion
    security_cameras >> Edge(label="RTSP/WebRTC") >> video_stream
    mobile_devices >> Edge(label="SDK") >> video_stream
    drones >> Edge(label="Live Feed") >> video_stream
    iot_cameras >> Edge(label="H.264/H.265") >> video_stream
    webcams >> Edge(label="USB/IP") >> video_stream
    
    # Stream components
    video_stream >> fragments
    video_stream >> metadata
    video_stream >> index
    
    # Real-time processing
    fragments >> Edge(label="Frame Analysis") >> rekognition
    fragments >> Edge(label="Custom Logic") >> lambda_processor
    fragments >> Edge(label="ML Models") >> ml_inference
    
    # Storage and archival
    fragments >> Edge(label="Archive") >> s3_archive
    rekognition >> Edge(label="Thumbnails") >> s3_thumbnails
    lambda_processor >> Edge(label="Results") >> s3_analytics
    
    # Playback endpoints
    fragments >> hls_endpoint
    fragments >> dash_endpoint
    fragments >> webrtc_endpoint
    fragments >> custom_player
    
    # Alerts and notifications
    rekognition >> Edge(label="Object Detection") >> alert_system
    ml_inference >> Edge(label="Anomaly Detection") >> notification_queue
    lambda_processor >> Edge(label="Custom Alerts") >> dashboard
    
    # User interaction
    users >> Edge(label="Live View") >> hls_endpoint
    users >> Edge(label="Playback") >> custom_player
    users >> Edge(label="Monitor") >> dashboard
    
    # Monitoring and security
    video_stream >> Edge(label="Metrics") >> cloudwatch
    security >> Edge(label="Access Control") >> video_stream

print("Kinesis Video Streams diagram generated successfully!")
