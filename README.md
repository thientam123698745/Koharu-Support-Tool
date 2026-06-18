🌸 Koharu-Support-Tool
A lightweight tool designed to help users with low-spec PCs quickly perform:

📝 Translation (via Google Translate)

🎨 Inpainting (image correction)

🔧 Transformations (resize text blocks)

📤 Exporting (translated images)

📦 System Information

Koharu Support version: 0.61.2

Koharu Official Website: https://koharu.rs/

Python version: 6.13

Download Python: https://www.python.org/downloads/

✅ Tested on Windows 11


🚀 Quick Start
1. Install dependencies (first run only)

py InstallLybrary.py


2. Run translation
Find the port and run:
python KST_QuickStart.py translate --port 4000


👉 This will:
Detect all OCR text blocks
Translate them via Google Translate
Post results to the Kohaku server

🎨 Features & Commands
Feature	Command	Description
| Feature | Command | Description |
| --- | --- | --- |
| **Translate** | ``python ``KST_QuickStart.py ``translate ``--port ``4000`` | Google Translate + Kohaku server sync |
| **Inpaint** | ``python ``KST_QuickStart.py ``inpaint ``--port ``4000`` | Quickly inpaint all images in the project |
| **Transform** | ``python ``KST_QuickStart.py ``transform ``--port ``4000`` | Increase size of all text blocks |
| **Export** | ``python ``KST_QuickStart.py ``export ``--port ``4000`` | Export only fully translated images to ``Export/`` folder |
| **Run All** | ``python ``KST_QuickStart.py ``all ``--port ``4000`` | Translate + Inpaint + Transform in one go |


📂 Output
Translated images are saved in the Export folder.

Original filenames are preserved for easy tracking.

💡 Notes
Designed for low-spec PCs to ensure smooth performance.

All-in-one workflow: Translate → Inpaint → Transform → Export.
