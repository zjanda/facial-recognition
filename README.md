# Raspberry Pi Camera Server

This project demonstrates a real-time camera streaming system with facial recognition, facilitating Raspberry Pi to Windows communication over Ethernet or WiFi.

## Key Features

- Real-time video streaming and facial recognition
- Dual connection support (Ethernet/WiFi)
- Threaded architecture for concurrent operations
- Frame capture for updating the recognition database

## Technical Overview

The system consists of a Windows server for video reception and facial recognition, and a Raspberry Pi client for capturing and streaming video. It uses socket-based communication and MJPEG streaming for efficient data transmission.

## Scalability and Optimization

While the current setup isn't designed for large-scale deployment, future enhancements could include a hybrid edge/server architecture for distributed processing, optimized recognition pipelines, model quantization for performance gains, and improved multithreading to decouple video handling and facial detection from recognition tasks.

## Installation and Usage

- **Server (Windows):** Install Python dependencies, 
                        set up a virtual environment, 
                        run `install_requirements.py`, 
                        then `encode_known_faces.py`, 
                        and finally `server.py`.
- **Client (Raspberry Pi):** Install system and Python dependencies, and run `client.py`.

## Vision

This project was designed for rapid prototyping. For production, a scalable architecture with distributed processing and centralized intelligence would be essential.

## License

Open source under the MIT License.
