CodeMirror.defineMode("diff2", function() {
	var TAG_REGEX = /(@[\w\/\.\-\:]*\w)/;

	return {
		token: function(stream, state) {
		//console.log('stream - ' + stream.string);
			
			if (stream.match(TAG_REGEX)) {
				//console.log('match occured, string = "' + stream.match(TAG_REGEX) + '"');
				//stream.eatWhile(TAG_REGEX);
		        /*while ((ch = stream.next()) != null)
					if (ch == " ") {
						stream.backUp(1); break;
				}*/
		
				while ((ch = stream.next()) != null) {
					//if (!stream.match(TAG_REGEX)) {
						//console.log('match finished');
						stream.backUp(1);
						break;
					//}
					//console.log('matching ..."' + ch + '"');
				}
			    return "positive";
			}
			while (stream.next() != null && !stream.match(TAG_REGEX, false)) {}
			return null;
	    }
	};
	
});

CodeMirror.defineMIME("text/x-diff", "diff2");
