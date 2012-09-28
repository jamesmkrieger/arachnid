''' Data analysis functions

.. todo:: Finish documenting analysis

.. todo:: Finish one_class_classification

.. Created on Jul 19, 2012
.. codeauthor:: Robert Langlois <rl2528@columbia.edu>
'''
import numpy, scipy.special, scipy.linalg
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def pca(trn, tst=None, frac=-1):
    ''' Principal component analysis using SVD
    
    :Parameters:
        
    trn : numpy.ndarray
          Matrix to decompose with PCA
    tst : numpy.ndarray
          Matrix to project into lower dimensional space (if not specified, then `trn` is projected)
    frac : float
           Number of Eigen vectors: frac < 0: fraction of variance, frac >= 1: number of components, frac == 0, automatically assessed
    
    :Returns:
        
    val : numpy.ndarray
          Projected data
    idx : int
          Selected number of Eigen vectors
    V : numpy.ndarray
        Eigen vectors
    spec : float
           Explained variance
               
    .. note::
        
        Automatic Assessment is performed using an algorithm by `Thomas P. Minka:
        Automatic Choice of Dimensionality for PCA. NIPS 2000: 598-604`
        
        Code originally from:
        `https://raw.github.com/scikit-learn/scikit-learn/master/sklearn/decomposition/pca.py`
    '''
    
    mtrn = trn.mean(axis=0)
    trn = trn - mtrn
    if tst is None: tst = trn
    else: tst = tst - mtrn
    U, d, V = scipy.linalg.svd(trn, False)
    t = d**2/trn.shape[0]
    t /= t.sum()
    if frac >= 1:
        idx = int(frac)
    elif frac == 0.0:
        if 1 == 0:
            diff = numpy.abs(d[:len(d)-1]-d[1:])
            idx = diff.argmax()+1
        else:
            idx = _assess_dimension(t, trn.shape[0], trn.shape[1])+1
    elif frac > 0.0:
        idx = numpy.sum(t.cumsum()<frac)+1
    else: idx = d.shape[0]
    _logger.error("pca: %s -- %s"%(str(V.shape), str(idx)))
    if idx >= len(d): idx = 1
    val = d[:idx]*numpy.dot(V[:idx], tst.T).T
    _logger.error("pca2: %s -- %s"%(str(V.shape), str(tst.shape)))
    return val, idx, V[:idx], t[idx]

def _assess_dimension(spectrum, n_samples, n_features):
    '''Compute the likelihood of a rank ``rank`` dataset

    The dataset is assumed to be embedded in gaussian noise of shape(n,
    dimf) having spectrum ``spectrum``.

    :Parameters:
    
    spectrum : numpy.ndarray
              Data spectrum
    n_samples : int
               Number of samples
    dim : int
         Embedding/empirical dimension

    :Returns:
    
    ll : float,
        The log-likelihood

    .. note::
        
        This implements the method of `Thomas P. Minka:
        Automatic Choice of Dimensionality for PCA. NIPS 2000: 598-604`
        
        Code originally from:
        https://raw.github.com/scikit-learn/scikit-learn/master/sklearn/decomposition/pca.py
    
    '''
    
    max_ll = (0, 0)
    for rank in xrange(len(spectrum)):
        pu = -rank * numpy.log(2)
        for i in xrange(rank):
            pu += (scipy.special.gammaln((n_features - i) / 2) - numpy.log(numpy.pi) * (n_features - i) / 2)
    
        pl = numpy.sum(numpy.log(spectrum[:rank]))
        pl = -pl * n_samples / 2
    
        if rank == n_features:
            pv = 0
            v = 1
        else:
            v = numpy.sum(spectrum[rank:]) / (n_features - rank)
            pv = -numpy.log(v) * n_samples * (n_features - rank) / 2
    
        m = n_features * rank - rank * (rank + 1) / 2
        pp = numpy.log(2 * numpy.pi) * (m + rank + 1) / 2
    
        pa = 0
        spectrum_ = spectrum.copy()
        spectrum_[rank:n_features] = v
        for i in xrange(rank):
            for j in xrange(i + 1, len(spectrum)):
                pa += (numpy.log((spectrum[i] - spectrum[j]) * (1. / spectrum_[j] - 1. / spectrum_[i])) + numpy.log(n_samples))
    
        ll = pu + pl + pv + pp - pa / 2 - rank * numpy.log(n_samples) / 2
        if numpy.isfinite(ll) and ll > max_ll[0]: max_ll = (ll, rank)

    return max_ll[1]

