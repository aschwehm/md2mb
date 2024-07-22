#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Frédéric Grosshans, 19 January 2012
Nathan R. Yergler, 6 June 2010

This file does not contain sufficient creative expression to invoke
assertion of copyright. No warranty is expressed or implied; use at
your own risk.

---

Uses Python's included mailbox library to convert mail archives from
maildir [http://en.wikipedia.org/wiki/Maildir] to 
mbox [http://en.wikipedia.org/wiki/Mbox] format, icluding subfolder.

See http://docs.python.org/library/mailbox.html#mailbox.Mailbox for 
full documentation on this library.

---

To run, save as md2mb.py and run:

$ python md2mb.py [maildir_path] [mbox_filename]

[maildir_path] should be the the path to the actual maildir (containing new, 
cur, tmp, and the subfolders, which are hidden directories with names like 
.subfolde.subsubfolder.subsubsbfolder);

[mbox_filename] will be newly created, as well as a [mbox_filename].sbd the 
directory.
"""

import mailbox
import sys
import email
import os
import argparse

def remove_lockfile(lockfile):
    """Remove lock file if it exists.
    
    Args:
        lockfile (str): Path to the lock file.
    
    This function checks if a lock file exists at the specified path and removes it.
    """
    if os.path.exists(lockfile):
        os.remove(lockfile)

def message_from_binary_file(file):
    """Convert a binary file-like object to a message object.
    
    Args:
        file (file-like object): A binary file-like object containing the email message.
    
    Returns:
        email.message.Message: An email message object parsed from the binary file.
    
    This function reads a binary file-like object and converts it to an email message object using the email library.
    """
    return email.message_from_bytes(file.read())

def is_valid_maildir(dirname):
    """Check if a directory is a valid Maildir.
    
    Args:
        dirname (str): Path to the directory.
    
    Returns:
        bool: True if the directory is a valid Maildir, False otherwise.
    
    This function checks if the specified directory contains the subdirectories 'cur', 'new', and 'tmp', 
    which are required for it to be a valid Maildir.
    """
    return all(os.path.isdir(os.path.join(dirname, subdir)) for subdir in ['cur', 'new', 'tmp'])

def maildir2mailbox(maildirname, mboxfilename, verbose=False):
    """
    Convert a Maildir to an mbox file.
    
    Args:
        maildirname (str): Path to the Maildir directory.
        mboxfilename (str): Path to the output mbox file.
        verbose (bool): Enable verbose output if True.
    
    This function converts an existing Maildir to an mbox file by iterating over all messages in the Maildir 
    and adding them to the mbox file.
    """
    # Open the existing maildir and the target mbox file
    maildir = mailbox.Maildir(maildirname, factory=message_from_binary_file)
    mbox = mailbox.mbox(mboxfilename)

    # Define the lock file path
    lockfile = mboxfilename + '.lock'

    # Remove the lock file if it exists
    remove_lockfile(lockfile)

    # Lock the mbox
    mbox.lock()

    if verbose:
        print(f"Processing {maildirname} -> {mboxfilename}")

    # Iterate over messages in the maildir and add to the mbox
    for msg in maildir:
        mbox.add(msg)
        if verbose:
            print(f"Added message {msg['subject']}")

    # Close and unlock
    mbox.close()
    maildir.close()

def process_maildir(dirname, mboxname, basepath='', verbose=False):
    """
    Recursively process a maildir and its subdirectories.
    
    Args:
        dirname (str): Path to the Maildir directory.
        mboxname (str): Name of the output mbox file.
        basepath (str): Base path for output mbox files.
        verbose (bool): Enable verbose output if True.
    
    This function processes a Maildir and its subdirectories recursively, converting each to an mbox file.
    """
    mboxdirname = os.path.join(basepath, mboxname + '.sbd')
    if not os.path.exists(mboxdirname):
        os.makedirs(mboxdirname)

    if is_valid_maildir(dirname):
        maildir2mailbox(dirname, os.path.join(basepath, mboxname), verbose)
    else:
        if verbose:
            print(f"Skipping invalid Maildir: {dirname}")

    for entry in os.listdir(dirname):
        entry_path = os.path.join(dirname, entry)
        if os.path.isdir(entry_path) and entry not in ['new', 'cur', 'tmp']:
            sub_mboxname = entry.replace('.', '_')
            sub_basepath = os.path.join(mboxdirname, sub_mboxname)
            if verbose:
                print(f'Processing subdirectory {entry_path} -> {sub_basepath}')
            process_maildir(entry_path, sub_mboxname, basepath=basepath, verbose=verbose)

# Main script execution
def main():
    parser = argparse.ArgumentParser(description='Convert maildir to mbox format.')
    parser.add_argument('maildir_path', help='Path to the maildir directory')
    parser.add_argument('mbox_filename', help='Name of the output mbox file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    print(f"{args.maildir_path} -> {args.mbox_filename}")
    process_maildir(args.maildir_path, args.mbox_filename, verbose=args.verbose)
    print('Done')

if __name__ == '__main__':
    main()

