// CONSTANTS
var NAME_MAX_LENGTH = 30
var DESCRIPTION_MAX_LENGTH = 40

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
            $.get('/tasks/get', { folder: this.params.folder }, function(data) {
                self.tasks_list(data);
                $('strong.task_name').popover({
                    placement: 'top'
                });
                $('span.task_description').popover({
                    placement: 'top'
                });
            });
        });
        
        this.get('', function() {
            this.app.runRoute('get', '#Active')
        });
    }).run();
    
    self.new_task = function(id) {
        $('#new_task_modal').modal('show');
        $.get('/tasks/new', {
            
        }, self.tasks_list);
    };
    
    self.mark_done = function (new_status) {
        //alert(self.modify_selected());
        $.get('/tasks/modify/status', { task_id:self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, self.tasks_list);
        //alert(self.modify_selected());
    }
    
    self.change_status = function (id, new_status, index) {
        $.get('/tasks/modify/status', { task_id:id, task_id_list: self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, self.tasks_list);
        //self.tasks_list.Elements.replace(self.tasks_list()[index], self.modified_tasks);
    };
    
    self.delete_task = function(id, index) {
        //alert(id);
        $.get('/tasks/delete/', { task_id:id, task_id_list: self.modify_selected(), folder: self.chosenFolderId() }, self.tasks_list);
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

function name_is_short(task_name) {
	return task_name.length < NAME_MAX_LENGTH
}

function shortify_name(task_name) {
    //return task_name.substring(0, NAME_MAX_LENGTH-3) + "<span style='color: #FF0000'>" + task_name.charAt(NAME_MAX_LENGTH-3) + "</span><span style='color: #EE0000'>" + task_name.charAt(NAME_MAX_LENGTH-2) + "</span><span style='color: #DD0000'>" + task_name.charAt(NAME_MAX_LENGTH-1) + "</span>"
    return task_name.substring(0, NAME_MAX_LENGTH-3) + '...'
}

function description_is_short(task_description) {
	return task_description.length < DESCRIPTION_MAX_LENGTH
}

function shortify_description(task_description) {
    //return task_name.substring(0, NAME_MAX_LENGTH-3) + "<span style='color: #FF0000'>" + task_name.charAt(NAME_MAX_LENGTH-3) + "</span><span style='color: #EE0000'>" + task_name.charAt(NAME_MAX_LENGTH-2) + "</span><span style='color: #DD0000'>" + task_name.charAt(NAME_MAX_LENGTH-1) + "</span>"
    return task_description.substring(0, DESCRIPTION_MAX_LENGTH-3) + '...'
}

function get_popover_placement(pop, dom_el) {
    var height = window.innerHeight;
    console.log('height' + height);
    if (height<500) return 'bottom';
    var left_pos = $(dom_el).offset().left;
    console.log('left_pos' + left_pos);
    if (height - left_pos > 400) return 'right';
    return 'left';
}