def one_class_classification(data, nstd_min=3):
    ''' Classify a set of data into one-class and outliers
    
    :Parameters:
        
    data : numpy.ndarray
           Data to find center
    nstd_min : int
               Minimum number of standard deviations for outlier rejection

    :Returns:
    
    dist : numpy.ndarray
          Distance of each point in data from the center
    '''
    
    dist = one_class_distance(data, nstd_min)
    dsel = one_class_selection(dist, 4)
    #th = otsu(dist, len(dist)/16)
    #th = otsu(dist, numpy.sqrt(len(dist)))
    #dsel = dist < th
    return dsel

def one_class_distance(data, nstd_min=3):
    ''' Calculate the distance from the median center of the data
    
    :Parameters:
        
    data : numpy.ndarray
           Data to find center
    nstd_min : int
               Minimum number of standard deviations for outlier rejection

    :Returns:
    
    dist : numpy.ndarray
          Distance of each point in data from the center
    '''
    
    sel = one_class_selection(data, nstd_min)
    axis = 0 if data.ndim == 2 else None
    m = numpy.median(data[sel], axis=axis)
    axis = 1 if data.ndim == 2 else None
    assert(data.ndim==2)
    dist = numpy.sqrt(numpy.sum(numpy.square(data-m), axis=axis)).squeeze()
    assert(dist.ndim==1)
    return dist

def one_class_selection(data, nstd_min=3):
    ''' Select a set of non-outlier projections
    
    This code starts at 10 (max) standard deviations from the median
    and goes down to `nstd_min`, throwing out outliers and recalculating
    the median and standard deviation.
    
    :Parameters:
        
    data : numpy.ndarray
           Data to find non-outliers
    nstd_min : int
               Minimum number of standard deviations

    :Returns:

    selected : numpy.ndarray
               Boolen array of selected data
    '''
    
    assert(hasattr(data, 'ndim'))
    axis = 0 if data.ndim == 2 else None
    m = numpy.median(data, axis=axis)
    s = numpy.std(data, axis=axis)
    maxval = numpy.max(data, axis=axis)
    minval = numpy.min(data, axis=axis)
    
    sel = numpy.ones(len(data), dtype=numpy.bool)    
    start = int(min(10, max(numpy.max((maxval-m)/s),numpy.max((m-minval)/s))))
    for nstd in xrange(start, nstd_min-1, -1):
        m=numpy.median(data[sel], axis=axis)
        s = numpy.std(data[sel], axis=axis)
        hcut = m+s*nstd
        lcut = m-s*nstd
        
        if data.ndim > 1:
            tmp = data<hcut
            assert(tmp.shape[1]==data.shape[1])
            sel = numpy.logical_and(data[:, 0]<hcut[0], data[:, 0]>lcut[0])
            for i in xrange(1, data.shape[1]):
                sel = numpy.logical_and(sel, numpy.logical_and(data[:, i]<hcut[i], data[:, i]>lcut[i]))
        else:
            sel = numpy.logical_and(data<hcut, data>lcut)
        assert(numpy.sum(sel)>0)
    return sel

