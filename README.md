# Email Generator

## Installation (PyPI)
```sh
pip3 install email-draft-generator
```

## Building from source
Install the `build` tool with pip and run `python3 -m build` to build the package.

## Usage (command line)
The utility provides two command-line binaries: `email-generator` and `email-list-parser`.

### email-generator
`email-generator` takes a JSON-formatted list of E-mail addresses and recipient names, formats them according to the template JSON, and uploads them to Gmail. To set up the Google API, run it once (you will need to provide a valid list of E-mail addresses for it to run), and it will guide you through setting this up. Most of the usage specifics are described in the usage help, which you can show by running `email-generator -h`.

### email-list-parser
`email-list-parser` takes a CSV formatted list or a newline-seperated list of values and turn it into a JSON file which can be piped into `email-generator`.

#### Text file format
The values should be formatted as follows
```
Company Name 1
e-mail@company1.com
Company Name 2
e-mail@company2.com
Company Name 3
e-mail@company3.com
...
```

#### CSV format
The CSV file should have the keys in the order `name,email`

### Template Format
The E-mail template is a JSON file with the following keys
| Key                      | Value                                            |
|--------------------------|--------------------------------------------------|
| `subject` (formatted)    | E-mail subject                                   |
| `body` (formatted)       | E-mail body                                      |
| `attachments` (optional) | Paths to any attachments that should be included |

Formatted fields can include the following variables
| Variable  | Data           |
|-----------|----------------|
| `{name}`  | Company name   |
| `{email}` | Company E-mail |

## Installation (scripts)
Download the latest release as a `tar.gz` file.

### Setup
#### Build program
Run `setup.sh` (can be run by simply double-clicking on the file).

#### Set up the template
Update the email template in `data/template.json` according to the [template format](#template-format).

#### Google API
Run the program once, and it will guide you through setting up the Google API.

## Usage (scripts)
### Prepare data
Copy and paste the table into `data/email-list.txt`.
### Run the program
Run `run.sh` (can be run by double-clicking as well)
The first time it is run, you will need to authenticate with the account that you want to upload the drafts to. A browser window should be opened automatically to do this in (if it is not, copy and paste the URL from the terminal window into your browser). The authentication flow may not work in Firefox or other Gecko-based browsers, so try Chrome, Safari, or another Chromium- or Webkit-based browser if it doesn't work for you.

## Usage (GUI)
The utility provides two GUI binaries: `email-generator-gui` and `email-template-editor-gui`. These take no command line arguments.