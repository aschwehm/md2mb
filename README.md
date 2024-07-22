# md2mb Fork - Maildir to Mbox Converter

## Overview

This repository is a fork of [mjbeverley's md2mb](https://github.com/mjbeverley/md2mb), a script designed to convert mail archives from Maildir format to Mbox format, including subfolders. This fork includes enhancements and additional features for improved functionality and usability.

## Changes from the Original Script

### Enhancements in This Fork

1. **Modularized Functions**: The script has been modularized into individual functions for better readability and maintainability. Functions such as `remove_lockfile`, `message_from_binary_file`, `is_valid_maildir`, and `maildir2mailbox` have been added to encapsulate specific tasks.

2. **Verbose Output Option**: An optional verbose output has been added to provide detailed information during the conversion process. This is useful for debugging and ensuring that all messages are being processed correctly.

3. **Recursive Processing**: The `process_maildir` function has been added to handle the recursive processing of Maildir directories and their subdirectories. This ensures that all messages, including those in nested folders, are converted.

4. **Command-line Interface**: The script now uses the `argparse` library to handle command-line arguments, making it easier to specify the Maildir path, Mbox filename, and enable verbose output.

5. **Lock File Management**: Added functionality to handle the removal of lock files before processing the Mbox file to prevent locking issues.

6. **Compatibility with Python 3**: The script has been updated to be compatible with Python 3, including changes to the way messages are read and converted.
