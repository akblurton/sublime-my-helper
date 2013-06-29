# MyHelper - Sublime Text 3 Plugin

The MyHelper plugin helps programmers get to the documentation they use the most, **quickly**.

## Usage

Using MyHelper is simple, select the code/line you want to look up and press `Ctrl+F1` (or `Cmd+F1` on Mac). Doing so will launch a new tab in your default browser, searching for what you just selected. Based on your settings file for MyHelper, you can define different search URLs for specific languages

## The Settings File

The default settings file for MyHelper looks like this:

	{
		"help_all" : "https://google.com/search?q=",
		"help_python" : "{all}python+",
		"help_java" : "http://search.oracle.com/search/search?search_p_main_operator=all&group=Documentation&q=$$+url:/javase&searchField=Timer&docsets=",
		"help_php" : "http://php.net/$$",
		"help_less" : "css",
		"help_js" : "https://developer.mozilla.org/en-US/search?q=$$+javascript",
		"help_css" : "https://developer.mozilla.org/en-US/search?q=$$+css",
		"help_html" : "https://developer.mozilla.org/en-US/search?q=$$+html",
		"help_plain": "http://answers.com/$$"
	}  

The `help_all` url is used when a url is not found for the current language

To define a search URL for a language, create a key in your settings file prefixed with "help_" and then the name of the language (the name as interpreted by Sublime Text that is). By default whatever you have selected is appended to the end of the url. To specify where the search query is placed, use $$.

You may also easily duplicate or include the search URLs of other languages. To simply copy the URL (useful for languages such as LESS/SASS which generally will need CSS documentation), just give the language name to copy rather than a search URL. If you want to include the URL of another language (but make further changes to it) use the language name surrounded in braces (i.e. `{css}`).