import sublime, sublime_plugin, urllib.parse, re, webbrowser

class HelpMeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Get all selections in the current view
		selections = self.view.sel()
		# We are going to store all selections into a URL encoded string, 
		# but first put them in an array
		str_selections = []

		# Stores the scope syntax that we're searching for
		scope = ''
		# Scope regular expression
		scope_regex = re.compile(r'source\.(\w+)')

		for select in selections:
			# If the selection is empty, select the whole line
			if select.empty():
				select = self.view.line(select)

			# Find the scope of the current selection
			selection_scope = '';
			view_scope = self.view.scope_name(select.begin())
			matches = re.match(scope_regex, view_scope)
			if matches:
				selection_scope = matches.group(1)
			else:
				selection_scope = 'None'

			if not scope:
				# If we haven't defined the scope for the current search do it now
				scope = selection_scope
			elif scope != selection_scope:
				# If the scope was defined, ignore any selections that don't match the first selection
				continue


			# Get the current text selection, convert tabs and line breaks to spaces
			text = self.view.substr(select).strip()

			# If the line is empty, skip it
			if not text:
				continue

			text = re.sub(r'\s+', ' ', text)
			# and then url quote it
			text = urllib.parse.quote(text, '')
			# convert the ugly %20 into +
			text = text.replace('%20', '+')
			str_selections.append(text)

		# Combine all our selections into a big query
		search_query = "+".join(str_selections)
		# Remove any double + signs
		search_query = re.sub(r'\+{2,}', '+', search_query)

		# No need to keep on going if nothing was selected
		if not len(str_selections):
			return

		# Load our settings file now
		settings = sublime.load_settings('MyHelper.sublime-settings')
		search_engine = settings.get('search_engine', 'https://google.com/search?q=')
		
		# Find any defined parsers
		parsers = settings.get('parsers', [])
		use_parser = False
		if len(parsers) and isinstance(parsers, dict):
			url = self.find_parser(parsers, scope)

		##Use our search engine instead
		if not url:
			url = search_engine

		# Add our search engine query if $SEARCH$ is found
		url = url.replace('$SEARCH$', search_engine)

		# Make sure we have a protocol infront of our URL, and default to http if not
		if not re.match(r'[A-Za-z]+:\/\/', url):
			url = 'http://' + url

		# Add our search query
		url = url.replace('$$', search_query) if '$$' in url else url + search_query
		# Finally - open our search query
		webbrowser.open_new_tab(url);
		



	# Method to recursively find a parser for the given syntax
	def find_parser(self, parsers, syntax, checked = []):
		if(syntax not in parsers):
			return False

		# Keep track of what we've checked already to prevent any infinite recursion
		checked.append(syntax)
		# Get the parser from our settings
		p = parsers.get(syntax)
		# Check if the result is actually a reference to another syntax's parser
		if p in parsers:
			# If we've already been to the syntax this parser points to,
			# we'll head in a circual direction: exit now
			if p in checked:
				return False
			return self.find_parser(parsers, p, checked)

		return p



