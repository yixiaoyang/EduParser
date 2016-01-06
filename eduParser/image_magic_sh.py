# coding=utf-8

import subprocess

### 放大
#% convert test.png -resize 800x80 test_800.png
### 黑白化
#% convert -monochrome  test_800.png test_black_white.png 


def image_resize(ifilename, ofilename):
	p = subprocess.Popen([ 'convert','-resize', '800x80', ifilename, ofilename],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	out, err = p.communicate()
	print out
	print err

def image_mono(ifilename, ofilename):
	p = subprocess.Popen([ 'convert','-monochrome', ifilename, ofilename],
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)
	out, err = p.communicate()
	print out
