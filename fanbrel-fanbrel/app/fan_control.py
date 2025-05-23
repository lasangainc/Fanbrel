#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os
import json
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# GPIO setup
FAN_PIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Temperature thresholds
TEMP_HIGH = 60.0  # Turn on above this temperature
TEMP_LOW = 50.0   # Turn off below this temperature

# Global state
fan_state = False
current_temp = 0.0

def get_cpu_temp():
    """Get CPU temperature from system"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0
        return temp
    except:
        return 0.0

def control_fan():
    """Control fan based on temperature"""
    global fan_state, current_temp
    
    while True:
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
        with open('/data/state.json', 'w') as f:
            json.dump(state, f)
            
        time.sleep(5)

@app.route('/api/status')
def get_status():
    """API endpoint to get current status"""
    return jsonify({
        'temperature': current_temp,
        'fan_state': fan_state,
        'thresholds': {
            'high': TEMP_HIGH,
            'low': TEMP_LOW
        }
    })

if __name__ == '__main__':
    # Start fan control in a separate thread
    from threading import Thread
    fan_thread = Thread(target=control_fan, daemon=True)
    fan_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=3500)

# Cleanup GPIO on exit
def cleanup():
    GPIO.cleanup()

import atexit
atexit.register(cleanup) 