''' Reading and writing NumPY arrays in various image formats

Supported formats:
    
     - :py:mod:`EMAN2/SPARX <formats.eman_format>`
     - :py:mod:`MRC <formats.mrc>`
     - :py:mod:`SPIDER <formats.spider>`

.. Created on Aug 11, 2012
.. codeauthor:: Robert Langlois <rl2528@columbia.edu>
'''
import logging, os
from ..app import tracing
from formats import spider, eman_format as spider_writer
from ..metadata import spider_utility 
from ..parallel import process_tasks, process_queue
import numpy

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def read_image_mat(filename, label, image_processor, shared=False, **extra):
    '''Create a matrix where each row is an image
    
    :Parameters:
    
    filename : str
               Name of the file
    label : array
            Array of selected indicies
    image_processor : function
                      Extract features from the image 
    shared : bool
             If True create a shared memory array
    extra : dict
            Unused keyword arguments
            
    :Returns:
    
    mat : array
          2D matrix where each row is an image
    '''
    
    if not isinstance(filename, dict) and not hasattr(filename, 'find'): filename=filename[0]
    if hasattr(label, 'ndim') and label.ndim == 2:
        filename = spider_utility.spider_filename(filename, int(label[0, 0]))
        index = int(label[0, 1])
    else: index = int(label[0])
    img1 = read_image(filename, index)
    img = image_processor(img1, 0, **extra).ravel()
    if shared:
        mat, shmem_mat = process_queue.create_global_dense_matrix( ( len(label), img.shape[0] )  )
    else:
        mat = numpy.zeros((len(label), img.shape[0]))
        shmem_mat = mat
    for row, data in process_tasks.for_process_mp(iter_images(filename, label), image_processor, img1.shape, **extra):
        mat[row, :] = data.ravel()[:img.shape[0]]
    return shmem_mat

def is_spider_format(filename):
    ''' Test if input file is in SPIDER format
    
    :Parameters:
    
    filename : str
               Input filename to test
    
    :Returns:
    
    is_spider : bool
                True if file is in SPIDER format
    '''
    
    return spider.is_readable(filename)

def copy_to_spider(filename, tempfile):
    ''' Test if input file is in SPIDER format, if not copy to tempfile
    
    :Parameters:
    
    filename : str
               Input filename to test
    tempfile : str
               Output filename (if input file not SPIDER format)
    
    :Returns:
    
    spider_file : str
                  Name of a file containing the image in SPIDER format
    '''
    
    if is_spider_format(filename): return filename
    
    img = read_image(filename)
    spider_writer.write_image(tempfile, img)
    #for index, img in enumerate(iter_images(filename)):
    #    spider_writer.write_image(tempfile, img, index)
    return tempfile

def is_readable(filename):
    ''' Test if the input filename of the image is in a recognized
    format.
    
    :Parameters:
    
    filename : str
               Input filename to test
    
    :Returns:
    
    read : bool
           True if the format is recognized
    '''
    
    if not os.path.exists(filename): raise IOError, "Cannot find file: %s"%filename
    return get_read_format(filename) is not None

def read_header(filename, index=None):
    '''Read the header of an image from the given file
    
    :Parameters:
    
    filename : str
               Input filename to read
    index : int, optional
            Index of image to get, if None, first image (Default: None)
    
    :Returns:
        
    out : array
          Array with header information in the file
    '''
    
    if not os.path.exists(filename): raise IOError, "Cannot find file: %s"%filename
    format = get_read_format(filename)
    if format is None: 
        raise IOError, "Could not find format for %s"%filename
    return format.read_header(filename, index)

def read_image(filename, index=None):
    '''Read an image from the given file
    
    :Parameters:
    
    filename : str
               Input filename to read
    index : int, optional
            Index of image to get, if None, first image (Default: None)
    
    :Returns:
        
    out : array
          Array with header information in the file
    '''
    
    if not os.path.exists(filename): raise IOError, "Cannot find file: %s"%filename
    format = get_read_format(filename)
    if format is None: 
        raise IOError, "Could not find format for %s"%filename
    return format.read_image(filename, index)

