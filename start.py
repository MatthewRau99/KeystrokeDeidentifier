import subprocess
import sys
import os
import argparse
from shutil import which
import time
import requests

def find_npm():
    """Find the npm executable"""
    npm_cmd = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    return which(npm_cmd)

def wait_for_backend():
    """Wait for backend server to be ready"""
    max_attempts = 10
    for _ in range(max_attempts):
        try:
            requests.get('http://localhost:8000')
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    return False

def start_servers(filename, output):
    # Find npm
    npm_path = find_npm()
    if not npm_path:
        print("Error: npm not found. Please ensure Node.js is installed and in your PATH")
        sys.exit(1)

    # Start the backend server
    backend = subprocess.Popen([sys.executable, "backend.py", filename, "--output", output])
    
    # Wait for backend to be ready
    if not wait_for_backend():
        print("Error: Backend server failed to start")
        backend.terminate()
        sys.exit(1)
    
    try:
        # Start the frontend server
        os.chdir("KeystrokeDeidentifier")
        frontend = subprocess.Popen([npm_path, "start"], 
                                  shell=True if sys.platform == 'win32' else False)
        
        # Wait for either process to finish
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
    except Exception as e:
        print(f"Error starting servers: {e}")
        backend.terminate()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Filepath to keystroke data CSV')
    parser.add_argument('-o', '--output', help='Project identifier', required=True)
    args = parser.parse_args()
    
    start_servers(args.filename, args.output)

