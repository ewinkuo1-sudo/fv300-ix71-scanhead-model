import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'FV5000_IX85_Model_25cm'/'.deps'))
import pymupdf
R=Path(__file__).resolve().parent/'references'
for name,ids in [('olympus_fv300_brochure.pdf',[1,2,15]),('olympus_ix71_ix81_brochure.pdf',[1,14])]:
    d=pymupdf.open(R/name)
    for i in ids:
        page=d[i]
        page.get_pixmap(matrix=pymupdf.Matrix(1.8,1.8),colorspace=pymupdf.csRGB).save(R/(Path(name).stem+'_page_'+str(i+1)+'.png'))
        if name.startswith('olympus_ix') and i==14:print(page.get_text())

