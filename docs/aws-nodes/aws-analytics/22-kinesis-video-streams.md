# Amazon Kinesis Video Streams

## Tổng quan

Amazon Kinesis Video Streams là node đại diện cho dịch vụ streaming video được quản lý hoàn toàn của AWS. Dịch vụ này giúp bạn dễ dàng stream video từ connected devices đến AWS cho analytics, machine learning, playback, và các processing khác. Kinesis Video Streams tự động provision và scale infrastructure cần thiết để ingest streaming video data từ millions of devices.

## Chức năng chính

### 1. Video Ingestion
- **Multi-device Support**: Cameras, smartphones, drones, IoT devices
- **Real-time Streaming**: Low-latency video streaming
- **Durable Storage**: Automatic storage với configurable retention
- **Multiple Formats**: H.264, H.265, và custom formats

### 2. Stream Management
- **Auto Scaling**: Tự động scale based on ingestion rate
- **Fragment-based Storage**: Efficient video fragment management
- **Time-indexed Access**: Access video by timestamp
- **Metadata Support**: Custom metadata với video fragments

### 3. Processing Integration
- **Amazon Rekognition**: Video analysis và object detection
- **AWS Lambda**: Custom video processing
- **Amazon SageMaker**: Machine learning inference
- **Third-party Analytics**: Integration với external services

### 4. Playback và Access
- **HLS Streaming**: HTTP Live Streaming support
- **DASH Streaming**: Dynamic Adaptive Streaming
- **WebRTC**: Real-time communication
- **Custom Applications**: SDK-based access

## Use Cases phổ biến

1. **Security Surveillance**: Real-time monitoring và alerts
2. **Smart Home**: Home automation và monitoring
3. **Industrial IoT**: Equipment monitoring và predictive maintenance
4. **Retail Analytics**: Customer behavior analysis
5. **Healthcare**: Remote patient monitoring

## Diagram Architecture

Kiến trúc Amazon Kinesis Video Streams với video processing pipeline:

![Amazon Kinesis Video Streams Architecture](/img/aws-analytics/kinesis-video-streams.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisVideoStreams
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.ml import Rekognition, SagemakerModel
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.iot import IotSensor

with Diagram("Amazon Kinesis Video Streams Architecture", show=False, direction="TB"):
    
    users = Users("Operators")
    
    with Cluster("Video Sources"):
        security_cameras = IotSensor("Security Cameras")
        mobile_devices = Lambda("Mobile Devices")
        drones = IotSensor("Drones")
        iot_cameras = IotSensor("IoT Cameras")
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
```

## Video Stream Setup

### 1. Stream Creation và Configuration
```python
import boto3
import json
from datetime import datetime

kvs = boto3.client('kinesisvideo')

def create_video_stream(stream_name, retention_hours=24):
    """Create Kinesis Video Stream"""
    
    try:
        response = kvs.create_stream(
            StreamName=stream_name,
            DataRetentionInHours=retention_hours,
            MediaType='video/h264',
            DeviceName='security-camera-01',
            Tags={
                'Environment': 'production',
                'Application': 'security-monitoring',
                'Owner': 'security-team'
            }
        )
        
        print(f"Video stream {stream_name} created successfully")
        return response
        
    except kvs.exceptions.ResourceInUseException:
        print(f"Stream {stream_name} already exists")
        return None

def configure_stream_settings(stream_name):
    """Configure advanced stream settings"""
    
    # Update stream configuration
    kvs.update_stream(
        StreamName=stream_name,
        CurrentVersion='1.0',
        MediaType='video/h264,audio/aac',  # Video with audio
        DeviceName='security-camera-01'
    )
    
    # Set up stream processor for real-time analysis
    kvs.create_stream_processor(
        ProcessorName=f'{stream_name}-processor',
        Inputs=[
            {
                'KinesisVideoStream': {
                    'StreamName': stream_name
                }
            }
        ],
        Output={
            'KinesisDataStream': {
                'StreamName': f'{stream_name}-analysis-results'
            }
        },
        Settings={
            'FaceSearch': {
                'CollectionId': 'security-faces',
                'FaceMatchThreshold': 85.0
            }
        },
        RoleArn='arn:aws:iam::account:role/KinesisVideoStreamProcessorRole'
    )

def get_stream_endpoint(stream_name, api_name):
    """Get stream endpoint for different APIs"""
    
    response = kvs.get_data_endpoint(
        StreamName=stream_name,
        APIName=api_name  # GET_MEDIA, GET_MEDIA_FOR_FRAGMENT_LIST, PUT_MEDIA, etc.
    )
    
    return response['DataEndpoint']
```

### 2. Video Producer Implementation
```python
import cv2
import boto3
import threading
import time
from datetime import datetime

class KinesisVideoProducer:
    def __init__(self, stream_name, region='us-west-2'):
        self.stream_name = stream_name
        self.region = region
        self.kvs = boto3.client('kinesisvideo', region_name=region)
        self.is_streaming = False
        
    def start_camera_stream(self, camera_index=0):
        """Start streaming from camera"""
        
        # Get PUT_MEDIA endpoint
        endpoint = self.kvs.get_data_endpoint(
            StreamName=self.stream_name,
            APIName='PUT_MEDIA'
        )['DataEndpoint']
        
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.is_streaming = True
        
        try:
            while self.is_streaming:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Encode frame
                encoded_frame = self.encode_frame(frame)
                
                # Send to Kinesis Video Streams
                self.send_frame(encoded_frame, endpoint)
                
                # Control frame rate
                time.sleep(1/30)  # 30 FPS
                
        finally:
            cap.release()
    
    def encode_frame(self, frame):
        """Encode frame to H.264"""
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Encode to H.264 (simplified - use proper encoder in production)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, encoded_frame = cv2.imencode('.jpg', rgb_frame, encode_param)
        
        return encoded_frame.tobytes()
    
    def send_frame(self, frame_data, endpoint):
        """Send frame to Kinesis Video Streams"""
        
        # Create PUT_MEDIA client
        kvs_media = boto3.client(
            'kinesis-video-media',
            endpoint_url=endpoint,
            region_name=self.region
        )
        
        try:
            # Send frame with metadata
            response = kvs_media.put_media(
                StreamName=self.stream_name,
                FragmentTimecodeType='ABSOLUTE',
                ProducerStartTimestamp=datetime.utcnow(),
                Payload=frame_data
            )
            
        except Exception as e:
            print(f"Error sending frame: {str(e)}")
    
    def stop_streaming(self):
        """Stop video streaming"""
        self.is_streaming = False

# Usage example
def start_security_camera():
    """Start security camera streaming"""
    
    producer = KinesisVideoProducer('security-camera-01')
    
    # Start streaming in separate thread
    streaming_thread = threading.Thread(
        target=producer.start_camera_stream,
        args=(0,)  # Camera index
    )
    streaming_thread.start()
    
    return producer, streaming_thread
```

### 3. Advanced Producer với GStreamer
```python
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import boto3

class GStreamerKinesisProducer:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.kvs = boto3.client('kinesisvideo')
        
        # Initialize GStreamer
        Gst.init(None)
        
        # Create pipeline
        self.pipeline = self.create_pipeline()
        
    def create_pipeline(self):
        """Create GStreamer pipeline for Kinesis Video Streams"""
        
        # Get stream endpoint
        endpoint = self.kvs.get_data_endpoint(
            StreamName=self.stream_name,
            APIName='PUT_MEDIA'
        )['DataEndpoint']
        
        # Pipeline elements
        pipeline_str = f"""
        v4l2src device=/dev/video0 ! 
        videoconvert ! 
        video/x-raw,format=I420,width=1280,height=720,framerate=30/1 ! 
        x264enc speed-preset=ultrafast tune=zerolatency key-int-max=45 bframes=0 ! 
        video/x-h264,stream-format=avc,alignment=au,profile=baseline ! 
        kvssink stream-name={self.stream_name} 
                 aws-region=us-west-2 
                 endpoint-uri={endpoint}
        """
        
        pipeline = Gst.parse_launch(pipeline_str)
        return pipeline
    
    def start_streaming(self):
        """Start GStreamer pipeline"""
        
        # Set pipeline to playing state
        ret = self.pipeline.set_state(Gst.State.PLAYING)
        
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Failed to start pipeline")
            return False
        
        print(f"Started streaming to {self.stream_name}")
        return True
    
    def stop_streaming(self):
        """Stop GStreamer pipeline"""
        
        self.pipeline.set_state(Gst.State.NULL)
        print("Stopped streaming")
```

## Video Processing và Analytics

### 1. Real-time Video Analysis
```python
import boto3
import json
from datetime import datetime

class VideoAnalyticsProcessor:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.rekognition = boto3.client('rekognition')
        self.kvs = boto3.client('kinesisvideo')
        
    def start_face_detection(self):
        """Start real-time face detection"""
        
        response = self.rekognition.start_face_detection(
            Video={
                'KinesisVideoStream': {
                    'Arn': f'arn:aws:kinesisvideo:region:account:stream/{self.stream_name}'
                }
            },
            NotificationChannel={
                'SNSTopicArn': 'arn:aws:sns:region:account:video-analysis-results',
                'RoleArn': 'arn:aws:iam::account:role/RekognitionServiceRole'
            },
            FaceAttributes='ALL',
            JobTag='security-face-detection'
        )
        
        return response['JobId']
    
    def start_person_tracking(self):
        """Start person tracking in video stream"""
        
        response = self.rekognition.start_person_tracking(
            Video={
                'KinesisVideoStream': {
                    'Arn': f'arn:aws:kinesisvideo:region:account:stream/{self.stream_name}'
                }
            },
            NotificationChannel={
                'SNSTopicArn': 'arn:aws:sns:region:account:person-tracking-results',
                'RoleArn': 'arn:aws:iam::account:role/RekognitionServiceRole'
            },
            JobTag='security-person-tracking'
        )
        
        return response['JobId']
    
    def start_label_detection(self):
        """Start object and scene detection"""
        
        response = self.rekognition.start_label_detection(
            Video={
                'KinesisVideoStream': {
                    'Arn': f'arn:aws:kinesisvideo:region:account:stream/{self.stream_name}'
                }
            },
            MinConfidence=80.0,
            NotificationChannel={
                'SNSTopicArn': 'arn:aws:sns:region:account:label-detection-results',
                'RoleArn': 'arn:aws:iam::account:role/RekognitionServiceRole'
            },
            Features=['GENERAL_LABELS', 'MODERATION_LABELS'],
            JobTag='security-object-detection'
        )
        
        return response['JobId']
    
    def process_analysis_results(self, job_id, job_type):
        """Process analysis results"""
        
        if job_type == 'FACE_DETECTION':
            response = self.rekognition.get_face_detection(JobId=job_id)
        elif job_type == 'PERSON_TRACKING':
            response = self.rekognition.get_person_tracking(JobId=job_id)
        elif job_type == 'LABEL_DETECTION':
            response = self.rekognition.get_label_detection(JobId=job_id)
        
        # Process results
        results = []
        for item in response.get('Faces', response.get('Persons', response.get('Labels', []))):
            result = {
                'timestamp': item.get('Timestamp', 0),
                'confidence': item.get('Face', item.get('Person', item.get('Label', {}))).get('Confidence', 0),
                'bounding_box': item.get('Face', item.get('Person', {})).get('BoundingBox', {}),
                'attributes': item.get('Face', {}).get('Attributes', {}),
                'detected_at': datetime.utcnow().isoformat()
            }
            results.append(result)
        
        return results
```

### 2. Custom Video Processing với Lambda
```python
import json
import boto3
import base64
from datetime import datetime

def lambda_handler(event, context):
    """Process Kinesis Video Stream fragments"""
    
    kvs = boto3.client('kinesisvideo')
    
    # Parse SNS notification from Rekognition
    for record in event['Records']:
        if record['EventSource'] == 'aws:sns':
            message = json.loads(record['Sns']['Message'])
            
            if message['Status'] == 'SUCCEEDED':
                # Process successful analysis
                process_video_analysis(message)
            else:
                # Handle failed analysis
                handle_analysis_failure(message)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Video processing completed')
    }

