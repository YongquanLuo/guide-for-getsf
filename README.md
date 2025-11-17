# guide-for-getsf
*getsf*, a new method for extracting sources and filaments in astronomical images, read more about it at https://irfu.cea.fr/Pisp/alexander.menshchikov/

This repository provide some python scripts to standardize the .fits file before you run getsf.

## description
<ins> getsf/modfits.py</ins> can be used to standardize the header and data of fits file so that it is suitable for running getsf.

<ins> getsf/make_mask.py</ins> can help you generate the corresponding .omask.fits file.

<ins> +getsf.cfg</ins> is config file used for running getsf.
