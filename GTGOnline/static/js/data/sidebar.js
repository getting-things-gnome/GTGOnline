
// Task Folders

function TaskFoldersViewModel() {
    // Data
    var self = this;
    self.folders = ['All', 'Active', 'Done', 'Dismissed'];
    self.chosenFolderId = ko.observable();
    self.tasks_list = ko.observableArray();
    self.tags_list = ko.observableArray();
    self.modified_tasks = ko.observableArray();
    self.modify_selected = ko.observableArray();
    
    // Behaviours
    self.goToFolder = function(folder) {
        location.hash = folder;
    };
    
    $.get('/tags/all', self.tags_list);
    
    // Client-side routes
    Sammy(function() {
        this.get('#:folder', function() {
            self.chosenFolderId(this.params.folder);
            $.get('/tasks/get', { folder: this.params.folder }, self.tasks_list);
        });
        
        this.get('', function() {
            this.app.runRoute('get', '#Active')
        });
    }).run();
    
    self.add_subtask = function(data) {
        return;
    };
    
    self.mark_done = function () {
        //alert(self.modify_selected());
        var new_status = 1;
        $.get('/tasks/modify/status', { task_id:self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, self.tasks_list);
        alert(self.modify_selected());
    }
    
    self.change_status = function (id, new_status, index) {
        //alert(new_status);
        $.get('/tasks/modify/status', { task_id:id, status: new_status, folder: self.chosenFolderId() }, self.tasks_list);
        //self.tasks_list.Elements.replace(self.tasks_list()[index], self.modified_tasks);
    };
    
    self.delete_task = function(id, index) {
        //alert(id);
        $.get('/tasks/delete/', { task_id:id, folder: self.chosenFolderId() }, self.tasks_list);
    };
};

//ko.applyBindings(new TaskFoldersViewModel(), document.getElementById("task_folders"));
//ko.applyBindings(new TaskFoldersViewModel(), document.getElementById("task_rows_container"));

function get_todays_date() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1;
    
    var yy = (today.getFullYear() + '').substring(2, 4);
    if(dd<10){dd='0'+dd} if(mm<10){mm='0'+mm} today = dd + '/' + mm + '/' + yy;
    //alert(today);
    return today;
}

function check_date_eq_today(date_str) {
    // date_str is in the form - 24/05/13
    var today = new Date();
    day = date_str.substring(0, 2)
}
