# COVAS:NEXT Sticky Notes

A notes & lists plugin for COVAS:NEXT.  
This is mostly a proof of concept at this point, and performance could probably be better, but it does work.


## Features

- Allows Commanders to add, update, delete and retrieve various notes and lists.
- All notes are kept fresh in the assistant's context.
- Notes are stored in a dedicated SQLite database, located in the plugin's data folder, allowing for persistance between characters, sessions and software updates.


## Installation

Download the latest release under the *Releases* section on the right.  
Unpack the plugin into the `plugins` folder in COVAS:NEXT, leading to the following folder structure:
* `plugins`
    * `StickyNotes`
        * `StickyNotes.py`
        * `requirements.txt`
        * `deps`
        * `__init__.py`
        * etc.
    * `OtherPlugin`

# Development
During development, clone the COVAS:NEXT repository and place your plugin-project in the plugins folder.  
Install the dependencies to your local .venv virtual environment using `pip`, by running this command in the `StickyNotes` folder:
```bash
  pip install -r requirements.txt
```

# Packaging
Use the `./pack.ps1` or `./pack.sh` scripts to package the plugin and any Python dependencies in the `deps` folder.
    
## Acknowledgements

 - [COVAS:NEXT](https://github.com/RatherRude/Elite-Dangerous-AI-Integration)
 - [My other projects](https://github.com/MaverickMartyn)
