
from astropy.io import fits
from astropy.wcs import WCS
from regions import Regions
import numpy as np

# 1) 读入基准图像（掩膜要与它同一头/同一shape）
hdu = fits.open('D:\Working Area 2\\code\MyWork\G332.296-0.094\\getsf\\pre_getsf\\alma_1300.fits')
hdr = hdu[0].header
shape = hdu[0].data.shape  # (ny, nx)
wcs = WCS(hdr)
hdu.close()

# 2) 读取 ds9 .reg，转为像素坐标区域
regs = Regions.read('D:\Working Area 2\\code\\MyWork\G332.296-0.094\\getsf\\mask.reg', format='ds9')
pix_regs = [r.to_pixel(wcs) for r in regs]

# 3) 栅格化：把所有区域并集变成布尔掩膜（True=有效区域）
mask = np.zeros(shape, dtype=bool)
for r in pix_regs:
    # 对大多数封闭区域（ellipse/polygon/circle）用 to_mask().to_image()
    m = r.to_mask(mode='center').to_image(shape)
    mask |= (m > 0)

# 4) 写成 0/1 掩膜（uint8），头信息直接用原图的
hdu_mask = fits.PrimaryHDU(mask.astype('uint8'), header=hdr)
hdu_mask.writeto('D:\Working Area 2\\code\\MyWork\G332.296-0.094\\getsf\\mask.fits', overwrite=True)