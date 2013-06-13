// CONSTANTS
var NAME_MAX_LENGTH = 30;
var DESCRIPTION_MAX_LENGTH = 40;
var TAGS_MAX_LENGTH = 3;
//var TAG_REGEX = /(?:^|[\s])(@[\w\/\.\-\:]*\w)/g;
var TAG_REGEX = /(?:^|[\s])(@\s*[\w\/\.\-\:]*\w)/g;
var a;

// GLOBAL VARIABLES
var parentId = -1

// Task Folders

ko.bindingHandlers.htmlValue = {
    init: function(element, valueAccessor, allBindingsAccessor) {
        ko.utils.registerEventHandler(element, "blur", function() {
            //alert('registered');
            var modelValue = valueAccessor();
            var elementValue = element.innerHTML;
            //console.log('text = ' + element.textContent||element.innerText);
            elementValue = convert_texttags_to_htmltags(elementValue);
            if (ko.isWriteableObservable(modelValue)) {
                modelValue(elementValue);
                
            }
            else { //handle non-observable one-way binding
                var allBindings = allBindingsAccessor();
                if (allBindings['_ko_property_writers'] && allBindings['_ko_property_writers'].htmlValue) allBindings['_ko_property_writers'].htmlValue(elementValue);
            }
        })
    },
    update: function(element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor()) || "";
        //console.log('value = ' + value + ' innerHTML = ' + element.innerHTML);
        if (element.innerHTML !== value) {
            element.innerHTML = value;
        }
    }
};


