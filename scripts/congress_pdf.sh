#!/bin/bash
mkdir $2_tmp
cd $2_tmp
# Usage: ./congress_pdf.sh <input pdf> <year> <results file> <totals file>
# lifted directly from http://bertanguven.com/faster-conversions-from-pdf-to-pngjpeg-imagemagick-vs-ghostscript
# also: https://github.com/ImageMagick/ImageMagick/issues/341
# to work around PDF errors, I settled on just tail'ing to get the last line of the page count output
pageNum=`gs -q -dNODISPLAY -c "(../$1) (r) file runpdfbegin pdfpagecount = quit" | tail -n 1`
gs -dNumRenderingThreads=4 -dNOPAUSE -sDEVICE=jpeg -dFirstPage=1 -dLastPage=$pageNum -sOutputFile=./page%d.jpg -dJPEGQ=100 -r600 -q ../$1 -c quit

for i in $( ls page*.jpg ); do
  # Trial and error + Stack Overflow seem to indicate that the best page segmentation mode is 4.
  # preserve_interword_spaces allows prevents the space between columns from getting squished together.
  tesseract $i $i -c preserve_interword_spaces=1 -psm 4
done
python ../congress_pdf.py page*.jpg.txt $2 ../$3 ../$4 --states ../states.txt
# cleanup
cd ..
rm -r $2_tmp
