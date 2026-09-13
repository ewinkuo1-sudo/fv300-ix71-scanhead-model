import sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parents[1]/'FV5000_IX85_Model_25cm'/'.deps'))
import pymupdf
tasks=[('olympus_fv300_brochure.pdf',1,(.375,.54,1,.95),'fv300_ix71_catalog_configuration.png'),
       ('olympus_ix71_ix81_brochure.pdf',14,(.52,.028,.747,.258),'ix71_catalog_dimensions.png')]
for fn,i,rect,out in tasks:
    d=pymupdf.open(R/'references'/fn);p=d[i];w,h=p.rect.width,p.rect.height
    p.get_pixmap(matrix=pymupdf.Matrix(3,3),clip=pymupdf.Rect(rect[0]*w,rect[1]*h,rect[2]*w,rect[3]*h),colorspace=pymupdf.csRGB).save(R/'references'/out)

