from pyngrok import ngrok
import time
import sys

def start():
    print("Starting ngrok tunnel on port 5000...")
    try:
        public_url = ngrok.connect(5000)
        print(f"\nSUCCESS! Your application is live at:\n{public_url}\n")
        print("Keep this terminal open to keep the tunnel alive. Press Ctrl+C to stop.")
        
        # Block until CTRL-C or some other terminating event
        ngrok_process = ngrok.get_ngrok_process()
        ngrok_process.proc.wait()
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start()
