# AutoClicker Kivy v4.0

## Description

A graphical autoclicker built with Kivy. Select a target window to filter clicks, choose between a fixed point or a random area, set the click delay, and monitor the click count and logs in real time.

## Table of Contents

* [Features](#features)
* [Installation](#installation)
* [Requirements File](#requirements-file)
* [Prerequisites](#prerequisites)
* [Launching the App](#launching-the-app)
* [GUI Overview](#gui-overview)
* [Controls & Hotkeys](#controls--hotkeys)
* [Logs](#logs)
* [Contributing](#contributing)
* [License](#license)

## Features

* **Fixed mode**: click repeatedly at a single point you set
* **Free mode**: click at random positions within a rectangle you define
* **Target window filter**: restrict clicks to a specific window and bring it to front
* Adjustable **delay** between clicks (in milliseconds)
* **Click counter** and **reset** options
* **Real-time logs** in the interface
* **Hotkey (Esc)** to stop clicking immediately

## Installation

1. Clone the repository:

   ```powershell
   git clone https://github.com/YourUsername/AutoClicker.git
   cd AutoClicker
   ```
2. (Optional) Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies from `requirements.txt`:

   ```powershell
   pip install -r requirements.txt
   ```

## Requirements File

A `requirements.txt` file is included at the root of the project. It lists all necessary packages:

```
pyautogui
keyboard
pynput
kivy
pywin32
```

## Prerequisites

* **Python** 3.7 or higher
* **Windows** (for `pywin32` and window filtering)
* The packages specified in `requirements.txt` (installs via `pip install -r requirements.txt`)

## Launching the App

Run the main script:

```powershell
python autoclicker.py
```

The Kivy window will open, displaying all controls and settings.

## GUI Overview

1. **Mode**

   * **Fixed**: click at one fixed point
   * **Free**: click at random points within a box
2. **Target Window**

   * Toggle to use a target window filter
   * **Set window**: click anywhere on screen to select the window title
3. **Fixed Click Settings** (when Fixed mode active)

   * **Set point**: click to record the exact coordinates
   * **Width/Height**: optional area dimensions (not used in Fixed)
4. **Free Click Settings** (when Free mode active)

   * **Top-left corner** and **Bottom-right corner**: click to define the rectangle
5. **Delay & Counter**

   * **Delay (ms)**: increase or decrease delay in 1000 ms steps, or type directly
   * **Counter**: show or hide total clicks; **Reset** to zero
6. **Control Buttons**

   * **Start**: begin clicking
   * **Stop**: halt immediately
   * **Reset All**: stop clicking and clear all settings

## Controls & Hotkeys

* **Esc key**: stops clicking immediately (when running)
* **Start/Stop buttons**: control the clicker manually
* **Reset All**: restores default values and stops any running clicker

## Logs

All actions (mode changes, delay updates, clicks, errors) appear in the log area at the bottom. It auto-truncates when too long.

## Contributing

Contributions are welcome! Steps:

1. Fork the project
2. Create a branch:

   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes:

   ```bash
   git commit -m "feat: add new feature"
   ```
4. Push to your branch:

   ```bash
   git push origin feature/my-feature
   ```
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
