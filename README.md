# SRT Caption Distiller

## Description
SRT Caption Distiller is a Python-based script that will quickly and effortlessly correct subtitle/caption formatting issues commonly found in auto-generated .srt (SubRip Subtitle) files.

In short, SRT Caption Distiller helps your subtitles/captions go from sometimes looking like this:
![Before SRT Caption Distiller](https://github.com/tmaaz/srt-caption-distiller/imgs/before_srtcd.png?raw=true)

to consistently looking like this:
![After SRT Caption Distiller](https://github.com/tmaaz/srt-caption-distiller/imgs/after_srtcd.png?raw=true)

## What It Does Do
SRT Caption Distiller adjusts the formatting (line and character count) of your subtitles/captions, to align with the official FCC Caption Quality Standards, while keeping the timing as close as possible to the original timing of the commentary in the video. SRT Caption Distiller does this incredibly fast, as well -- I have processed several 6-hour long recordings of Twitch streaming video (lots of speaking), and it takes only a fraction of a second to process the entire file.

## What It Doesn't Do
SRT Caption Distiller can not make your subtitles/captions ADA compliant. It is impossible to automate the proccess of adding and/or correcting precise spelling, punctuation, grammar, annotated background noises, etc. SRT Caption Distiller can save you literal hours worth of work per hour of recorded video, but it can't do everything -- a human being is still required to do the fine detail work, to potentially meet ADA compliance.

## Tech Used
SRT Caption Distiller was created using the latest version of Python (3.10.0), and it requires no additional/external tools or libraries to work, only built-in modules. (It may very well be backward compatible to earlier version of Python, I just haven't had the opportunity to check as of yet.)

## Future Features
- a simple drag-and-drop widget-like interface would be nice
- expanding the code to distill additional file formats
  - .sbv (YouTube Captions) files, if there is a call for it
  - .sub (MicroDVD subtitle) files, if there is a call for it

## How To Install
As a simple Python script file, there is no real "installation" necessary -- you just copy the file onto your computer. However, running the script ***does*** require that you have Python installed on your computer.

To see if you have it:
1. Open a terminal window
  - On Windows, click Search in the taskbar, and type "Command Prompt" and open the app.
  - On a Mac, go to Applications > Utilities > Terminal, and open the app.
2. At the prompt, simply type the word "python", and Enter.

If Python is already installed, you will see some text appear, followed by a ">>>" prompt. This means that Python is installed and now running. (If you do not have Python installed: [Download Python for Windows](https://www.python.org/downloads/windows/) | [Download Python for Mac](https://www.python.org/downloads/macos/) | [How to Install Python](https://wiki.python.org/moin/BeginnersGuide/Download) )

## How To Use
With python running in the terminal, simply click and drag the "srt-caption-distiller.py" file into the terminal window, and Enter. SRT Caption Distiller will open, and ask you for the .srt file. Again, a simple click and drag of your .srt file into the terminal window, and then Enter.

If you have provided a proper .srt file, SRT Cpation Distiller will instantly create a temporary copy (your original file is never altered), the working file is modified as necessary, and then it is saved as a separate final .srt file, with "_distilled" added to the name. (e.g., if your original file is on the Desktop and is named "transcript_22-01-26.srt", your new distilled file will be saved on the Desktop, named "transcript_22-01-26_distilled.srt")

## To Contribute
Please see the ![Contributing](/CONTRIBUTING.md) and ![Code of Conduct](/COODE_OF_CONDUCT.md) documents included in this project. The code is currently almost line-by-line commented, for those learning Python or just wanting to understand how this works.

## Credits
Created by Trevor Masinelli (aka tmaaz)

## License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Badges
![GitHub](https://img.shields.io/github/license/tmaaz/srt-caption-distiller) | [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md) | ![GitHub all releases](https://img.shields.io/github/downloads/tmaaz/srt-caption-distiller/total) | ![GitHub release (latest by date)](https://img.shields.io/github/v/release/tmaaz/srt-caption-distiller)