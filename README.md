# k-meanz
k-means clustering of image data, pixel by pixel.

Implemented in various combinations of:
* PIL
* numpy
* Google's [Tensorflow] (https://github.com/tensorflow/tensorflow)

# Usage

Clustering with Tensorflow...

```>python k_means_tf.py <path/to/input> [-k K] [-r ROUNDS] [-o OUTDIR] [-s SCALE] [-g GENERATE_ALL]```

Clustering with numpy...

```>python k_means_np_vanilla.py <path/to/input> [-k K] [-r ROUNDS] [-o OUTDIR] [-s SCALE] [-g GENERATE_ALL]```

positional arguments:
* path to input image jp(e)g

optional arguments:
* -h, --help    help message
* -k, --k   number of centroids (default: 50)
* -r, --rounds    number of rounds of clustering (default: 5)
* -o, --outdir    path/to/output/directory (default: working dir)
* -s, --scale   scale pixel location to be equitable with RGB vals? [True/False] (default: T)
* -g, --generate_all    generate image after each round? (slower) [True/False] (default: F)

# e.g.

```>python k_means_tf.py ~/Downloads/erykah_badu.jpg -k10 -r5```
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/102397924@N07/24178107450/in/dateposted-public/" title="536211-78101_160103_0516_k10_0"><img src="https://farm2.staticflickr.com/1614/24178107450_60f51bb83b_b.jpg" width="960" height="960" alt="536211-78101_160103_0516_k10_0"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

```>python k_means_tf.py ~/Downloads/erykah_badu.jpg -k10 -r5 -s False```
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/102397924@N07/24178583830/in/dateposted-public/" title="536211-78101_160119_0002_k10_4"><img src="https://farm2.staticflickr.com/1651/24178583830_c598f41e8a_b.jpg" width="960" height="960" alt="536211-78101_160119_0002_k10_4"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

```>python k_means_tf.py ~/Downloads/erykah_badu.jpg -k50 -r5 -s False```
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/102397924@N07/24474140105/in/dateposted-public/" title="536211-78101_160118_1728_k50_4"><img src="https://farm2.staticflickr.com/1636/24474140105_bcce40ca4c_b.jpg" width="960" height="960" alt="536211-78101_160118_1728_k50_4"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>

```>python k_means_tf.py ~/Downloads/erykah_badu.jpg -k1000 -r3```
<a data-flickr-embed="true"  href="https://www.flickr.com/photos/102397924@N07/24473648725/in/dateposted-public/" title="536211-78101_kmeanz_3_k1000"><img src="https://farm2.staticflickr.com/1651/24473648725_a449105fcc_b.jpg" width="960" height="960" alt="536211-78101_kmeanz_3_k1000"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>


# "Go on..."

k-means clustering is a method for data mining with no prior knowledge of data distribution but explicit number of classifications ("clusters"). In each round, pixels are partitioned by minimizing distance to the most similar cluster, based on Euclidean distance along 5 dimensions: location (x,y) and color (R,G,B). Centroid values are then updated by re-computing cluster averages. In order to generate clustered ("segmented") images, each pixel color value is determined by its centroid (mean cluster value).

N.B. k_means_tf.py is the most efficient, but memory-intensive!
