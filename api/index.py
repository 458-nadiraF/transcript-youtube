from http.server import BaseHTTPRequestHandler
from youtube_transcript_api import YouTubeTranscriptApi
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)
        
        # Get video_id from query parameter
        video_id = params.get('video_id', [None])[0]
        
        if not video_id:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Missing video_id parameter',
                'usage': '/api?video_id=YOUR_VIDEO_ID'
            }).encode())
            return
        
        try:
            # Fetch transcript
            ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id)
            
            # Format the response
            full_text = ' '.join([entry['text'] for entry in transcript])
            
            response = {
                'success': True,
                'video_id': video_id,
                'transcript': transcript,
                'full_text': full_text
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
    
    def do_POST(self):
        # Get the content length
        content_length = int(self.headers.get('Content-Length', 0))
        
        # Read the POST data
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON body
            data = json.loads(post_data.decode())
            video_id = data.get('video_id')
            
            if not video_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Missing video_id in request body'
                }).encode())
                return
            
            # Fetch transcript
            ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id)
            
            # Format the response
            full_text = ' '.join([entry['text'] for entry in transcript])
            
            response = {
                'success': True,
                'video_id': video_id,
                'transcript': transcript,
                'full_text': full_text
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Invalid JSON in request body'
            }).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
