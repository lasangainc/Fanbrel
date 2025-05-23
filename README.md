# Fanbrel Community App Store

This is a community app store for Umbrel OS containing the Fanbrel app - a smart fan controller for your Raspberry Pi.

## Installation

1. In your Umbrel OS dashboard, go to "App Store"
2. Click on "..." and select "Add Community App Store"
3. Enter the following URL: `https://github.com/yourusername/fanbrel`
4. Click "Add" to add the community app store
5. Find "Fanbrel" in the app list and click "Install"

## Local Development

To develop and test the Fanbrel app locally:

1. Clone this repository:
```bash
git clone https://github.com/yourusername/fanbrel
cd fanbrel
```

2. Connect your fan to GPIO14 (Pin 8) and GND on your Raspberry Pi.

3. Build and run the app:
```bash
cd fanbrel-fanbrel
docker-compose up --build
```

4. Access the web UI at `http://localhost:3500`

## Hardware Setup

The app expects a 2-pin fan connected to:
- GPIO14 (Pin 8) for PWM control
- Any GND pin for ground

## Configuration

Temperature thresholds can be modified in `fanbrel-fanbrel/app/fan_control.py`:
- `TEMP_HIGH`: Temperature at which the fan turns on (default: 60°C)
- `TEMP_LOW`: Temperature at which the fan turns off (default: 50°C)

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

MIT 