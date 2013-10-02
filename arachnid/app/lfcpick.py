''' Semi-automated particle selection (LFCPick)

This script (`ara-lfcpick`) was designed to locate potential particles on a micrograph using template-matching. A user
should spend time tuning the number of particles returned to limit the number of noise windows found. Also, a manual
selection is generally performed to remove contamination.

Tips
====

 #. Filenames: Must follow the SPIDER format with a number before the extension, e.g. mic_00001.spi. Output files just require the number of digits: `--output sndc_0000.spi`

 #. CCD micrographs - Use the `--invert` parameter to invert CCD micrographs. In this way, you can work directly with the original TIFF
 
 #. Decimation - Use the `--bin-factor` parameter to reduce the size of the micrograph for more efficient processing. Your coordinates will be on the full micrograph.
 
 #. Restart - After a crash, you can restart where you left off by specifying restart file (a list of files already processed). One is automatically created in each run called
    .restart.autopick and can be used as follows: `--restart-file .restart.autopick`
    
 #. Parallel Processing - Several micrographs can be run in parallel (assuming you have the memory and cores available). `-p 8` will run 8 micrographs in parallel. 

Examples
========

.. sourcecode :: sh

    # Source AutoPart - FrankLab only
    
    $ source /guam.raid.cluster.software/arachnid/arachnid.rc
    
    # Run with a disk as a template on a raw film micrograph
    
    $ ara-lfcpick mic_*.spi -o sndc_00001.spi -r 110 -w 312
    
    # Run with a disk as a template on a raw CCD micrograph
    
    $ ara-lfcpick mic_*.spi -o sndc_00001.spi -r 110 -w 312 --invert

Critical Options
================

.. program:: ara-lfcpick

.. option:: -i <FILENAME1,FILENAME2>, --input-files <FILENAME1,FILENAME2>, FILENAME1 FILENAME2
    
    List of filenames for the input micrographs.
    If you use the parameters `-i` or `--inputfiles` they must be comma separated 
    (no spaces). If you do not use a flag, then separate by spaces. For a 
    very large number of files (>5000) use `-i "filename*"`

.. option:: -o <FILENAME>, --output <FILENAME>
    
    Output filename for the coordinate file with correct number of digits (e.g. sndc_0000.spi)

.. option:: -r <int>, --pixel-radius <int>
    
    Size of your particle in pixels. If you decimate with `--bin-factor` give the undecimated pixel size.

Useful Options
===============

These options 

.. program:: ara-lfcpick

.. option:: --template <FILENAME>
    
    An input filename of a template to use in template-matching. If this is not specified then a Gaussian smoothed disk is used of radius 
    `disk-mult*pixel-radius`.

.. option:: -w <int>, --worker-count <int>
    
    Set the number of micrographs to process in parallel (keep in mind memory and processor restrictions)
    
.. option:: --invert
    
    Invert the contrast of CCD micrographs
    
.. option:: --bin-factor <int>
    
    Decimate the micrograph to speed up computation time

.. option:: --disable-bin <BOOL>
    
    Disable micrograph decimation
    
.. option:: --restart-file <FILENAME>

    If the script crashes, the restart file will allow it to pick up where it left off. If you did not specify one, 
     then .restart.autopick is automatically created. Just specify that as the filename on the next run and it will restart. If no
     restart file exists one is created with the name given (or .restart.autopick if none is given).

Tunable Options
===============

Generally, these options do not need to be changed, their default parameters have proven successful on many datasets. However,
you may enounter a dataset that does not react properly and these options can be adjusted to get the best possible particle
selection.

.. program:: ara-lfcpick

.. option:: --dist-mult <float>
    
    This multipler scales the radius of the Gaussian smooth disk (which is used when no template is specified).

.. option:: --overlap-mult <float>
    
    Multiplier for the amount of allowed overlap or inter-particle distance.

.. option:: --limit <int>
    
    Number of windows to return

Other Options
=============

This is not a complete list of options available to this script, for additional options see:

    #. :ref:`Options shared by all scripts ... <shared-options>`
    #. :ref:`Options shared by MPI-enabled scripts... <mpi-options>`
    #. :ref:`Options shared by file processor scripts... <file-proc-options>`
    #. :ref:`Options shared by SPIDER params scripts... <param-options>`


.. Created on Aug 2, 2012
.. codeauthor:: Robert Langlois <rl2528@columbia.edu>
'''
from ..core.app.program import run_hybrid_program
from ..core.image import eman2_utility, ndimage_utility, ndimage_file
from ..core.metadata import format_utility, format, spider_params, spider_utility
from ..core.parallel import mpi_utility
from ..util import bench as benchmark
import os, logging
import numpy

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def process(filename, id_len=0, **extra):
    '''Concatenate files and write to a single output file
    
    :Parameters:
        
    filename : str
               Input filename
    id_len : int
             Maximum length of the ID
    extra : dict
            Unused key word arguments
                
    :Returns:
        
    filename : string
          Current filename
    peaks : numpy.ndarray
             List of peaks and coordinates
    '''
    
    spider_utility.update_spider_files(extra, spider_utility.spider_id(filename, id_len), 'good_coords', 'output', 'good')    
    mic = read_micrograph(filename, **extra)
    peaks = search(mic, **extra)
    coords = format_utility.create_namedtuple_list(peaks, "Coord", "id,peak,x,y", numpy.arange(1, peaks.shape[0]+1, dtype=numpy.int))
    format.write(extra['output'], coords, default_format=format.spiderdoc)
    return filename, peaks

