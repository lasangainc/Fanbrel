#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os
import json
import sys
from flask import Flask, jsonify, send_from_directory

# Initialize Flask app
app = Flask(__name__)

# GPIO setup
FAN_PIN = 14

def setup_gpio():
    """Setup GPIO with error handling"""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FAN_PIN, GPIO.OUT)
        return True
    except Exception as e:
        print(f"Error setting up GPIO: {e}", file=sys.stderr)
        return False

# Temperature thresholds
TEMP_HIGH = 60.0  # Turn on above this temperature
TEMP_LOW = 50.0   # Turn off below this temperature

# Global state
fan_state = False
current_temp = 0.0
gpio_available = False

def get_cpu_temp():
    """Get CPU temperature from system"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
        return temp
    except Exception as e:
        print(f"Error reading temperature: {e}", file=sys.stderr)
        return 0.0

def control_fan():
    """Control fan based on temperature"""
    global fan_state, current_temp, gpio_available
    
    if not gpio_available:
        gpio_available = setup_gpio()
        if not gpio_available:
            print("Failed to setup GPIO, retrying in 30 seconds...", file=sys.stderr)
            time.sleep(30)
            return
    
    while True:
        try:
            current_temp = get_cpu_temp()
            
            if current_temp >= TEMP_HIGH and not fan_state:
                GPIO.output(FAN_PIN, GPIO.HIGH)
                fan_state = True
            elif current_temp <= TEMP_LOW and fan_state:
                GPIO.output(FAN_PIN, GPIO.LOW)
                fan_state = False
                
            # Save state to file for web UI
            state = {
                'temperature': current_temp,
                'fan_state': fan_state,
                'timestamp': time.time()
            }
            
            os.makedirs('/data', exist_ok=True)
            with open('/data/state.json', 'w') as f:
                json.dump(state, f)
                
        except Exception as e:
            print(f"Error in control loop: {e}", file=sys.stderr)
            
        time.sleep(5)

@app.route('/')
def root():
    return send_from_directory('ui', 'index.html')

@app.route('/api/status')
def get_status():
    """API endpoint to get current status"""
    return jsonify({
        'temperature': current_temp,
        'fan_state': fan_state,
        'gpio_available': gpio_available,
        'thresholds': {
            'high': TEMP_HIGH,
            'low': TEMP_LOW
        }
    })

if __name__ == '__main__':
    # Create data directory
    os.makedirs('/data', exist_ok=True)
    
    # Start fan control in a separate thread
    from threading import Thread
    fan_thread = Thread(target=control_fan, daemon=True)
    fan_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=3500)

# Cleanup GPIO on exit
def cleanup():
    if gpio_available:
        GPIO.cleanup()

import atexit
atexit.register(cleanup) 