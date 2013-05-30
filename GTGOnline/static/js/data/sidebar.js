
// Task Folders

function TaskFoldersViewModel() {
    // Data
    var self = this;
    self.folders = ['All', 'Active', 'Done', 'Dismissed'];
    self.chosenFolderId = ko.observable();
    self.tasks_list = ko.observableArray();
    self.tags_list = ko.observableArray();
    
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