def search(img, use_spectrum=False, overlap_mult=1.2, limit=0, noise=False, **extra):
    ''' Search a micrograph for particles using a template
    
    :Parameters:
        
    img : EMData
          Micrograph image
    use_spectrum : bool
                   Set True to use spectrum correlation
    overlap_mult : float
                   Amount of allowed overlap
    extra : dict
            Unused key word arguments
    
    :Returns:
        
    peaks : numpy.ndarray
            List of peaks and coordinates
    '''
    
    template = create_template(**extra)
    radius, offset, bin_factor, mask = init_param(**extra)
    if noise:
        if eman2_utility.is_em(img):
            emimg = img
            img = eman2_utility.em2numpy(emimg)
        if eman2_utility.is_em(template):
            emtemplate = template
            template = eman2_utility.em2numpy(emtemplate)
        cc_map = ndimage_utility.cross_correlate(img, template)
    elif use_spectrum: cc_map = scf_center(img, template, mask)
    else: cc_map = lfc(img, template, mask)
    if noise: 
        numpy.fabs(cc_map, cc_map)
        cc_map -= numpy.max(cc_map)
        cc_map *= -1
    peaks = search_peaks(cc_map, radius, overlap_mult)
    peaks = numpy.asarray(peaks).squeeze()
    if peaks.shape[0] < 2: raise ValueError, "No peaks found"
    if peaks.ndim == 1: peaks = peaks.reshape((len(peaks)/3, 3))
    peaks[:, 1:3] *= bin_factor
    index = numpy.argsort(peaks[:,0])[::-1]
    if limit > 0 and len(index) > limit: index = index[:limit]
    try:
        peaks = peaks[index].copy().squeeze()
    except:
        _logger.error("peaks: %s != %s"%(str(peaks.shape), str(index.shape))) # --- %d, %d", numpy.min(index), numpy.max(index)))
        raise
    return peaks

def search_peaks(cc_map, radius, overlap_mult, peak_last=None):
    ''' Search a cross-correlation map for peaks
    
    :Parameters:
        
    cc_map : EMData
             Cross-correlation map
    radius : int
             Radius of the particle in pixels
    overlap_mult : float
                   Fraction of allowed overlap
    peak_last : list, optional
                Previous set of peaks to merge (if None, ignored)
    
    :Returns:
    
    peaks : list
            List of peaks and coordinates
    '''
    
    if 1 == 0:
        peaks = cc_map.peak_ccf(radius*overlap_mult)
        if peak_last is not None: peaks = eman2_utility.EMAN2.Util.merge_peaks(peak_last, peaks, 2*radius)
    else:
        #noise
        peaks = ndimage_utility.find_peaks_fast(cc_map, radius*overlap_mult)
        if peak_last is not None:
            cc_map[:, :] = 0
            cc_map[peaks[:, 1:]] = peaks[:, 0]
            cc_map[peak_last[:, 1:]] = peak_last[:, 0]
            peaks = ndimage_utility.find_peaks_fast(cc_map, radius*overlap_mult)
    return peaks

