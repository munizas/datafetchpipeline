#!/usr/bin/env python

from config.config import Config
import optparse
import re
import sys
import os
from datetime import date

class WgetLogValidator:
    def __init__(self):
        # regular expressions:
        # regexp denoting successful collection index/directory listing save:
        self.cindex      = re.compile(r'(index|listing).*saved')

        # regexp for timestamp string containing an 'http' hdf (or xml) target:
        self.timestamp   = r'--\d{4}-\d{2}-\d{2} *\d{2}:\d{2}:\d{2}--'
        self.target      = r'(http|ftp).*\.(hdf|nc).*$'
        self.regex_save_loc    = ".*('/.*/.*') saved.*"
        self.timestamp_and_target = re.compile( self.timestamp + ' *' + '(' + self.target + ')')    # save target as group

        self.regex_saved_file_loc = re.compile(r'=> (\'.*\')')

        # regexp denoting target was successfully downloaded (saved):
        self.saved       = re.compile(r'saved')

        # regexp denoting overall completion:
        self.finished    = re.compile(r'FINISHED')

        # regex for 'Remote file no newer than local file'
        self.regex_no_retrieve = re.compile(r'Remote file no newer than local file*not retrieving\.')

        # regex for 'failed: Network is unreachable'
        self.regex_unreachable_network = re.compile(r'Connecting.*failed: Network is unreachable')

        self.download_list = []
        self.saved_file_locs = []

        self.summary = 'Wget Log Summary (' + str(date.today()) + '):*************************************************************************\n\n'

        self.config = Config()

    def summary_str(self):
        return self.summary

    def downloaded_filenames(self):
        return self.download_list

    def saved_file_locs(self):
        return self.saved_file_locs

    def file_count(self):
        return len(self.download_list)

    def str_file_count(self):
        return "file download count = " + str(self.file_count())

    def validate_logs(self, logfiles):
        # write new download file paths to preconlist.txt
        precon = open(self.config.preconfilename(), 'w')

        for logfilename in logfiles:

            # logicals, re match objects for checking status of download requests:

            cindex_present  = False         # collection index presence
            downloading     = False         # True at start of a reqest, False when complete.
            err             = False         # True for incomplete downloads.
            tt_match        = None          # timestamp and target match object.
            tt_match_prev   = None          # prior match object for possible failed request
                                            # reporting.
            tt_match_this_line  = False     # timestamp and target match on this line.
            _finished_      = False         # 'FINISHED' all files in collection
            saved_match     = []            # 'saved' string match object
            errlist         = []            # list of failed download targets.
            should_finish   = False

            logfile = ''
            try:
                logfile = open(logfilename)
            except IOError as e:
                print e;

            # for individual file download checks, scan through the "noise" in the file,
            # looking for typical download start/end signatures, taking note of those that
            # are incomplete:

            for line in logfile:

                # timestamp and target request match?
                if self.timestamp_and_target.match(line):
                    should_finish = True

                #if timestamp_and_target.match(line) and not get_request.search(line):
                    tt_match_this_line=True
                    if tt_match:
                        tt_match_prev = tt_match
                    tt_match = self.timestamp_and_target.match(line)

                # "saved" string match?
                saved_match = self.saved.search(line)

                # check process status:
                if tt_match_this_line and not downloading:
                    # start of new request
                    downloading = True
                elif tt_match_this_line and downloading and \
                     tt_match.group(1)!=tt_match_prev.group(1):
                    # new download request without successful completion of prior one
                    # (sometimes wget attempts to re-download a target, which is perfectly
                    # ok, thus the check against the previous target)
                    err = True
                elif downloading and saved_match:
                    # successful completion; reset logicals
                    downloading = False
                    saved_match = None
                    self.download_list.append('\'' + tt_match.group(1) + '\'')
                    self.saved_file_locs.append(re.search(self.regex_save_loc, line).group(1))
                elif self.finished.match(line):
                    _finished_  = True
                elif self.regex_saved_file_loc.search(line):
                    if ".listing" not in self.regex_saved_file_loc.search(line).group(1):
                        self.saved_file_locs.append(self.regex_saved_file_loc.search(line).group(1))
                elif self.regex_unreachable_network.search(line):
                    self.summary += 'Unable to connect, network is unreachable.\n'

                if err:
                    # capture target of failed request
                    errlist.append(tt_match_prev.group(1))

                # continue download error search:
                err = False
                tt_match_this_line = False

            # last attempted download complete?:
            if should_finish and not _finished_:
                try:
                    errlist.append('download aborted during read of '+tt_match.group(1))
                except:
                    errlist.append('download aborted.')

            self.summary += '\nlog file at: ' + logfilename + '\n\n'

            # summary output:
            if errlist.__len__():
                print '%s:' % logfilename
                print '   error(s) downloading the following files in the collection:'
                for failed_target in errlist:
                    print '   %s' % failed_target

            if len(self.saved_file_locs) > 0:
                mo = re.search(self.config.redataproduct(), logfilename)
                download_size = 0
                isPrecon = mo and mo.group(1) in self.config.preconwatch() # check if this logfile is monitored for precon processing
                for f in self.saved_file_locs:
                    f = f.replace("'", "")
                    download_size += os.path.getsize(f) # remove single quotes
                    if isPrecon:
                        precon.write(f + '\n')
                self.summary += 'files downloaded: ' + str(len(self.saved_file_locs)) + '\n'
                self.summary += 'total download size: ' + str(download_size/1000000000.0) + ' GB\n'
                self.summary += 'saved to location: ' + re.search('/.*/', self.saved_file_locs[0][1:-1]).group() + '\n'
            else:
                self.summary += 'no files downloaded\n'
            
            del self.download_list[:]
            del self.saved_file_locs[:]

            self.summary += '\n*******************************************************************************************************\n\n'

        precon.close()
        # if nothing was written, delete empty file
        if os.path.getsize(self.config.preconfilename()) == 0:
            os.remove(self.config.preconfilename())

if __name__ == '__main__':
    w = WgetLogValidator()
    logs = ['/Users/asmuniz/ProjectCode/data/MOD04_L2/logs/2015-06-30-MOD04_L2grid(240)-2013.log', '/Users/asmuniz/ProjectCode/data/MCD12Q1.051/logs/2015-07-03-2012.01.01.log', '/Users/asmuniz/Desktop/develop/project-info/gregg_data_processing/success.log', '/Users/asmuniz/Desktop/develop/project-info/gregg_data_processing/no-re-retrieve.log', '/Users/asmuniz/Desktop/develop/project-info/gregg_data_processing/network-error.log']
    w.validate_logs(logs)
    print w.summary_str()