<p align="center">
    <img src="https://raw.githubusercontent.com/ndrscalia/pandasnoir/demo.gif" alt="Cover photo" />
    <br/>
    <img src="https://img.shields.io/github/stars/ndrscalia/pandasnoir?style=social" />
  </p>

`pandasnoir` is a TUI based game built with [Textual](https://github.com/textualize/textual) and inspired by [sqlnoir](sqlnoir.com). The cases and the data are the same, but you can now test your pandas' skills on them.<br/>
The pixel "art" (I'm no professional, I know) was drawn by me with [Aseprite](https://www.aseprite.org). For it to render, your monitor should be bigger than a laptop's one.

If you find any value in this project please leave a star and consider buying me a coffee.

> [!IMPORTANT]
> For the Textual experience to fully express itself you should run the program on a modern terminal emulator (tested on Kitty only, but any other popular option should work fine).

> [!IMPORTANT]
> Assets and output enrichment are mainly suited to Textual's default dark theme. Other themes – especially light ones – may not allow a good UI experience.

Once you launch the game the directory `~/.pandasnoir/` is created to store progress and make your work persistent. If you want to reset everything, just delete the directory.

# Installation
The software can be installed through PyPi:<br/>
```bash
# using pip/pipx
pip install pandasnoir
pipx install pandasnoir # pipx upgrade to update it

# or using uv
uv tool install pandasnoir
```

You can also install the software from source:<br/>
```bash
git clone https://github.com/ndrscalia/pandasnoir
cd pandasnoir
pip install -e .
```
Then you can simply run `pandasnoir`.

The software can also be used without installing it through uv:
```bash
uvx --from pandasnoir pandasnoir
```

# Contributing
Any contribution is welcome. Open an issue for bugs / qol proposals or use pull requests if you wrote a new case that you would like to be added.

# Testing
To test the repo install the test dependencies

```bash
cd pandasnoir
pip install -e ".[test]" # or pip install -e ".[dev]"
pytest -v
```

The test suite was built with claude-code and then reviewed by me.
