CodeMirror.defineMode("diff2", function() {
	var TAG_REGEX = /(@[\w\/\.\-\:]*\w)/;
	var match, workaround, decision;

	return {
		token: function(stream, state) {
		//console.log('stream - ' + stream.string);
			
			if ((match = stream.match(TAG_REGEX))) {
				//console.log('match occured, string = "' + stream.match(TAG_REGEX) + '"');
				//stream.eatWhile(TAG_REGEX);
		        /*while ((ch = stream.next()) != null)
					if (ch == " ") {
						stream.backUp(1); break;
				}*/
				//workaround = stream.string.indexOf(match[0]);
				//console.log('workaround = ' + workaround + ' char = "' + stream.string.charAt(workaround-1) + '"');
				//if ( workaround != -1 && stream.string.charAt(workaround-1) == ' ' )
				//{
					stream.string = stream.string.replace(match[0], match[0].toLowerCase());
					return "positive";
				//}
				/*while ((ch = stream.next()) != null) {
					//if (!stream.match(TAG_REGEX)) {
						//console.log('match finished');
						stream.backUp(1);
						break;
					//}
					//console.log('matching ..."' + ch + '"');
				}*/
				//workaround = stream.string.slice(-3);
				//console.log('match = "' + match + '" last char = "' + workaround + '"');
				//decision = workaround[1] == '@' && workaround[0] != ' ';
			}
			while (stream.next() != null && !stream.match(TAG_REGEX, false)) {}
			return null;
	    }
	};
	
});

CodeMirror.defineMIME("text/x-diff", "diff2");
