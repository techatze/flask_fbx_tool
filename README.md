# FBX Processing Pipeline Tool

A lightweight pipeline tool that demonstrates an end-to-end workflow for processing FBX files using a client-server architecture.

This project was built to simulate real-world pipeline tools used in game development and VFX environments.



## Overview

This tool allows users to:

- Browse and select .fbx files
- Submit processing jobs through a UI
- Execute tasks asynchronously on a backend
- Track job status in real time
- Visualize FBX scene hierarchy in a structured tree view



## Key Concepts Demonstrated

- Asynchronous job processing
- REST API communication
- Separation of concerns (UI / API / logic)
- State-driven UI updates
- Basic pipeline architecture

## Architecture

PySide UI (Client)

Flask API (Server)

Job Manager (State)

Worker (Execution)

FBX Processing (Core Logic)




## Project Structure

-- app.py # Flask API

-- job_manager.py # Job creation & state management

-- worker.py # Job execution logic

-- validator.py # FBX processing logic

-- frontend_ui.py # PySide6 UI client




## Features

### Job System
Unique job IDs (UUID)

Job states: queued → processing → done / failed

Persistent storage using JSON

### Backend (Flask)
- POST /submit → submit job
- GET /status/<job_id> → check status
- Asynchronous execution using threads

### UI (PySide6)
- File browser for FBX files
- Job table with:
  - File name
  - Status
  - Result summary
- Real-time polling of job status
- Double-click result to inspect details

### FBX Processing
- Scene hierarchy traversal
- Mesh detection
- Structured output for visualization

### Visualization
- Tree view (QTreeWidget) for scene hierarchy
- Indentation-based parsing into hierarchy



## Example Workflow

1. Select a folder containing .fbx files
2. Choose a process (Analyze / Find Meshes)
3. Submit jobs
4. Monitor job status in the table
5. Double-click a result to inspect scene structure



## Technologies Used

- Python
- PySide6 (UI)
- Flask (API)
- FBX SDK (Python bindings)
- Requests (HTTP client)




## Purpose

This project was created as a learning exercise to:

- Understand pipeline architecture
- Build tools with UI + backend communication
- Simulate real production workflows in a simplified environment




