# Pitchfork
 [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
 
A Python bot that webscrapes the Dickinson College Caf Menus and utilizes SMTP to email daily menus to a select list of people. The deployment of Pitchfork is done by setting a cronjob on Github Actions to run every morning at 8:00 AM (Send time may vary considering Github Actions add a cronjob to a queue). 

# Installing Pitchfork 
Both the script version and the binary version follow the same install process. Assuming you have Python 3, you can do this to install the dependencies:
```py
pip install -r requirements.txt
```
You can then execute the script (found in src/) like this:
```py
python3 pitchfork.py
```
or if you want to use the cli binary (found in bin/) you can set permissions (using chmod or equivalent) and put it in a directory in your path (or alias into your shellrc):
```py
chmod +x cafmenu
./cafmenu
```

# Improvements
Please feel free to submit a pull request or discuss any recommended improvements with me on GitHub Issues!


# Contributors
[Ty Chermsirivatana '27](https://github.com/WarpWing) - Initial Work

<sup><sub><sub>[Evan Wong '24](https://github.com/evanwong1020) - Added Song Lyrics</sub></sub></sub></sup>

# Acknowledgements 
[Boosung Kim '25](https://github.com/boosungkim) - For his work on his own Dickinson Menu Bot which inspired this project.


