from flask import Flask, request, redirect
from lib.template import Template
import os

app = Flask(__name__)

# app ↓

# home
@app.route('/')
def home():
	title = 'Welcome'
	description = 'Hello World'
	lists = Template.list(os.listdir('./data'))

	return Template.html(
		title,
		lists,
		f'<h2>{title}</h2><p>{description}</P>',
		f'<a href="/create/">Create</a>'
	)

# page
@app.route('/page/<title>/')
def page(title):
	with open(f'./data/{title}', 'r', encoding="utf-8") as file:
		description = file.read()
	
	lists = Template.list(os.listdir('./data'))

	return Template.html(
		title,
		lists,
		f'<h2>{title}</h2><p>{description}</P>',
		f'''<a href="/create/">Create</a> <a href="/update/{title}">Update</a>
			<form action="/delete/{title}/" method="post" onsubmit="return confirm(\'Do you really want to delete it?\')">
				<input type="submit" value="Delete">
			</form>
		'''
	)
	
# create
@app.route('/create/', methods=['GET', 'POST'])
def create():
	if request.method == 'GET':
		title = 'Create'

		lists = Template.list(os.listdir('./data'))

		create = f'''
			<h2>{title}</h2>
			<form action="/create/" method="post">
				<p><input type="text" name="title" placeholder="title"></p>
				<p><textarea name="description" placeholder="description"></textarea></p>
				<p><input type="submit" value="Create"></p>
			</form>
		'''

		return Template.html(
			title,
			lists,
			create,
			''
		)
	
	elif request.method == 'POST':
		title = request.form['title']
		description= request.form['description']

		with open(f'./data/{title}', 'w', encoding="utf-8") as file:
			file.write(description)
		print(f'Created: {title}')

		return redirect(f'/page/{title}/')
	
# update
@app.route('/update/<title>/', methods=['GET', 'POST'])
def update(title):
	if request.method == 'GET':
		with open(f'./data/{title}', 'r', encoding="utf-8") as file:
			description = file.read()

		lists = Template.list(os.listdir('./data'))
	
		create = f'''
			<h2>Update {title}</h2>
			<form action="/update/{id}/" method="post">
				<input type="hidden" name="old_title" value="{title}">
				<p><input type="text" name="title" placeholder="title" value="{title}"></p>
				<p><textarea name="description" placeholder="description"">{description}</textarea></p>
				<p><input type="submit" value="Update"></p>
			</form>
		'''

		return Template.html(
			f'Update {title}',
			lists,
			create,
			''
		)
	
	elif request.method == 'POST':
		old_title = request.form['old_title']
		title = request.form['title']
		description= request.form['description']

		with open(f'./data/{old_title}', 'w', encoding="utf-8") as file:
			file.write(description)

		os.rename(f'./data/{old_title}', f'./data/{title}')
		print(f'Updated: {old_title} -> {title}')

		return redirect(f'/page/{title}/')

# delete
@app.route('/delete/<title>/', methods=['POST'])
def delete(title):
	os.remove(f'./data/{title}')
	print(f'Deleted: {title}')

	return redirect('/')

app.run(port = 4000, debug=True)