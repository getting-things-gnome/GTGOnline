// CONSTANTS
var NAME_MAX_LENGTH = 30
var DESCRIPTION_MAX_LENGTH = 40
var TAG_REGEX = /(?:^|[\s])(@[\w\/\.\-\:]*\w)/g;

// GLOBAL VARIABLES
var parentId = -1

// Task Folders

function TaskFoldersViewModel() {
    // Data
    var self = this;
    self.folders = ['All', 'Active', 'Done', 'Dismissed'];
    self.chosenFolderId = ko.observable();
    self.tasks_list = ko.observableArray();
    self.tasks_list_length = ko.observable('0');
    
    self.tags_list = ko.observableArray();
    self.modified_tasks = ko.observableArray();
    self.modify_selected = ko.observableArray();
    
    self.task_name_field = ko.observable('');
    self.task_description_field = ko.observable('');
    self.task_start_date_field = ko.observable('');
    self.task_due_date_field = ko.observable('');
    
    self.all_tags = ko.observableArray();
    
    self.tasks_list.subscribe(function (newValue) {
        self.tasks_list_length(newValue.length);
    }, self);
    
    self.task_name_field.subscribe(function (newValue) {
        self.all_tags((newValue + " " + self.task_description_field()).match(TAG_REGEX));
    }, self);
    
    self.task_description_field.subscribe(function (newValue) {
        self.all_tags((self.task_name_field() + " " + newValue).match(TAG_REGEX));
    }, self);
    
    self.modify_selected.subscribe(function (newValue) {
        if (self.modify_selected().length > 0) {
            $("#dropdown").show();
            $("#header").hide();
        }
        else {
            $("#dropdown").hide();
            $("#header").show();
        }
    });
    
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
                    placement: 'top',
                    trigger: 'hover',
                });
                $('span.task_description').popover({
                    placement: 'top',
                    trigger: 'hover',
                });
                /*$('.show_dropdown').click(function() {
                    if( $(this).is(':checked')) {
                        $("#dropdown").show();
                        $("#header").hide();
                    } else {
                        $("#dropdown").hide();
                        $("#header").show();
                    }
                });*/
            });
        });
        
        
        this.get('', function() {
            this.app.runRoute('get', '#Active')
        });
    }).run();
    
    self.show_new_task_modal = function() {
        /*var match = ko.utils.arrayFirst(self.tasks_list(), function(item) {
           return 28 === item.id;
        });
        
        if (!match) {
            alert('no match found');
        }
        else {
            var old_id =  match.id
            self.tasks_list.replace(match, {
                id: old_id,
                name: 'hey',
                description: 'none',
                indent: 0,
                subtasks: [],
                tags: [],
                start_date: '23/05/13',
                due_date: '6/06/13',
            });
            alert(match.name);
        }*/
        
        $('#new_task_modal').modal('show');
        setParentId(-1);
    }
    
    self.show_new_subtask_modal = function(parent_id) {
        self.task_name_field('');
        self.task_description_field('');
        self.task_start_date_field('');
        self.task_due_date_field('');
        setParentId(parent_id);
        $('#new_task_modal').modal('show');
    }
    
    self.new_task = function() {
        if (self.task_name_field() == '') {
            alert("Task name cannot be empty");
            return
        }
        $('#new_task_modal').modal('hide');
        $.get('/tasks/new', {
            name: self.task_name_field(),
            description: self.task_description_field(),
            start_date: self.task_start_date_field(),
            due_date: self.task_due_date_field(),
            folder: self.chosenFolderId(),
            parent_id: getParentID(),
        }, function(data) {
            
            if (getParentID() != -1) {
                var match = ko.utils.arrayFirst(self.tasks_list(), function(item) {
                    //alert(data[0].id);
                    return data[0].id === item.id;
                });
                if (match) {
                    //alert(match.name);
                    self.tasks_list.replace(match, data[0]);
                    //alert(match.name);
                }
                else {
                    alert("no match found");
                }
            }
            self.tasks_list(data);
            $.get('/tags/all', self.tags_list);
            setParentId(-1);
            self.task_name_field('');
            self.task_description_field('');
            self.task_start_date_field('');
            self.task_due_date_field('');
            $('strong.task_name').popover({
                    placement: 'top',
                    trigger: 'hover',
            });
            $('span.task_description').popover({
                placement: 'top',
                trigger: 'hover',
            });
        });
    };
    
    self.update_task = function() {
        if (self.task_name_field() == '') {
            alert("Task name cannot be empty");
            return
        }
        $('#edit_task_modal').modal('hide');
        $.get('/tasks/update', {
            name: self.task_name_field(),
            description: self.task_description_field(),
            start_date: self.task_start_date_field(),
            due_date: self.task_due_date_field(),
            folder: self.chosenFolderId(),
            task_id: getParentID(),
        }, function(data) {
            //self.tasks_list(data);
            var match = ko.utils.arrayFirst(self.tasks_list(), function(item) {
                //alert(data[0].id);
                return data[0].id === item.id;
            });
            if (match) {
                //alert(match.name);
                self.tasks_list.replace(match, data[0]);
                //alert(match.name);
            }
            else {
                alert("no match found");
            }
            $.get('/tags/all', self.tags_list);
            setParentId(-1);
            $('strong.task_name').popover({
                    placement: 'top',
                    trigger: 'hover',
            });
            $('span.task_description').popover({
                placement: 'top',
                trigger: 'hover',
            });
        });
    };
    
    self.show_edit_task_modal = function(id, name, description, start_date, due_date) {
        self.task_name_field(name);
        self.task_description_field(description);
        self.task_start_date_field(start_date);
        self.task_due_date_field(due_date);
        setParentId(id);
        $('#edit_task_modal').modal('show');
    }
    
    self.reset_start_date_field = function() {
        self.task_start_date_field('')
    }
    
    self.reset_due_date_field = function() {
        self.task_due_date_field('')
    }
    
    self.mark_done = function (new_status) {
        //alert(self.modify_selected());
        $.get('/tasks/modify/status', { task_id:self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            $('strong.task_name').popover({
                    placement: 'top',
                    trigger: 'hover',
            });
            $('span.task_description').popover({
                placement: 'top',
                trigger: 'hover',
            });
        });
        //alert(self.modify_selected());
    }
    
    self.change_status = function (id, new_status, index) {
        $.get('/tasks/modify/status', { task_id:id, task_id_list: self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            $('strong.task_name').popover({
                placement: 'top',
                trigger: 'hover',
            });
            $('span.task_description').popover({
                placement: 'top',
                trigger: 'hover',
            });
            self.modify_selected([]);
        });
        //self.tasks_list.Elements.replace(self.tasks_list()[index], self.modified_tasks);
    };
    
    self.delete_task = function(id, index) {
        //alert(id);
        $.get('/tasks/delete/', { task_id:id, task_id_list: self.modify_selected(), folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            $('strong.task_name').popover({
                    placement: 'top',
                    trigger: 'hover',
            });
            $('span.task_description').popover({
                placement: 'top',
                trigger: 'hover',
            });
            $.get('/tags/all', self.tags_list);
        });
    };
    
    self.get_tasks_by_tag = function(id) {
        $.get('/tags/get_tasks', { tag_id:id, folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            $('strong.task_name').popover({
                    placement: 'top',
                    trigger: 'hover',
            });
            $('span.task_description').popover({
                placement: 'top',
                trigger: 'hover',
            });
        });
    }
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