def scf_center(img, template, mask):
    ''' Variant of the spectrum correlation function
    
    :Parameters:
        
    img : EMData
          Micrograph
    template : EMData
               Template
    mask : EMData
           Mask for variance map or variance map
    
    :Returns:
        
    cc_map : EMData
             Spectrum enhanced cross-correlation map
             
    .. todo:: replace acf with fftconvolve
    
         > r = numpy.correlate(x, x)
    '''
    
    cc_map = lfc(img, template, mask)
    template = eman2_utility.acf(template)
    map2 = lfc(cc_map, template, mask)
    cc_map.mult(map2)
    return cc_map

def lfc(img, template, mask):
    ''' Locally normalized fast cross-correlation
    
    :Parameters:
        
    img : EMData
          Micrograph
    template : EMData
          Template
    mask : EMData
           Mask for variance map or variance map
    
    :Returns:
        
    cc_map : EMData
             Cross-correlation map
    
    def fft_correlate(A,B,*args,**kwargs):
    return S.signal.fftconvolve(A,B[::-1,::-1,...],*args,**kwargs)
    '''
    
    if 1 == 0:
        cc_map = img.calc_ccf(template)
        cc_map.process_inplace("xform.phaseorigin.tocenter")
        if mask.get_xsize() < img.get_xsize():
            inv_sigma_image = img.calc_fast_sigma_image(mask)
            inv_sigma_image.process_inplace("math.invert.carefully",{"zero_to": 1.0})
        else: inv_sigma_image = mask
        cc_map.mult(inv_sigma_image)
    else:
        if eman2_utility.is_em(img):
            emimg = img
            img = eman2_utility.em2numpy(emimg)
        if eman2_utility.is_em(template):
            emtemplate = template
            template = eman2_utility.em2numpy(emtemplate)
        if eman2_utility.is_em(mask):
            emmask = mask
            mask = eman2_utility.em2numpy(emmask)
        cc_map = ndimage_utility.cross_correlate(img, template)
        cc_map /= ndimage_utility.local_variance(img, mask)
        #cc_map = eman2_utility.numpy2em(cc_map)
    return cc_map

def read_micrograph(filename, emdata=None, bin_factor=1.0, sigma=1.0, disable_bin=False, invert=False, fraction=1, **extra):
    ''' Read a micrograph from a file and perform preprocessing
    
    :Parameters:
        
    filename : str
               Filename for micrograph
    emdata : EMData
             Reuse allocated memory
    bin_factor : float
                Downsampling factor
    sigma : float
            Gaussian highpass filtering factor (sigma/window)
    disable_bin : bool    
                  If True, do not downsample the micrograph
    invert : bool
             If True, invert the contrast of the micrograph (CCD Data)
    extra : dict
            Unused keyword arguments
    
    :Returns:
        
    mic : EMData
          Micrograph image
    '''
    
    count = ndimage_file.count_images(filename)
    if count > 1 and fraction > 1:
        mic = ndimage_file.read_image(filename, cache=emdata).astype(numpy.float32)
        for i in xrange(1, min(fraction, count)):
            mic += ndimage_file.read_image(filename, i, cache=emdata)
    else:
        mic = ndimage_file.read_image(filename, cache=emdata).astype(numpy.float32)

    if bin_factor > 1.0 and not disable_bin: mic = eman2_utility.decimate(mic, bin_factor)
    if invert: mic = ndimage_utility.invert(mic)
    return mic

