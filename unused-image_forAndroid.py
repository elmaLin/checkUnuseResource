
import os
import sys, getopt

from pathlib import Path
project_path = './'
is_remove = False
def search(path,keyword, exclude_path_name):
	content = os.listdir(path)
	results = []
	if path.endswith(exclude_path_name):
		return results
	for each in content:
		each_path = path+os.sep+each
		if os.path.isdir(each_path):
			results.extend(search(each_path,keyword,exclude_path_name))
		elif keyword in each:
			results.append(each_path)

	return results

def batch_search(path, exclude_path_name, keywords):
	results = []
	for keyword in keywords:
		results.extend(search(path, keyword, exclude_path_name))

	return results

def main():
	# try:
	# 	opts, args = getopt.getopt(argv)
	# except getopt.GetoptError:
	# 	print('test.py -p <inputpath> -r')
	# 	sys.exit(2)
	# for opt, arg in opts:
	# 	if opt in ("-p"):
	# 		project_path = arg
	# 	elif opt in ("-r"):
	# 		is_remove = True
	#
	# if project_path is None:
	# 	exit(-2)

	png_files = batch_search(project_path,  "build", ['.png', '.svga', '.gif', '.mp3', '.mp4'])
	check_files = batch_search(project_path, "build", ['.xib', '.storyboard', '.[mh]', '.pch', '.java', '.xml', '.m', '.mm', "plist", "swift", ".kt"])
	suffix1 = "@2x.png"
	suffix2 = ".9.png"
	suffix3 = ".png"
	suffix4 = "@3x.png"
	suffix5 = ".svga"
	suffix6 = ".gif"
	suffix7 = ".mp3"
	suffix8 = '.mp4'

	png_files_infos = {}
	for png_file in png_files:
		png_filename = os.path.basename(png_file)
		png_dir = os.path.dirname(png_file)
		if 'Pods' in png_dir:
			continue
		if png_dir.endswith('.imageset'):
			png_filename = os.path.split(png_dir)[-1].split(".")[0]
		png_filename = png_filename.replace(suffix1, '').replace(suffix2, '').replace(suffix3, '').replace(suffix4, '').replace(suffix5, '').replace(suffix6, '').replace(suffix7, '').replace(suffix8, '')

		if png_dir.endswith('bundle') or png_dir.endswith('appiconset') or png_dir.endswith('launchimage'):
			continue

		if png_filename in png_files_infos:
			png_files_infos[png_filename].append(png_file)
		else:
			png_files_infos[png_filename] = [png_file]

	refenced_png_names = []
	for check_file in check_files:
		with open(check_file, encoding="utf-8") as f:
			try:
				if '.mp4' in check_file:
					continue
				if '.mp3' in check_file:
					continue
				lines = f.readlines()
				for line in lines:
					for png_filename, png_file in png_files_infos.items():
						temp_name =  png_filename
						if temp_name in line:
							refenced_png_names.append(png_filename)
			except:
				print(check_file + ' read fail', sys.exc_info())
	# for png_filename, png_file in png_files_infos.items:
	# 	if png_filename in text:
	# 		refenced_png_names.append(png_filename)

	total_size = 0
	for png_filename, png_files in png_files_infos.items():
		if png_filename in refenced_png_names:
			continue
		for png_file in png_files:
			total_size += Path(png_file).stat().st_size
			if is_remove:
				os.remove(png_file)
			print(png_file)
	print('rescue total size:', total_size / 1024 / 1024, 'M')

if __name__ == "__main__":
    main()