function find_tags(text) {
    alert(text);
}

function get_formatted_date(date_str) {
    var chunks = date_str.split('/');
    var formatted_date = chunks[1] + '-' + chunks[0] + '-' + chunks[2];
    return formatted_date
}

function get_date_object(date_str) {
    if (date_str == '') {
        return null
    }
    var formatted_date = get_formatted_date(date_str)
    var date_object = new Date(formatted_date);
    //alert(date_object);
    return date_object
}

function get_days_left(date) {
    var date_object = get_date_object(date);
    //alert(due_date_object);
    var today_object = new Date();
    today_object = new Date(today_object.toDateString());
    //alert( due_date_object + " " + today_object );
    var days_left = date_object - today_object;
    var one_day = 1000*60*60*24;
    days_left = Math.round(days_left/one_day);
    //alert(days_left);
    return days_left
}

function prettify(date) {
    //alert(date);
    if (date == '') {
        return '&nbsp;'
    }
    var days_left = get_days_left(date);
    if (days_left < -7) {
        return date
    }
    else if (days_left == -1) {
        return 'Yesterday'
    }
    else if (days_left < -1) {
        return -days_left + ' days ago'
    }
    else if (days_left == 0) {
        return 'Today'
    }
    else if (days_left == 1) {
        return 'Tomorrow'
    }
    else if (days_left < 8) {
        return 'In ' + days_left + ' days'
    }
    return date
}

function get_size_of_date(due_date) {
    if (due_date == '') {
        return '20px'
    }
    days_left = get_days_left(due_date);
    if (days_left < 0) {
        return '30px'
    }
    else if (days_left < 8) {
        return 30 - days_left + 'px'
    }
    else if (days_left < 10) {
        return '23px'
    }
    return '20px'
}

function setParentId(new_parent_id) {
    parentId = new_parent_id;
}

function getParentID() {
    return parentId
}