def threshold_max(data, threshold, max_num, reverse=False):
    ''' Ensure no more than `max_num` data points are selected by
    the given threshold.
    
    :Parameters:
    
    data : array
           Array of values to select
    threshold : float
                Values greater than thresold are selected
    max_num : int
              Only the `max_num` highest are selected
    reverse : bool
              Reverse the order of selection
    
    :Returns:
    
    threshold : float
                New threshold to use
    '''
    
    idx = numpy.argsort(data)
    if not reverse: idx = idx[::-1]
    threshold = numpy.searchsorted(data[idx], threshold)
    if threshold > max_num: threshold = max_num
    return data[idx[threshold]]

def threshold_from_total(data, total, reverse=False):
    ''' Find the threshold given the total number of elements kept.
    
    :Parameters:
    
    data : array
           Array of values to select
    total : int or float
            Number of elements to keep (if float and less than 1.0, then fraction)
    reverse : bool
              Reverse the order of selection
    
    :Returns:
    
    threshold : float
                New threshold to use
    '''
    
    if total < 1.0: total = int(total*data.shape[0])
    idx = numpy.argsort(data)
    if not reverse: idx = idx[::-1]
    return data[idx[total]]

def otsu(data, bins=0):
    ''' Otsu's threshold selection algorithm
    
    :Parameters:
        
    data : numpy.ndarray
           Data to find threshold
    bins : int
           Number of bins [if 0, use sqrt(len(data))]
    
    :Returns:
    
    th : float
         Optimal threshold to divide classes
    
    .. note::
        
        Code originally from:
            https://svn.broadinstitute.org/CellProfiler/trunk/CellProfiler/cellprofiler/cpmath/otsu.py
    '''
        
    data = numpy.array(data).flatten()
    if bins <= 0: bins = int(numpy.sqrt(len(data)))
    if bins > len(data): bins = len(data)
    data.sort()
    var = running_variance(data)
    rvar = numpy.flipud(running_variance(numpy.flipud(data)))
    
    rng = len(data)/bins
    thresholds = data[1:len(data):rng]
    if 1 == 1:
        idx = numpy.arange(0,len(data)-1,rng, dtype=numpy.int)
        score_low = (var[idx] * idx)
        idx = numpy.arange(1,len(data),rng, dtype=numpy.int)
        score_high = (rvar[idx] * (len(data) - idx))
    else:
        score_low = (var[0:len(data)-1:rng] * numpy.arange(0,len(data)-1,rng))
        score_high = (rvar[1:len(data):rng] * (len(data) - numpy.arange(1,len(data),rng)))
    scores = score_low + score_high
    if len(scores) == 0: return thresholds[0]
    index = numpy.argwhere(scores == scores.min()).flatten()
    if len(index)==0: return thresholds[0]
    index = index[0]
    if index == 0: index_low = 0
    else: index_low = index-1
    if index == len(thresholds)-1: index_high = len(thresholds)-1
    else: index_high = index+1
    return (thresholds[index_low]+thresholds[index_high]) / 2

def running_variance(x):
    '''Given a vector x, compute the variance for x[0:i]
    
    :Parameters:
        
    x : numpy.ndarray
        Sorted data
    
    :Returns:
        
    var : numpy.ndarray
          Running variance
    
    .. note::
        
        Code originally from:
            https://svn.broadinstitute.org/CellProfiler/trunk/CellProfiler/cellprofiler/cpmath/otsu.py
    
        http://www.johndcook.com/standard_deviation.html
            S[i] = S[i-1]+(x[i]-mean[i-1])*(x[i]-mean[i])
            var(i) = S[i] / (i-1)
    '''
    n = len(x)
    # The mean of x[0:i]
    m = x.cumsum() / numpy.arange(1,n+1)
    # x[i]-mean[i-1] for i=1...
    x_minus_mprev = x[1:]-m[:-1]
    # x[i]-mean[i] for i=1...
    x_minus_m = x[1:]-m[1:]
    # s for i=1...
    s = (x_minus_mprev*x_minus_m).cumsum()
    var = s / numpy.arange(2,n+1)
    # Prepend Inf so we have a variance for x[0]
    return numpy.hstack(([0],var))