def process_video_analysis(message):
    """Process video analysis results"""
    
    job_id = message['JobId']
    job_tag = message.get('JobTag', '')
    
    if 'face-detection' in job_tag:
        process_face_detection_results(job_id)
    elif 'person-tracking' in job_tag:
        process_person_tracking_results(job_id)
    elif 'object-detection' in job_tag:
        process_object_detection_results(job_id)

def process_face_detection_results(job_id):
    """Process face detection results"""
    
    rekognition = boto3.client('rekognition')
    dynamodb = boto3.resource('dynamodb')
    
    # Get face detection results
    response = rekognition.get_face_detection(JobId=job_id)
    
    # Store results in DynamoDB
    table = dynamodb.Table('video-analysis-results')
    
    for face in response['Faces']:
        # Check if face matches known individuals
        if face['Face']['Confidence'] > 90:
            # Search in face collection
            search_response = rekognition.search_faces_by_image(
                CollectionId='security-faces',
                Image={'Bytes': get_face_image_bytes(face)},
                MaxFaces=1,
                FaceMatchThreshold=85
            )
            
            # Store result
            table.put_item(
                Item={
                    'job_id': job_id,
                    'timestamp': face['Timestamp'],
                    'face_confidence': face['Face']['Confidence'],
                    'bounding_box': face['Face']['BoundingBox'],
                    'matched_face': search_response.get('FaceMatches', []),
                    'created_at': datetime.utcnow().isoformat()
                }
            )
            
            # Send alert if unknown face detected
            if not search_response.get('FaceMatches'):
                send_security_alert('Unknown face detected', face)

