DirtLENS was created to enhance data collection in soil science and field-based research. Early on, I developed a light-chambered borescope to improve accuracy in analyzing soil and geological materials. That foundation evolved into a compact utility that identifies surface colors in real time and overlays them with GPS-based cardinal direction data—optimized for use in remote, outdoor environments.

The system runs on a compact single-board computer housed in a cylindrical, flashlight-like chamber. A ribbon-connected camera sits at the top, with internal LED lighting for consistent illumination and a round display mounted on the back for real-time feedback.

Key Features
- Detects and displays surface color in real time using OpenCV.
- Overlays GPS-based cardinal direction (e.g., “NW Wall”) with a custom `gps_helper`.
- 3-click top-corner shutdown mechanism for quick field control.
- Modular architecture for easy expansion (`circle_color_detector`).
- Designed for embedded setups with a compact camera chamber and onboard display.

Hardware Highlights
- Lightweight single-board computer runs the Python utility.
- Ribbon camera module installed inside a sealed chamber.
- LED lighting integrated to maintain consistent conditions.
- Round display provides immediate visual output from the utility.



Field Use:
Ideal for archaeology, soil science, and other environmental research, DirtLENS helps document surface pigments and environmental data accurately in off-grid or low-connectivity
