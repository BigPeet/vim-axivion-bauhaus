# vim-axivion-bauhaus

TODO: General introduction

## What does it do?

TODO

## Installation

TODO

### Requirements

TODO

## Commands and Options

TODO

## Compatibility

TODO

## Development Steps

* Convert the Bauhaus CSV file into a suitable input for setqflist (see :help setqflist).
    * First approach would be to provide the "list" parameter, e.g. every issue/error should result in a dictionary.
    * If this should lead to complications, then provide the "what" parameter instead.
* Add a command/function taking a path to the CSV file that does the following:
    1. Pass the CSV path (and Bauhaus version) to the conversion function.
    2. Take the formatted output and use it to populate the quickfix list (with setqflist()).
    3. Open quickfix list and jump to first error (if the list it not empty).
* Add a path filter to the conversion function that removes errors that do not match the given path.
* Add a second command/function that uses the modified conversion function with the filename of the current window.
    * The result should be that only the errors for the currently viewed file are returned.
    * The converted output will be put into the location list (with setloclist()).
* Add a version of those commands without arguments that will look for the CSV file in a directory specifief by variable.
* Add global variables that allow customization
    * bauhaus-version (if the CSV formats start to differ)
    * CSV directory
