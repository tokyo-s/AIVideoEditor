# AIVideoEditor
heh, my Thesis

This is a project for my thesis about automating the process of video editing
The video editing app is a web application that will allow users to select with checkboxes any preprocessing steps the user wants, examples of options are:

* Auto subtitles
* Text translation
* Newsletter creation from video content
* Topics division 
* Audio cleaning
* Video trimming
* Logo blurring 
* Faces blurring
* Licence plates blurring, 
* Quality enhancement, 
* Auto AI Thumbnail creation

# Installation Steps:

## Install ImageMagick 

1. Download and install ImageMagick for Windows from the official website: https://imagemagick.org/script/download.php. Make sure to check the "Install legacy utilities (e.g. convert)" option during the installation process.

2. After installing ImageMagick, you need to find the path to the `magick` binary. It is usually located in the installation folder, for example: `C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe` (the version number may be different).

3. Replace the path with the correct path to your `magick.exe` file inside the `config.py`.

## Change config.py file

### 1. Create a OpenAI Account on https://platform.openai.com and create a new API key
### 2. add your API key to the Worker/config.py file
```python
OPEN_API_KEY = 'YOUR_API_KEY'
```
