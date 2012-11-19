''' Converts a set of micrographs into SPIDER format

This script (`ara-convert2spi`) converts a set of micrographs in most formats to SPIDER format. It also
renames the files to ensure SPIDER compatiblity. A selection file is written out to track the mapping.

Tips
====
 
 #. Output filename: Must follow the SPIDER format with a number before the extension, e.g. mic_00001.spi. Output files just require the number of digits: `--output sndc_0000.spi`

Running Script
===============

.. sourcecode :: sh
    
    # Source AutoPart - FrankLab only
    
    $ source /guam.raid.cluster.software/arachnid/arachnid.rc
    
    # Example usage - Convert raw CCD micrographs
    
    $ ara-convert2spi mics/* -o mic_0000.spi
    
    # Example usage - Convert a set of film micrographs
    
    $ ara-convert2spi mics/* -o mic_0000.spi --film

Critical Options
================

.. program:: ara-selrelion

.. option:: -i <filename1,filename2>, --input-files <filename1,filename2>, filename1 filename
    
    List of filenames for the input micrographs.
    If you use the parameters `-i` or `--inputfiles` they must be comma separated 
    (no spaces). If you do not use a flag, then separate by spaces. For a 
    very large number of files (>5000) use `-i "filename*"`

.. option:: -o <str>, --output <str>
    
    Output filename for the relion selection file

Other Options
=============

This is not a complete list of options available to this script, for additional options see:

    #. :ref:`Options shared by all scripts ... <shared-options>`

.. Created on Nov 13, 2012
.. codeauthor:: Robert Langlois <rl2528@columbia.edu>
'''
from ..core.app import program
from ..core.metadata import spider_utility, format_utility, format
from ..core.image import ndimage_file, ndimage_utility
import logging, os

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def batch(files, output, film=False, **extra):
    '''Convert a set of micrographs to SPIDER
    
    :Parameters:
    
    filename : list
               List of micrographs names
    output : str
             Output SPIDER filename template
    film : bool
           Set true if input micrographs are film (or do not need to be inverted)
    extra : dict
            Unused key word arguments
    '''
    
    seloutput=format_utility.add_prefix(output, "sel")
    if os.path.exists(seloutput):
        selection = format.read(seloutput, numeric=True)
        check = dict(selection)
        update = []
        index = len(selection)+1
        for filename in files:
            if filename not in check:
                selection.append((filename, index))
                update.append((filename, index))
                index += 1
            elif not os.path.exists(spider_utility.spider_filename(output, index)):
                update.append((filename, check[filename]))
    else:
        selection = []
        index = 1
        for filename in files:
            selection.append((filename, index))
        update = selection
    format.write(seloutput, os.path.splitext(selection)[0]+".star")
    
    for filename, index in update:
        img = ndimage_file.read_image(filename)
        if not film: ndimage_utility.invert(img, img)
        ndimage_file.spider_writer.write_image(spider_utility.spider_filename(output, index), img)
    _logger.info("Completed")

def setup_options(parser, pgroup=None, main_option=False):
    # Collection of options necessary to use functions in this script
    
    from ..core.app.settings import OptionGroup
    group = OptionGroup(parser, "SPIDER Conversion", "Options to control SPIDER conversion",  id=__name__)
    group.add_option("-g", film=False, help="Set true if micrograph is film or inverted CCD")
    pgroup.add_option_group(group)
    if main_option:
        pgroup.add_option("-i", input_files=[], help="List of filenames for the input stacks or selection file", required_file=True, gui=dict(filetype="file-list"))
        pgroup.add_option("-o", output="",      help="Output filename for the relion selection file", gui=dict(filetype="save"), required_file=True)
        parser.change_default(log_level=3)

'''
def check_options(options, main_option=False):
    #Check if the option values are valid
    
    from ..core.app.settings import OptionValueError
'''

def main():
    #Main entry point for this script
    
    program.run_hybrid_program(__name__,
        description = '''Converts a set of micrographs into SPIDER format
        
                         http://
                         
                         Example: Convert raw CCD micrographs
                         
                         $ ara-convert2spi mics/* -o mic_0000.spi
                         
                         Example: Convert a set of film micrographs
                         
                         $ ara-convert2spi mics/* -o mic_0000.spi --film
                      ''',
        supports_MPI = False,
        use_version = False,
    )
def dependents(): return []
if __name__ == "__main__": main()

