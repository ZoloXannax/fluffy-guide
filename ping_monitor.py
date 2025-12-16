import subprocess
import time
import os
from datetime import datetime
import statistics

def get_ping(host="8.8.8.8"):
    """
    Measure ping to a given host. 
    Returns ping time in milliseconds, or None if ping fails.
    """
    try:
        # Determine the correct ping command based on OS
        param = "-n" if os.name == "nt" else "-c"
        
        # Execute ping command (1 packet)
        result = subprocess.run(
            ["ping", param, "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        
        # Parse the output
        output = result.stdout.decode('utf-8', errors='ignore')
        
        # Extract ping time
        if "time=" in output:
            ping_time = float(output.split("time=")[1].split("ms")[0].strip())
            return ping_time
        elif "time " in output:  # Windows format
            ping_time = float(output.split("time ")[1].split("ms")[0].strip())
            return ping_time
    except Exception as e:
        print(f"Error pinging {host}: {e}")
    
    return None

def monitor_ping(host="8.8.8.8", interval=5, duration=None):
    """
    Monitor ping to a host at regular intervals.
    
    Args:
        host: Target host to ping (default: 8.8.8.8 - Google DNS)
        interval: Time between pings in seconds (default: 5)
        duration: Total monitoring duration in seconds (None = infinite)
    """
    ping_times = []
    start_time = time.time()
    
    print(f"Starting ping monitor for {host}...")
    print(f"Interval: {interval}s | Duration: {duration if duration else 'Infinite'}")
    print("-" * 60)
    
    try:
        while True:
            # Check if duration limit reached
            if duration and (time.time() - start_time) > duration:
                break
            
            ping_time = get_ping(host)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if ping_time is not None:
                ping_times.append(ping_time)
                status = "✓ OK"
                print(f"{timestamp} | {status} | Ping: {ping_time:.2f}ms")
            else:
                status = "✗ FAILED"
                print(f"{timestamp} | {status} | Connection lost!")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n" + "-" * 60)
        print("Monitor stopped by user.")
    
    # Print statistics
    if ping_times:
        print("\nPing Statistics:")
        print(f"  Packets sent: {len(ping_times)}")
        print(f"  Min ping: {min(ping_times):.2f}ms")
        print(f"  Max ping: {max(ping_times):.2f}ms")
        print(f"  Avg ping: {statistics.mean(ping_times):.2f}ms")
        if len(ping_times) > 1:
            print(f"  Std Dev: {statistics.stdev(ping_times):.2f}ms")
    else:
        print("No successful pings recorded.")

if __name__ == "__main__":
    # Example usage
    # monitor_ping(host="8.8.8.8", interval=5, duration=None)
    
    # Or customize: 
    monitor_ping(
        host="8.8.8.8",      # Change to your target host
        interval=2,          # Ping every 2 seconds
        duration=60          # Monitor for 60 seconds (None = infinite)
    )