def create_template(template, disk_mult=1.0, disable_bin=False, **extra):
    ''' Read a template from a file or create a soft disk
    
    :Parameters:
        
    template : EMData
             Cross-correlation map
    disk_mult : float
                Mulitplier to control size of soft disk template
    extra : dict
            Unused keyword arguments
    
    :Returns:
        
    template : EMData
               Template read from file or uniform disk with soft edge
    '''
    #mic = ndimage_file.read_image(template)
    if template != "": 
        img= ndimage_file.read_image(template)
        bin_factor=extra['bin_factor']
        if bin_factor > 1.0 and not disable_bin: img = eman2_utility.decimate(img, bin_factor)
        return img
    radius, offset = init_param(**extra)[:2]
    template = eman2_utility.utilities.model_circle(int(radius*disk_mult), int(offset*2), int(offset*2), 1)
    if True:
        kernel_size = int(radius) #
        if (kernel_size%2)==0: kernel_size += 1
        try:
            return eman2_utility.utilities.gauss_edge(template, kernel_size = kernel_size, gauss_standard_dev = 3)
        except:
            _logger.error("template(%d,%d) - %d, %f"%(template.get_xsize(), template.get_ysize(), radius, disk_mult))
            raise
    else: return template

def init_param(pixel_radius, pixel_diameter=0.0, window=1.0, bin_factor=1.0, **extra):
    ''' Ensure all parameters have the proper scale and create a mask
    
    :Parameters:
        
    pixel_radius : float
                  Radius of the particle
    pixel_diameter : int
                     Diameter of the particle
    window : float
             Size of the window (if less than particle diameter, assumed to be multipler)
    bin_factor : float
                 Decimation factor
    extra : dict
            Unused keyword arguments
    
    :Returns:
        
    rad : float
          Radius of particle scaled by bin_factor
    offset : int
             Half-width of the window
    bin_factor : float
                 Decimation factor
    mask : EMData
           Disk mask with `radius` that keeps data in the disk
    '''
    
    if pixel_diameter > 0:
        rad = int( float(pixel_diameter) / 2 )
        offset = int( window / 2.0 )
    else:
        rad = int( pixel_radius / float(bin_factor) )
        offset = int( window / (float(bin_factor)*2.0) )
    if window == 1.0: window = 1.4
    if window < (2*rad): offset = int(window*rad)
    width = offset*2
    mask = eman2_utility.utilities.model_circle(rad, width, width)
    _logger.debug("Radius: %d | Window: %d"%(rad, offset*2))
    return rad, offset, bin_factor, mask

def read_bench_coordinates(fid, good_coords="", good="", bin_factor=1.0, **extra):
    ''' Read benchmark coordinates
    
    :Parameters:
        
    pixel_radius : int
                   Current SPIDER ID
    good_coords : str
                  Filename for input benchmark coordinates
    good : str
           Filename for optional selection file to select good coordinates
    extra : dict
            Unused keyword arguments
    
    :Returns:
        
    coords : numpy.ndarray
             Selected (x,y) coordinates
    '''
    
    if good_coords == "" or not os.path.exists(format_utility.parse_header(good_coords)[0]): 
        return None
    coords, header = format_utility.tuple2numpy(format.read(good_coords, numeric=True, spiderid=fid))
    if good != "":
        try:
            selected = format_utility.tuple2numpy(format.read(good, numeric=True, spiderid=fid))[0].astype(numpy.int)
        except:
            return None
        else:
            selected = selected[:, 0]-1
            coords = coords[selected].copy().squeeze()
    x, y = header.index('x'), header.index('y')
    return numpy.vstack((coords[:, x], coords[:, y])).T

