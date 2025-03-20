HEAD
Slowloris DoS Attack Tool (Educational Purpose Only)

This is a Python implementation of a Slowloris DoS attack tool, created for educational and research purposes only. This tool demonstrates how Slowloris attacks work and can be used for learning about network security and DoS attack prevention.

 ⚠️ Legal Notice

This tool is for educational purposes only. Using this tool to attack systems without explicit permission is illegal and may result in criminal charges. The author is not responsible for any misuse of this tool.

Features

- Configurable number of connections
- Adjustable request intervals
- Customizable socket timeouts
- Graceful shutdown support
- Thread-safe connection tracking
- Support for both HTTP and HTTPS targets

Requirements

- Python 3.6 or higher
- Standard library modules (no external dependencies)

Installation

1. Clone this repository:
bash
git clone https://github.com/YOUR_USERNAME/slowloris-dos.git
cd slowloris-dos


2. Run the script:
bash
python dos.py [target] [options]


 Usage

Basic usage:
bash
python dos.py example.com


With options:
bash
python dos.py example.com -c 100 -i 2 -t 5


Options

target`: Target URL or IP address (required)
c, --connections`: Number of connections (default: 100)
i, --interval`: Interval between requests in seconds (default: 2)
t, --timeout`: Socket timeout in seconds (default: 5)
Example

bash
python dos.py example.com -c 200 -i 1.5 -t 10

How to Stop

Press `Ctrl+C` to gracefully stop the attack.

Security Considerations

This tool is designed for:
- Educational purposes
- Security research
- Testing your own systems
- Understanding DoS attack mechanisms

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details. 
slowloris-dos
>>>>>>> 3e85cd93eca1ce20793078eedd69fd555f86212b
