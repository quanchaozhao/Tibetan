#_*_cording:utf-8_*_
import os
import sys
import codecs

#批量编码格式转换utf-8-BOM
# 注意windows下编辑的文件需要转换，linux下编辑的不需要转换

#编码转换函数
def convert(input_dir,file,output_dir,out_enc="UTF-8-sig"):
	try:
		input_file = os.path.join(input_dir,file)
		print ("convert " + input_file)
		f=codecs.open(input_file,'r','gb2312')
		new_content=f.read()
		codecs.open(os.path.join(output_dir,os.path.splitext(file)[0])+'.xml','w+',out_enc).write(new_content)
		f.close()
		#os.remove(file)
	except UnicodeDecodeError as err:
		input_file = os.path.join(input_dir,file)
		print ("convert " + input_file)
		f=codecs.open(input_file,'r','utf-8')
		new_content=f.read()
		os.path.join(output_dir,file)
		codecs.open(os.path.join(output_dir,os.path.splitext(file)[0])+'.xml','w+',out_enc).write(new_content)
		f.close()
	except IOError as err:
		print ("I/O error: {0}".format(err))

#文件夹处理函数
def explore(dir,out_dir):
	for root,dirs,files in os.walk(dir):
		for file in files:
			# path=os.path.join(root,file)
			convert(root,file,out_dir)
#主函数
def main():
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	for path in sys.argv[1:]:
		if(os.path.isfile(path)):
			convert(".",path,out_dir)
		elif os.path.isdir(path):
			explore(path,out_dir)

if __name__=="__main__":
	out_dir="_out"
	main()