def find_overlap(coords, bench, bench_mult=1.2, pixel_radius=1.0, **extra):
    '''Find the overlaping coordinates with the benchmark
    
    :Parameters:
        
    coords : numpy.ndarray
             Coorindates found by algorithm
    bench : numpy.ndarray
                Set of 'good' coordinates
    pixel_radius : int
                   Radius of the particle in pixels
    bench_mult : float
                 Amount of allowed overlap (pixel_radius*bench_mult)
    
    :Returns:
        
    coords : list
             Overlapping (x,y) coordinates
    '''
    
    _logger.error("%s == %s"%(str(bench.max(0)), str(coords.max(0))))
    assert(bench.shape[1] == 2)
    bench=bench.copy()
    rad = pixel_radius*bench_mult
    pixel_radius = rad*rad
    selected = []
    if len(bench) > 0:
        for i, f in enumerate(coords):
            dist = f-bench
            numpy.square(dist, dist)
            dist = numpy.sum(dist, axis=1)
            if dist.min() < pixel_radius:
                bench[dist.argmin(), :]=(1e20, 1e20)
                selected.append((i+1, 1))
    return selected

def initialize(files, param):
    # Initialize global parameters for the script
    
    param['emdata'] = eman2_utility.EMAN2.EMData()
    param["confusion"] = numpy.zeros((len(files), 4))
    
    if mpi_utility.is_root(**param):
        if os.path.dirname(param['output']) != "":
            if not os.path.exists(os.path.dirname(param['output'])):
                os.makedirs(os.path.dirname(param['output']))
        radius, offset, bin_factor, param['mask'] = init_param(**param)
        _logger.info("Pixel radius: %d"%radius)
        _logger.info("Window size: %d"%(offset*2))
        if param['bin_factor'] > 1 and not param['disable_bin']: _logger.info("Decimate micrograph by %d"%param['bin_factor'])
        if param['invert']: _logger.info("Inverting contrast of the micrograph")
    
    assert('selection_doc' in param)
    _logger.error("selection:\"%s\""%param['selection_doc'])
    if 'selection_doc' in param and param['selection_doc'] != "":
        select = format.read(param['selection_doc'], numeric=True)
        oldcnt = len(files)
        files = spider_utility.select_subset(files, select)
        _logger.info("Selecting %d files from %d"%(len(files), oldcnt))
    return files

def reduce_all(val, confusion, file_index, **extra):
    # Process each input file in the main thread (for multi-threaded code)
    
    filename, coords = val
    info=""
    if len(coords) > 0:
        coords = format_utility.create_namedtuple_list(coords, "Coord", "id,peak,x,y", numpy.arange(1, coords.shape[0]+1, dtype=numpy.int))
        if not hasattr(coords, 'ndim') and (extra['good'] != "" or extra['good_coords'] != ""):
            try:
                vals = benchmark.benchmark(coords, filename, **extra)
            except:
                info=""
            else:
                confusion[file_index, 0] = vals[0]+vals[1]
                confusion[file_index, 1] = vals[0]+vals[3]
                confusion[file_index, 2] = vals[0]
                pre = float(confusion[file_index, 2]) / (confusion[file_index, 0]) if confusion[file_index, 0] > 0 else 0
                sen = float(confusion[file_index, 2]) / (confusion[file_index, 1]) if confusion[file_index, 1] > 0 else 0
                info = " - %d,%d,%d - precision: %f, recall: %f"%(confusion[file_index, 0], confusion[file_index, 1], confusion[file_index, 2], pre, sen)
        else:
            bench = read_bench_coordinates(filename, **extra)
            if bench is not None and len(coords) > 0:
                if bench.shape[1] != 2:
                    _logger.error("bench: %s"%str(bench.shape))
                overlap = benchmark.find_overlap(coords[:, 1:3], bench, **extra)
                confusion[file_index, 0] = len(coords) #len(peaks), len(selected), len(overlap)
                confusion[file_index, 1] = len(bench)
                confusion[file_index, 2] = len(overlap)
                assert(len(overlap) <= len(coords))
                assert(len(overlap) <= len(bench))
                pre = float(len(overlap)) / len(coords) if len(coords) > 0 else 0
                sen = float(len(overlap)) / len(bench) if len(bench)> 0 else 0
                info = " - %d,%d,%d - precision: %f, recall: %f"%(len(coords), len(bench), len(overlap), pre, sen)
    return filename+info

