# vim-axivion-bauhaus

![bh2err module](https://github.com/BigPeet/vim-axivion-bauhaus/workflows/bh2err%20module/badge.svg)

[Axivion's Bauhaus suite](https://www.axivion.com/en/p/products-60.html#produkte_bauhaussuite) provides a static code analysis for your projects.
Found issues can be managed inside Axivion's dashboard and also exported to CSV files.
This plugin aims to provide functionality to read in these CSV files into VIM to more easily jump to the problematic locations inside your code.

To achieve this, the CVS content is parsed and afterwards written into VIM's quickfix list (see `:help quickfix`).

**This plugin is in early stages of development and therefore bugs are expected.**
(Feel free to report issues.)

This plugin and I are not affiliated with Axivion.

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

1. Export the CSV files you are interested in from Bauhaus. Main focus is on Style Violations. Other kind of violations might not work properly.
2. The paths inside the CSV should be relative to your project's top directory (referred to as `$PROJ_DIR` from now on).
3. Either open VIM inside `$PROJ_DIR` or set it inside VIM with `:cd $PROJ_DIR`.
4. Execute a convert command, e.g. `:ConvBh <PATH-TO-CSV>`
5. Depending on your configuration, your quickfix list should open and VIM should jump to the first issue.
    * To learn how to navigate the quickfix list, see `:help quickfix`.

## Commands and Options

Commands are executed with a leading `:` in the command line of VIM, e.g. `:COMMAND`.

The following commands are added by this plugin:

* `ConvBh <file> [<filter-options>]`
* `ConvBhRaw <raw-csv-content>`
* `ConvBhCmd <shell-cmd to provide csv-content>`, e.g. `:ConvBhCmd cat file.csv`

### Filter Options

Some of the commands can take `<filter-options>` to filter the violations, e.g. by error number, file path or severity.
Using filter-options is optional.
(Note: Currently suppressed violations are always filtered.)
Multiple filter-options can be used in the same call.
They will be concatenated with AND, i.e. each violation must pass all filters.
Each filter-option must have the following form:

`type:mode:pattern[;pattern]*`

* type: The column to be filtered (e.g. error, path, severity)
    * Some columns are key-worded for ease-of-use (e.g. the "Error Number" column is keyworded as "error").
    * If a column has no keyword, then its full name can be used.
* mode:
    * default (leave empty): Check if the pattern is contained in the field.
    * exact (!): Check if the pattern is equal to the field.
    * negate (-): Will negate the result
* pattern:
    * The pattern to be searched for.
    * Multiple patterns can be specified (separated by ;) and are concatenated with OR, i.e. each violation must only pass at least one of the patterns.

Examples:

* `error::M6` will only show violations which contain M6 in their error number.
* `path::%` will only show violations which contain the current file in their path.
* `severity:!:required;advisory` will only show violations whose severity field is exactly required or advisory.
* `path:-:/usr` will remove all findings whose path includes "/usr"
* `Id:!-:SV01` will show all findings whose Id column is not exactly "SV01".

## Compatibility

Currently aims to work with Bauhaus version 6.9.15 and versions with a compatible CSV format.
