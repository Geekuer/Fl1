class Template:
	# template
	def html(title, list, body, control):
		return f'''
			<!DOCTYPE html>
			<html lang="en">
				<head>
					<meta charset="UTF-8">
					<meta name="viewport" content="width=device-width, initial-scale=1.0">
					<title>{title}</title>
				</head>
				<body>
					<h1><a href="/">WEB</a></h1>
					<ul>
						{list}
					</ul>
					{control}
					{body}
				</body>
			</html>
		'''

	# list
	def list(filelist):
		list = ''
		for file in filelist:
			list += f'<li><a href="/page/{file}/">{file}</a></li>'
		
		return list