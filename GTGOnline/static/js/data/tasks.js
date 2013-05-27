function hello_world() {
    alert("The World is Yours");
};

function show_tasks(task_tree) {
    
    /*for (var i=0; i<task_tree.length; i++) {
        alert("id = " + task_tree[i].id + " name = " + task_tree[i].name);
    }*/
    var main = document.getElementById('task_row');
    var row = main;
    var children = row.childNodes;
    var subtasks_count = 0;
    var main_div = document.getElementById("main_div");
    
    var children2 = children[5].childNodes; 
    /*for (var i=0; i<children2.length; i++) {
        alert(i + " " + children2[i].textContent);
    }*/
    
    /*for (var i=0; i<task_tree.length; i++) {
        row = main.cloneNode(true);
        children = row.childNodes;
        subtasks_count = task_tree[i].subtasks.length;
        if (subtasks_count > 0) {
            children[3].childNodes[1].textContent = "+" + subtasks_count;
        }
        children[5].childNodes[1].textContent = task_tree[i].name;
        row.style.display = "block";
        main_div.appendChild(row);
    }*/
    //clone.id = "1";
    //clone.style.display = "block";
    //clone.style.marginLeft = "40px"
    //document.getElementById("main_div").appendChild(clone);
    
    
}

var task_array;

function get_tasks_ajax() {
    var xmlHttp = new XMLHttpRequest();
	
    try {
		xmlHttp.open("GET", "/tasks/json_dumps/", true);
		xmlHttp.onreadystatechange = function ()
        {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            {
                var obj = JSON.parse(xmlHttp.responseText);
                //var arr = ko.observableArray([]);
                task_array = ko.mapping.fromJS(obj);
                //alert(task_array()[1].tags()[0].color());
                ko.applyBindings(task_array(), document.getElementById('task_rows_container'));
            }
        }
        xmlHttp.send(null);
	} catch(e) {
        alert("can't connect to server" + e.toString());
    }
}

function viewModel() {
    var self = this;
    self.subtask_count = ko.observable('+2');
    self.name = ko.observable("Summer's here: Lets clean the house!");
    self.description = ko.observable("It's that time of the year again ...");
    self.due_date = ko.observable("13.09.12");
    self.start_date = ko.observable("2 days ago");
}