def send_security_alert(alert_type, detection_data):
    """Send security alert"""
    
    sns = boto3.client('sns')
    
    message = {
        'alert_type': alert_type,
        'timestamp': datetime.utcnow().isoformat(),
        'confidence': detection_data.get('Face', {}).get('Confidence', 0),
        'location': detection_data.get('Face', {}).get('BoundingBox', {}),
        'stream_name': 'security-camera-01'
    }
    
    sns.publish(
        TopicArn='arn:aws:sns:region:account:security-alerts',
        Message=json.dumps(message),
        Subject=f'Security Alert: {alert_type}'
    )
```

## Playback và Streaming

### 1. HLS Playback Implementation
```python
import boto3
from datetime import datetime, timedelta

class KinesisVideoPlayback:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.kvs = boto3.client('kinesisvideo')
        
    def get_hls_streaming_session(self, start_time=None, end_time=None):
        """Get HLS streaming session URL"""
        
        # Get HLS endpoint
        endpoint = self.kvs.get_data_endpoint(
            StreamName=self.stream_name,
            APIName='GET_HLS_STREAMING_SESSION_URL'
        )['DataEndpoint']
        
        # Create HLS client
        kvs_archived_media = boto3.client(
            'kinesis-video-archived-media',
            endpoint_url=endpoint
        )
        
        # Configure playback parameters
        playback_config = {
            'StreamName': self.stream_name,
            'PlaybackMode': 'LIVE'  # or 'ON_DEMAND'
        }
        
        if start_time and end_time:
            playback_config.update({
                'PlaybackMode': 'ON_DEMAND',
                'HLSFragmentSelector': {
                    'FragmentSelectorType': 'SERVER_TIMESTAMP',
                    'TimestampRange': {
                        'StartTimestamp': start_time,
                        'EndTimestamp': end_time
                    }
                }
            })
        
        # Get HLS streaming session URL
        response = kvs_archived_media.get_hls_streaming_session_url(**playback_config)
        
        return response['HLSStreamingSessionURL']
    
    def get_dash_streaming_session(self, start_time=None, end_time=None):
        """Get DASH streaming session URL"""
        
        # Get DASH endpoint
        endpoint = self.kvs.get_data_endpoint(
            StreamName=self.stream_name,
            APIName='GET_DASH_STREAMING_SESSION_URL'
        )['DataEndpoint']
        
        # Create DASH client
        kvs_archived_media = boto3.client(
            'kinesis-video-archived-media',
            endpoint_url=endpoint
        )
        
        # Configure DASH parameters
        dash_config = {
            'StreamName': self.stream_name,
            'PlaybackMode': 'LIVE'
        }
        
        if start_time and end_time:
            dash_config.update({
                'PlaybackMode': 'ON_DEMAND',
                'DASHFragmentSelector': {
                    'FragmentSelectorType': 'SERVER_TIMESTAMP',
                    'TimestampRange': {
                        'StartTimestamp': start_time,
                        'EndTimestamp': end_time
                    }
                }
            })
        
        response = kvs_archived_media.get_dash_streaming_session_url(**dash_config)
        
        return response['DASHStreamingSessionURL']
    
    def get_media_for_fragment_list(self, fragment_numbers):
        """Get media for specific fragments"""
        
        # Get media endpoint
        endpoint = self.kvs.get_data_endpoint(
            StreamName=self.stream_name,
            APIName='GET_MEDIA_FOR_FRAGMENT_LIST'
        )['DataEndpoint']
        
        # Create media client
        kvs_archived_media = boto3.client(
            'kinesis-video-archived-media',
            endpoint_url=endpoint
        )
        
        response = kvs_archived_media.get_media_for_fragment_list(
            StreamName=self.stream_name,
            Fragments=fragment_numbers
        )
        
        return response['Payload']
