var tag_array;

function get_tags_by_user() {
    var xmlHttp = new XMLHttpRequest();
	
    try {
		xmlHttp.open("GET", "/tags/all/", true);
		xmlHttp.onreadystatechange = function ()
        {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            {
                var obj = JSON.parse(xmlHttp.responseText);
                //var arr = ko.observableArray([]);
                tag_array = ko.mapping.fromJS(obj);
                alert(tag_array()[0].name());
                ko.applyBindings(tag_array(), document.getElementById('sidebar_tags_list'));
            }
        }
        xmlHttp.send(null);
	} catch(e) {
        alert("can't connect to server" + e.toString());
    }
}