function TaskFoldersViewModel() {
    // Data
    var self = this;
    self.folders = ['All', 'Active', 'Done', 'Dismissed'];
    self.chosenFolderId = ko.observable();
    self.tasks_list = ko.observableArray();
    self.tasks_list_length = ko.observable('0');
    self.todays_tasks = ko.observableArray();
    
    self.tags_list = ko.observableArray();
    self.modified_tasks = ko.observableArray();
    self.modify_selected = ko.observableArray();
    
    self.task_name_field = ko.observable('');
    self.task_name_htmlfield = ko.observable('');
    
    self.task_description_field = ko.observable('');
    self.task_description_htmlfield = ko.observable('');
    
    self.task_start_date_field = ko.observable('');
    self.task_due_date_field = ko.observable('');
    
    self.all_tags = ko.observableArray();
    
    self.tasks_list.subscribe(function (newValue) {
        self.tasks_list_length(newValue.length);
        show_popover();
    }, self);
    
    self.task_name_field.subscribe(function (newValue) {
        self.all_tags(eliminateDuplicates((newValue + " " + self.task_description_field()).match(TAG_REGEX)));
        //self.all_tags();

    }, self);
    
    self.task_description_field.subscribe(function (newValue) {
        self.all_tags(eliminateDuplicates((self.task_name_field() + " " + newValue).match(TAG_REGEX)));
        //self.all_tags((self.task_name_field() + " " + newValue).match(TAG_REGEX));
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
    
    self.task_start_date_field.subscribe(function (newValue) {
        //console.log('newvalue = "' + get_date_object(newValue) + '" due_date = "' + $('.task_due_datepicker').datetimepicker('getDate') + '"')
        var newvalue = get_date_object(newValue);
        var due_date_val = self.task_due_date_field();
        var due_date = get_date_object(due_date_val);
        if ((newValue != '' && due_date_val != '') && (newvalue > due_date)) {
            $('.task_due_datepicker').datetimepicker('setDate', newvalue);
        }
        
        $('.task_due_datepicker').datetimepicker('setStartDate', newvalue);
        //$('.task_due_datepicker').datetimepicker('show');
    }, self);
    
    // Behaviours
    self.goToFolder = function(folder) {
        location.hash = folder;
    };
    
    $.get('/tasks/get/due_by', { days_left: 0, folder: self.chosenFolderId() }, function(data) {
        self.todays_tasks(data);
                
        if (self.todays_tasks().length > 0 && cookie_says_yes()) {
            $('#startup_modal').modal('show');
        }
                
        show_popover();
    });
    
    $.get('/tags/all', self.tags_list);
    
    // Client-side routes
    Sammy(function() {
        this.get('#:folder', function() {
            self.chosenFolderId(this.params.folder);
            $.get('/tasks/get', { folder: this.params.folder }, function(data) {
                self.tasks_list(data);
                show_popover();
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
        
        //alert(self.task_description_field());
        $('#new_task_modal').modal('show');
        console.log(self.task_name_field());
        console.log(self.task_description_field());
        task_name_editor.setValue(self.task_name_field());
        task_description_editor.setValue(self.task_description_field());
        task_name_editor.refresh();
        task_description_editor.refresh();
        setParentId(-1);
    }
    
    self.show_new_subtask_modal = function(parent_id) {
        self.task_name_field('');
        self.task_description_field('');
        self.task_start_date_field('');
        self.task_due_date_field('');
        setParentId(parent_id);
        $('#new_task_modal').modal('show');
        console.log(self.task_name_field());
        console.log(self.task_description_field());
        task_name_editor.setValue(self.task_name_field());
        task_description_editor.setValue(self.task_description_field());
        task_name_editor.refresh();
        task_description_editor.refresh();
    }
    
    self.new_task = function() {
        if (self.task_name_field() == '') {
            alert("Task name cannot be empty");
            return
        }
        $('#new_task_modal').modal('hide');
        
        if (getParentID() == -1) {
            self.tasks_list.splice(0, 0, {
                id: -9,
                name: self.task_name_field(),
                description: self.task_description_field(),
                start_date: self.task_start_date_field(),
                due_date: self.task_due_date_field(),
                subtasks: [],
                indent: 0,
                tags: [],
            });
        }
        
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
            else {
                self.tasks_list(data);
            }
            $.get('/tags/all', self.tags_list);
            setParentId(-1);
            self.task_name_field('');
            self.task_description_field('');
            self.task_start_date_field('');
            self.task_due_date_field('');
            show_popover();
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
            $.get('/tasks/get', { folder: self.chosenFolderId }, self.tasks_list)
            $.get('/tags/all', self.tags_list);
            setParentId(-1);
            show_popover();
        });
    };
    
    self.show_edit_task_modal = function(id, name, description, start_date, due_date) {
        self.task_name_field(name);
        self.task_description_field(description);
        self.task_start_date_field(start_date);
        self.task_due_date_field(due_date);
        setParentId(id);
        $('#edit_task_modal').modal('show');
        console.log(self.task_name_field());
        console.log(self.task_description_field());
        task_name_editor.setValue(self.task_name_field());
        task_description_editor.setValue(self.task_description_field());
        task_name_editor.refresh();
        task_description_editor.refresh();
    }
    
    self.hide_edit_task_modal = function() {
        $('#edit_task_modal').modal('hide');
        self.task_name_field('');
        self.task_description_field('');
        self.task_start_date_field('');
        self.task_due_date_field('');
        task_name_editor.setValue('');
        task_description_editor.setValue('');
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
            show_popover();
        });
        //alert(self.modify_selected());
    }
    
    self.change_status = function (id, new_status, index) {
        $.get('/tasks/modify/status', { task_id:id, task_id_list: self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, function(data) {
            /*if (self.modify_selected().length == 0) {
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
            else {
                self.tasks_list(data);
            }*/
            self.tasks_list(data);
            show_popover();
            self.modify_selected([]);
        });
        //self.tasks_list.Elements.replace(self.tasks_list()[index], self.modified_tasks);
    };
    
    self.delete_task = function(id, index) {
        //alert(id);
        $.get('/tasks/delete/', { task_id:id, task_id_list: self.modify_selected(), folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            show_popover();
            $.get('/tags/all', self.tags_list);
        });
    };
    
    self.get_tasks_by_tag = function(id) {
        $.get('/tags/get_tasks', { tag_id:id, folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            show_popover();
        });
    }
    
    update_description_field = function(text) {
        self.task_description_field(text);
    }
    
    get_description_field = function() {
        return self.task_description_field()
    }
};

ko.applyBindings(a = new TaskFoldersViewModel(), document.getElementById("html_page"));

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

function tags_are_less(tags_length) {
    //alert(tags_length);
    return tags_length < TAGS_MAX_LENGTH
}

function get_remaining_tags(tags) {
    var remaining_tags = '';
    for (var i=TAGS_MAX_LENGTH-1; i < tags.length; i++) {
        remaining_tags += '<span class="label" style="background-color: ' + tags[i].color + '">' + tags[i].name + '</span>&nbsp;'
    }
    return remaining_tags
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

function eliminateDuplicates(arr) {
    var i, out=[], obj={};
    if (arr != null) {
        var len = arr.length;
    }
    else {
        var len = 0;
    }
    
    for (i=0;i<len;i++) {
        obj[arr[i]]=0;
    }
    for (i in obj) {
        out.push(i);
    }
    return out;
}

function show_popover() {
    //alert('working');
    $('strong.task_name').popover({
        placement: 'top',
        trigger: 'hover',
        //delay: { show: 400, hide: 0 },
    });
    $('span.task_description').popover({
        placement: 'top',
        trigger: 'hover',
        //delay: { show: 400, hide: 0 },
    });
    $('i.remaining_tags_icon').popover({
        placement: 'top',
        trigger: 'hover',
        html: true,
        //delay: { show: 400, hide: 0 },
    });
}

function startup_modal_header_string(length) {
    if (length > 1) {
        return length + ' tasks'
    }
    return length + ' task'
}

function cookie_says_yes() {
    var a = $.cookie('startup_dialog_shown');
	//var username = "{{ username }}";
	today = new Date();
	today.setHours(0,0,0,0);
	if (a == null) {
		$.cookie('startup_dialog_shown', today, { expires: 1 });
		return true
	}
	else if (today != a) {
		//alert(today + " " + a);
		$.cookie('startup_dialog_shown', today, { expires: 1 });
		return true
	}
	return false
}

function convert_texttags_to_htmltags(text) {
    text = text.replace('&nbsp;', ' ');
    
    var tags = text.match(TAG_REGEX);
    if (tags == null) {
        var length = 0;
        return text;
    }
    else {
        var length = tags.length;
    }
    console.log('tags = "' + tags + '"');
    for (var i=0; i < length; i++) {
        if (text.indexOf(tags[i] + '</span>') == -1) {
            console.log('not found ' + tags[i] + ' replacing ...');
        text = text.replace(tags[i], " " + '<span class="label label-input">' + tags[i].toLowerCase().replace(/^ /, '') + '</span>');
        }
    }
    text = text.replace('<span class="label label-input"></span>', '>@<');
    //text = text.replace('<span class="label label-input"></span>', '@');
    
    console.log('at the end, text = "' + text + '"');
    return text;
}

function update_description(text) {
    a.task_description_field(text);
    console.log(a.task_description_field());
}

function start_codemirror(name_id, description_id) {
    
    task_name_editor = new CodeMirror.fromTextArea(document.getElementById(name_id), {
		mode: 'diff2',
		parserfile: "../static/js/data/parsediff.js",
		//stylesheet: "../static/css/task_editor.css",
		electricChars: false,
		extraKeys: {
			Enter: function(cm) { return; },
			Tab: function(cm) { return; },
		},
		lineWrapping: true,
        tabindex: 1,
	});
		
	task_name_editor.on("change", function(cm, change) {
		//console.log("something changed! (" + change.origin + ")");
        a.task_name_field(task_name_editor.getValue());
	});
    
    task_name_editor.setSize(466, 28);
    task_name_editor.setValue(a.task_name_field());
    task_name_editor.getWrapperElement().style["min-height"] = "28px";
    //task_name_editor.getWrapperElement().style["max-height"] = "64px";
    task_name_editor.getWrapperElement().style["font-weight"] = "bold";
    task_name_editor.getWrapperElement().style["font-size"] = "20px";
    task_name_editor.getWrapperElement().style["display"] = "block";
    //task_name_editor.getWrapperElement().style["tabindex"] = 1;
    task_name_editor.refresh();
    //task_name_editor.getInputField().tabIndex = 1;
    
    task_description_editor = new CodeMirror.fromTextArea(document.getElementById(description_id), {
		mode: 'diff2',
		parserfile: "../static/js/data/parsediff.js",
		//stylesheet: "../static/css/task_editor.css",
		electricChars: false,
		extraKeys: {
			Enter: function(cm) { cm.replaceSelection("\n", "end"); },
			Tab: function(cm) { return; },
		},
		lineWrapping: true,
        tabindex: 2,
	});
		
	task_description_editor.on("change", function(cm, change) {
		//console.log("something changed! (" + change.origin + ")");
        a.task_description_field(task_description_editor.getValue());
	});
    
    task_description_editor.setSize(466, 200);
    task_description_editor.setValue(a.task_description_field());
    task_description_editor.getWrapperElement().style["font-weight"] = "normal";
    task_description_editor.getWrapperElement().style["display"] = "block";
    //task_description_editor.getWrapperElement().style["tabindex"] = 2;
    task_description_editor.refresh();
    //task_description_editor.getInputField().tabIndex = 2;
}
