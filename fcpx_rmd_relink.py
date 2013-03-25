#!/usr/bin/env python

"""
Tool to relink Final Cut Pro X events with .RMD files generated
elsewhere.

This is a little helper script that aides in a particular workflow
when using RED cameras and FCP-X.  There's an issue in FCP-X when not
copying the original R3D files into a FCPX Event.  If there was no
.RMD sidecar when the clip was imported, and a RMD was later generated
by REDCINE-X (or other software), FCPX will not find the .RMD file.

This script creates the appropriate links back to the original RMD
files for use by FCPX.
"""

import argparse
import os
import os.path

def get_orig_media_dirs(path):
    """
    Get the list of subdirectories in the original media folder within
    a FCPX event.
    """
    dirs = []
    for dirname, dirnames, filenames in os.walk(path):
        for subdir in dirnames:
            dirs.append(
                os.path.join(dirname, subdir))
    return dirs

def relink(rdc_dir, media_dirs):
    """
    Relink the source R3D files with the RMD's in a
    separate directory.

    rdc_dir: This is the folder that contains your folder full of .RDC
    folders.  .RDC folders are the clip folders created by the RED
    EPIC that contain the clips.

    media_dirs: List of folders under Original Media in the Final Cut
    Pro X event.
    """
    for md in media_dirs:
        rmd_basename = os.path.basename(md)+'.RMD'
        src = os.path.join(
            rdc_dir,
            os.path.basename(
                md)) + '.RDC'
        rmd = os.path.join(
            src,
            rmd_basename)

        target_rmd = os.path.join(
            md, rmd_basename)

        if not os.path.exists(rmd):
            continue

        if (os.path.exists(rmd) and
            os.path.exists(target_rmd) and
            not os.path.samefile(rmd, target_rmd)):
            print 'updating symlink to %s' % rmd
            os.remove(target_rmd)
            os.symlink(rmd, target_rmd)
        elif (os.path.exists(rmd) and
              not os.path.exists(target_rmd)):
            print 'creating symlink to %s' % rmd
            os.symlink(rmd, target_rmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Relink RMDs with FCPX Events')
    parser.add_argument(
        'source_dir',
        help='Path to your .RDC directories')
    parser.add_argument(
        'event_dir',
        help='Path to the FCP Event directory')

    args = parser.parse_args()

    if not os.path.exists(args.source_dir):
        print 'source directory does not exist'
        exit(1)

    if not os.path.exists(args.event_dir):
        print 'event directory does not exist'
        exit(1)

    orig_media_dir = os.path.join(
        args.event_dir,
        'Original Media')

    media_dirs = get_orig_media_dirs(orig_media_dir)

    relink(args.source_dir, media_dirs)




