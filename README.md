# vim-axivion-bauhaus

[Axivion's Bauhaus suite](https://www.axivion.com/en/p/products-60.html#produkte_bauhaussuite) provides a static code analysis for your projects.
Found issues can be managed inside Axivion's dashboard and also exported to CSV files.
This plugin aims to provide functionality to read in these CSV files into VIM to more easily jump to the problematic locations inside your code.

To achieve this, the CVS content is parsed and afterwards written into VIM's quickfix list (see `:help quickfix`).
I'm in no way affiliated with Axivion.

## Requirements

This plugin uses Python3.
Your system needs to have Python3. Try running `python3 --version` to see, if you have Python3 installed.
If you don't have Python3 installed, you can install it from [here](https://www.python.org/downloads/).

Your VIM also needs to be compiled with Python3. Check the output of `vim --version` for `+python3`.

## Installation

To install, you can either use VIM's built-in package management (see `:help packages`).
Assuming your VIM directory is `~/.vim`, simply

```bash
mkdir -p ~/.vim/pack/bigpeet/start
cd ~/.vim/pack/bigpeet/start
git clone https://github.com/BigPeet/vim-axivion-bauhaus
vim -u NONE -c "helptags vim-axivion-bauhaus/doc" -c q # installs the helptags
```

Alternatively, use your preferred 3rd-party plugin manager, e.g. pathogen or Vundle.

## How to use

1. Export the CSV files you are interested in from Bauhaus. Currently only Style Violations are supported.
2. The paths inside the CSV should be relative to your project's top directory (referred to as `$PROJ_DIR` from now on).
3. Either open VIM inside `$PROJ_DIR` or set it inside VIM with `:cd $PROJ_DIR`.
4. Execute a convert command, e.g. `:ConvBh <PATH-TO-CSV>`
5. Depending on your configuration, your quickfix list should open and VIM should jump to the first issue.
    * To learn how to navigate the quickfix list, see `:help quickfix`.

## Commands and Options

Commands are executed with a leading `:` in the command line of VIM, e.g. `:COMMAND`.

The following commands are added by this plugin:

* `ConvBh <file>`

## Compatibility

Currently aims to work with Bauhaus version 6.9.15 and versions with a compatible CSV format.

## Next Development Steps

* ~Convert the Bauhaus CSV file into a suitable input for setqflist (see :help setqflist).~
    * ~First approach would be to provide the "list" parameter, e.g. every issue/error should result in a dictionary.~
    * ~If this should lead to complications, then provide the "what" parameter instead.~
* ~Add a command/function taking a path to the CSV file that does the following:~
    1. ~Pass the CSV path (and Bauhaus version) to the conversion function.~
    2. ~Take the formatted output and use it to populate the quickfix list (with setqflist()).~
    3. ~Open quickfix list and jump to first error (if the list it not empty).~
* Add conversions for the remaining CSV file types.
    * Metric Violations
    * Architecture Violations
    * Dead Code
    * Cyclic
    * Clones
* Add alternative command/function that does not take a file, but the "raw" csv content
    * call the *convert\_text* function directly
* Add a path filter to the conversion function that removes errors that do not match the given path.
* Add an additional command/function that uses the modified conversion function with the filename of the current window.
    * The result should be that only the errors for the currently viewed file are returned.
    * The converted output will be put into the location list (with setloclist()).
* Add a version of those commands without arguments that will look for the CSV file in a directory specified by variable.
* Add global variables that allow customization
    * bauhaus-version (if the CSV formats start to differ)
    * CSV directory
    * Default behaviour (e.g. opening the window)
* Add extensive filter options to the "general" commands:
    * *type:mode:pattern1;pattern2*
    * type: path, error, ...
    * mode: - (remove matches), ! (only matches)
    * pattern: pattern that should be matched, multiple patterns are concatenated with OR
* Add error handling for malformed input.
    * early abort
    * informative output