def finalize(files, confusion, output, **extra):
    # Finalize global parameters for the script
    
    tot = numpy.sum(confusion, axis=0)
    if tot[1] > 0:
        _logger.info("Overall - precision: %f, recall: %f - %d,%d,%d"%(tot[2]/tot[0], tot[2]/tot[1], tot[0], tot[1], tot[2]))
        format.write(os.path.splitext(output)[0]+".csv", confusion, header="pp,pos,tp,dist".split(','), prefix="summary")
    _logger.info("Completed")

def setup_options(parser, pgroup=None, main_option=False):
    # Collection of options necessary to use functions in this script
    
    from ..core.app.settings import OptionGroup
    group = OptionGroup(parser, "Template-matching", "Options to control template-matching",  id=__name__)
    group.add_option("-r", pixel_radius=0,      help="Radius of the expected particle (if default value 0, then overridden by SPIDER params file, --param-file)")
    group.add_option("",   window=1.0,          help="Size of the output window or multiplicative factor if less than particle diameter (overridden by SPIDER params file, --param-file)")
    group.add_option("",   disk_mult=0.65,      help="Disk smooth kernel size factor", gui=dict(maximum=10.0, minimum=0.01, singleStep=0.1, decimals=2)) #"2:0.1:0.01:10.0"
    group.add_option("",   overlap_mult=1.2,    help="Multiplier for the amount of allowed overlap or inter-particle distance", gui=dict(maximum=10.0, minimum=0.001, singleStep=0.1, decimals=2))
    group.add_option("",   template="",         help="Optional predefined template", gui=dict(filetype="open"))
    group.add_option("",   disable_bin=False,   help="Disable micrograph decimation")
    group.add_option("",   invert=False,        help="Invert the contrast of CCD micrographs")
    group.add_option("",   fraction=0,          help="Number of dose fractionated images to average")
    
    
    if main_option:
        pgroup.add_option("-i", input_files=[], help="List of filenames for the input micrographs", required_file=True, gui=dict(filetype="file-list"))
        pgroup.add_option("-o", output="",      help="Output filename for the coordinate file with correct number of digits (e.g. sndc_0000.spi)", gui=dict(filetype="save"), required_file=True)
        group.add_option("",   limit=2000,      help="Limit on number of particles, 0 means give all", gui=dict(minimum=0, singleStep=1))
        group.add_option("",   noise=False,     help="Search out noise windows in the micrograph")
        # move next three options to benchmark
        
        bgroup = OptionGroup(parser, "Benchmarking", "Options to control benchmark particle selection",  id=__name__)
        bgroup.add_option("-g", good="",        help="Good particles for performance benchmark", gui=dict(filetype="open"), dependent=False)
        bgroup.add_option("",   good_coords="", help="Coordindates for the good particles for performance benchmark", gui=dict(filetype="open"), dependent=False)
        bgroup.add_option("",   good_output="", help="Output coordindates for the good particles for performance benchmark", gui=dict(filetype="open"), dependent=False)
        pgroup.add_option_group(bgroup)
        parser.change_default(log_level=3)
        parser.change_default(window=1.4)
    pgroup.add_option_group(group)

def check_options(options, main_option=False):
    #Check if the option values are valid
    
    from ..core.app.settings import OptionValueError
    if main_option:
        if options.good_coords != "" or options.template == "":
            if options.pixel_radius == 0: raise OptionValueError, "Pixel radius must be greater than zero"

def main():
    #Main entry point for this script
    run_hybrid_program(__name__,
        description = '''Find particles using template-matching
        
                        http://
                        
                        Example: Unprocessed film micrograph
                         
                        $ ara-lfcpick input-stack.spi -o coords.dat -r 110
                        
                        Example: Unprocessed CCD micrograph
                         
                        $ ara-lfcpick input-stack.spi -o coords.dat -r 110 --invert
                      ''',
        use_version = True,
        supports_OMP=True,
    )

def dependents(): return [spider_params]
if __name__ == "__main__": main()