```

### 2. WebRTC Implementation
```javascript
// WebRTC viewer implementation
class KinesisVideoWebRTCViewer {
    constructor(streamName, region) {
        this.streamName = streamName;
        this.region = region;
        this.peerConnection = null;
        this.localVideo = null;
        this.remoteVideo = null;
    }
    
    async startViewer() {
        // Get signaling channel endpoint
        const kinesisVideo = new AWS.KinesisVideo({ region: this.region });
        
        const endpoint = await kinesisVideo.getDataEndpoint({
            StreamName: this.streamName,
            APIName: 'GET_SIGNALING_CHANNEL_ENDPOINT'
        }).promise();
        
        // Create WebRTC peer connection
        this.peerConnection = new RTCPeerConnection({
            iceServers: [
                { urls: 'stun:stun.kinesisvideo.us-west-2.amazonaws.com:443' }
            ]
        });
        
        // Handle remote stream
        this.peerConnection.ontrack = (event) => {
            if (this.remoteVideo) {
                this.remoteVideo.srcObject = event.streams[0];
            }
        };
        
        // Connect to signaling channel
        await this.connectToSignalingChannel(endpoint.DataEndpoint);
    }
    
    async connectToSignalingChannel(endpoint) {
        // WebSocket connection to signaling channel
        const ws = new WebSocket(endpoint);
        
        ws.onopen = () => {
            console.log('Connected to signaling channel');
            this.sendViewerMessage();
        };
        
        ws.onmessage = async (event) => {
            const message = JSON.parse(event.data);
            await this.handleSignalingMessage(message);
        };
    }
    
    async handleSignalingMessage(message) {
        switch (message.messageType) {
            case 'SDP_OFFER':
                await this.handleOffer(message.messagePayload);
                break;
            case 'ICE_CANDIDATE':
                await this.handleIceCandidate(message.messagePayload);
                break;
        }
    }
    
    async handleOffer(offer) {
        await this.peerConnection.setRemoteDescription(offer);
        
        const answer = await this.peerConnection.createAnswer();
        await this.peerConnection.setLocalDescription(answer);
        
        // Send answer back through signaling channel
        this.sendSignalingMessage('SDP_ANSWER', answer);
    }
}
```

## Best Practices

1. **Stream Configuration**: Configure appropriate retention và resolution
2. **Security**: Use IAM roles và encrypt streams
3. **Cost Optimization**: Monitor usage và optimize retention periods
4. **Performance**: Optimize encoding settings cho bandwidth
5. **Monitoring**: Set up comprehensive monitoring
6. **Error Handling**: Implement robust error handling
7. **Scalability**: Design cho multiple concurrent streams
8. **Integration**: Leverage AWS services cho processing

## Tích hợp với các dịch vụ AWS khác

- **Amazon Rekognition Video**: Video analysis và object detection
- **AWS Lambda**: Custom video processing
- **Amazon SageMaker**: Machine learning inference
- **Amazon S3**: Video archival và storage
- **Amazon DynamoDB**: Metadata và results storage
- **Amazon SNS**: Real-time notifications
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Security và access control
- **Amazon API Gateway**: REST APIs cho video access
- **AWS IoT Core**: IoT device integration