def iter_images(filename, index=None):
    ''' Read a set of images from the given file
    
    :Parameters:
    
    filename : str
               Input filename to read
    index : int or array, optional
            Index of image to start or array of selected images, if None, start with the first image (Default: None)
    
    :Returns:
        
    out : array
          Array with header information in the file
        
    .. todo:: iter single images
    '''
    
    if index is not None and hasattr(index, 'ndim'):
        if index.ndim == 2 and index.shape[1]>1:
            beg = 0
            tot = len(numpy.unique(index[:, 0].astype(numpy.int)))
            if not isinstance(filename, dict) and not hasattr(filename, 'find'): filename=filename[0]
            for i in xrange(tot):
                id = index[beg, 0]
                filename = spider_utility.spider_filename(filename, int(id)) if not isinstance(filename, dict) else filename[int(id)]
                sel = numpy.argwhere(id == index[:, 0]).ravel()
                if beg != sel[0]: raise ValueError, "Array must be sorted by file ids: %d != %d -- %f, %f"%((beg), sel[0], index[beg, 0], beg)
                for img in iter_images(filename, index[sel, 1]):
                    yield img
                beg += sel.shape[0]
            
            '''
            fileid = index[:, 0].astype(numpy.int)
            ids = numpy.unique(fileid)
            if not isinstance(filename, dict) and not hasattr(filename, 'find'): filename=filename[0]
            for id in ids:
                filename = spider_utility.spider_filename(filename, int(id)) if not isinstance(filename, dict) else filename[int(id)]
                for img in iter_images(filename, index[id == fileid, 1]):
                    yield img
            '''
            return
    if not os.path.exists(filename): raise IOError, "Cannot find file: %s"%filename
    format = get_read_format(filename)
    if format is None: raise IOError, "Could not find format for %s"%filename
    for img in format.iter_images(filename, index):
        yield img

def count_images(filename):
    ''' Count the number of images in the file
    
    :Parameters:
    
    filename : str
               Input filename to read
    
    :Returns:
        
    out : int
          Number of images in the file
    '''
    
    if isinstance(filename, list):
    
        if not os.path.exists(filename[0]): raise IOError, "Cannot find file: %s"%filename
        format = get_read_format(filename[0])
        total = 0
        for f in filename:
            total += format.count_images(f)
        return total
    else:
        if not os.path.exists(filename): raise IOError, "Cannot find file: %s"%filename
        format = get_read_format(filename)
    if format is None: 
        raise IOError, "Could not find format for %s"%filename
    return format.count_images(filename)

def is_writable(filename):
    ''' Test if the image extension of the given filename is understood
    as a writable format.
    
    :Parameters:
    
    filename : str
               Output filename to test
    
    :Returns:
    
    write : bool
            True if the format is recognized
    '''
    
    return get_write_format(filename) is not None

def write_image(filename, img, index=None):
    ''' Write the given image to the given filename using a format
    based on the file extension, or given type.
    
    :Parameters:
    
    filename : str
               Output filename for the image
    img : array
          Image data to write out
    index : int, optional
            Index image should be written to in the stack
    '''
    
    if index is not None and index == 0 and os.path.exists(filename):
        os.unlink(filename)
    
    format = get_write_format(filename)
    if format is None: 
        raise IOError, "Could not find format for extension of %s"%filename
    format.write_image(filename, img, index)
    
def write_stack(filename, imgs):
    ''' Write the given image to the given filename using a format
    based on the file extension, or given type.
    
    :Parameters:
    
    filename : str
               Output filename for the image
    imgs : array
           Image stack data to write out
    '''
    
    format = get_write_format(filename)
    if format is None: 
        raise IOError, "Could not find format for extension of %s"%filename
    index = 0
    for img in imgs:
        format.write_image(filename, img, index)
        index += 1

def get_write_format(filename):
    ''' Get the write format for the image
    
    :Parameters:
    
    filename : str
               Output filename to test
    
    :Returns:
    
    write : format
            Write format for given file extension
    '''
    
    for f in _formats:
        if f.is_writable(filename): return f
    return _default_write_format

def get_read_format(filename):
    ''' Get the write format for the image
    
    :Parameters:
    
    filename : str
               Input file to test
    
    :Returns:
    
    write : format
            Read format for given file
    '''
    
    for f in _formats:
        if f.is_readable(filename): return f
    return None


def _load():
    ''' Import available formats
    '''
    
    from formats import mrc
    formats = [mrc]
    try: from formats import eman_format
    except: tracing.log_import_error("Cannot load EMAN2 - supported image formats will not be available - see documentation for more details")
    else: formats.append(eman_format)
    if len(formats) == 0: raise ImportError, "No image format modules loaded!"
    return formats, eman_format

_formats, _default_write_format = _load()

