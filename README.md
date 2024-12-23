# The Blender AI Plugin 🚀

Use AI to make changes to your blender scene in seconds! Completely free of charge.

![Demo Gif](https://github.com/user-attachments/assets/28312688-ccb9-4089-a9b0-58d9d2786e6d)

# Installation

1) Click on the green code button for this repository near the upper right hand corner and download the code as a ZIP file.
2) Open the download and extract it using the file explorer to wherever you want to put it (just remember the location for later)
3) Open blender
4) Edit > Preferences > Add-ons
5) Click the Install button in the upper right hand corner
6) Navigate to the folder you extracted in step 2
7) Open the folder and double click to open ```ai_plugin.py```
8) Search for ```Google AI Studio Script Executor``` in your addons list and make sure it is enabled.

API Key Setup (Necessary):
1) Visit https://aistudio.google.com/apikey and generate an api key. You might have to make a Google Cloud project first, but this is free (if you need help, ask an AI)

Option 1 (Set as environment variable, recommended):
Windows:
1) Search for "environment variables" using the windows search on your computer
2) Click on ```Edit the system enviroment variables``` or ```Edit user enviroment variables```
3) A "system properties" window should appear, click on the ```Environment Variables``` button near the bottom
4) Two boxes will appear for user and environment variables, click on the ```New...``` button in the upper box
5) Enter ```GOOGLE_AI_STUDIO_API_KEY``` as the name and paste your api key in the value box.
6) Close out and restart blender for changes to take effect
Linux:
1) Append ```export GOOGLE_AI_STUDIO_API_KEY="<your_api_key_here>"``` to your bashrc
2) Restart blender and enjoy

Option 2 (Paste API key into box, not recommended):
1) Paste your API key into the ```API KEY``` box in the plugin menu and use as normal

# Usage

1) When in the 3d viewport, press ```n``` to toggle the side menu on. In the menu that pops up, you should see ```AI Studio``` as one of the tabs.
2) Click on ```AI Studio``` to open the plugin menu. Sometimes it shows up compacted so make sure you click on the carrot if you need to expand it.
3) Make sure you have your API key configured then select a model from the dropdown
4) Enter a prompt and then click ```Generate and Execute Script```
5) Sometimes this will give errors, just try to adjusts your prompts as needed
6) If something breaks or the AI starts getting confused, you can always click the ```Clear Context``` button. The AI will forget what it has done and won't know anything about what objects are in the scene, but can still make new objects (and change existing ones if you tell it the exact name of the object)
7) Remember that this is not a production-grade product and there will likely be many bugs. I made this almost entirely using ChatGPT, so it can't be perfect. If you find any issues, you can edit the code yourself (it's only one python file, you got this!), ask an AI for assistance, or submit an issue on GitHub (although I might not be able to fix it)
8) Enjoy 🗿

# Contribution

Any contributions are welcome! Just open a PR with your changes and as long as they seem beneficial and work well, I will probably merge them. If you have some spare time and want to contribute, it might be cool to have integrations for other model providers or the ability to send the model a screenshot of the current scene :)

# Credits

This was heavily inspired by Polyfjord's youtube video on controlling blender using AI, go check it out!
[![Watch the video](https://img.youtube.com/vi/ytomieYqUCQ/0.jpg)](https://www.youtube.com/watch?v=ytomieYqUCQ)
