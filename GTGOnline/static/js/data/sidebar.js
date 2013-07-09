// CONSTANTS
var NAME_MAX_LENGTH = 30;
var DESCRIPTION_MAX_LENGTH = 40;
var TAGS_MAX_LENGTH = 3;
var EMAIL_MAX_LENGTH = 30;
var USER_NAME_MAX_LENGTH = 13;
var GROUP_NAME_MAX_LENGTH = 7;
var NAME_USER_SELECTION_MAX_LENGTH = 24;
//var TAG_REGEX = /(?:^|[\s])(@[\w\/\.\-\:]*\w)/g;
var TAG_REGEX = /(@[\w\/\.\-\:]*\w)/g;
var a;
var task_name_editor;
var task_description_editor;

// GLOBAL VARIABLES
var parentId = -1;
var shareId = -1;
var is_edit_task = 1;

// Task Folders

ko.bindingHandlers.htmlValue = {
    init: function(element, valueAccessor, allBindingsAccessor) {
        ko.utils.registerEventHandler(element, "blur", function() {
            //alert('registered');
            var modelValue = valueAccessor();
            var elementValue = element.innerHTML;
            console.log('text = ' + element.textContent||element.innerText);
            //elementValue = convert_texttags_to_htmltags(elementValue);
            //highlight(document.getElementById('task_description_field2'),'@tag','label-input label');
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
        console.log('value = ' + value + ' innerHTML = ' + element.innerHTML);
        if (element.innerHTML !== value) {
            element.innerHTML = value;
        }
    }
};

ko.bindingHandlers.minicolors = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        var options = {
			animationSpeed: 100,
			animationEasing: 'swing',
			change: null,
			changeDelay: 0,
			control: 'saturation',
			defaultValue: '',
			hide: null,
			hideSpeed: 100,
			inline: false,
			letterCase: 'uppercase',
			opacity: false,
			position: 'default',
			show: null,
			showSpeed: 100,
			swatchPosition: 'left',
			textfield: true,
			theme: 'bootstrap'
		};

        var funcOnSelectColor = function () {
            var observable = valueAccessor();
            observable($(element).minicolors("value"));
        };

        //-- also change event to hide
        options.hide = funcOnSelectColor;

        $(element).minicolors(options);

        //handle the field changing
        ko.utils.registerEventHandler(element, "change", funcOnSelectColor);

        //handle disposal (if KO removes by the template binding)
        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            $(element).minicolors("destroy");
        });
    },
 
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        var current = $(element).minicolors("value");
        if (value - current !== 0) {
            $(element).minicolors("value", value);
        }
    }
};


function TaskFoldersViewModel() {
    // Data
    var self = this;
    self.folders = ['All', 'Active', 'Done', 'Dismissed'];
    self.chosenFolderId = ko.observable();
    self.titlebar_display = ko.observable('');
    self.tasks_list = ko.observableArray();
    self.tasks_list_length = ko.observable('0');
    self.todays_tasks = ko.observableArray();
    
    self.tags_list = ko.observableArray();
    self.modified_tasks = ko.observableArray();
    self.modify_selected = ko.observableArray();
    
    self.task_list_field = ko.observable('');
    
    self.task_name_field = ko.observable('');
    self.task_name_htmlfield = ko.observable('');
    
    self.task_description_field = ko.observable('');
    self.task_description_htmlfield = ko.observable('');
    
    self.task_start_date_field = ko.observable('');
    self.task_due_date_field = ko.observable('');
    self.search_query = ko.observable('');
    self.search_option = ko.observable('');
    self.header_name = ko.observable('');
    self.selected_tag = ko.observable('');
    self.new_group_name = ko.observable('');
    self.tag_color = ko.observable('#F89406');
    
    self.all_tags = ko.observableArray();
    self.task_dict = ko.observableArray();
    self.user_list = ko.observableArray();
    self.group_list = ko.observableArray();
    self.visited_users = ko.observableArray();
    self.checked_groups = ko.observableArray();
    self.checked_users = ko.observableArray();
    
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
            //$("#header").hide();
        }
        else {
            $("#dropdown").hide();
            //$("#header").show();
        }
    }, self);
    
    self.task_start_date_field.subscribe(function (newValue) {
        //console.log('newvalue = "' + get_date_object(newValue) + '" due_date = "' + $('.task_due_datepicker').datetimepicker('getDate') + '"')
        var newvalue = get_date_object(newValue);
        var due_date_val = self.task_due_date_field();
        var due_date = get_date_object(due_date_val);
        
        $('.task_due_datepicker').datetimepicker('setStartDate', newvalue);
        //console.log('newvalue = ' + newValue + ' due_date = ' + due_date_val);
        
        if ((newValue != '' && due_date_val != '') && (newvalue > due_date)) {
            //console.log('changed');
            $('.task_due_datepicker').datetimepicker('setDate', newvalue);
        }
        
        //$('.task_due_datepicker').datetimepicker('setStartDate', newvalue);
        //$('.task_due_datepicker').datetimepicker('show');
    }, self);
    
    self.tag_color.subscribe(function (newValue) {
        //alert('newvalue = ' + newValue);
        $.get('/tags/modify/color/',{ tag_name: self.selected_tag(), new_color: newValue, folder: self.chosenFolderId() }, function(data){
            self.tasks_list(data);
            $.get('/tags/all/', self.tags_list);
            show_popover();
        });
    }, self);
    
    self.user_list.subscribe(function (newValue) {
        self.group_list([]);
        self.visited_users([]);
        for (var i=0; i < newValue.length; i++) {
            var group = newValue[i];
            if (group.name != 'Others') {
                self.group_list.push(group.name);
                for (var j=0; j < group.members.length; j++) {
                    self.visited_users.push(group.members[j].email);
                }
            }
        }
        console.log(self.visited_users());
    }, self);
    
    self.checked_groups.subscribe(function (newValue) {
        //alert('newvalue = "' + newValue + '"');
        self.checked_users([]);
        for (var i=0; i < newValue.length; i++) {
            var match = ko.utils.arrayFirst(self.user_list(), function(item) {
                //alert(data[0].id);
                return newValue[i] === item.name;
            });
            if (match) {
                console.log(match);
                for (var j=0; j < match.members.length; j++) {
                    var email = match.members[j].email;
                    console.log('email = ' + email);
                    self.checked_users.push(email);
                    //document.getElementById('e' + email).style.border = "2px solid green";
                }
            }
        }
        console.log(self.checked_users());
    }, self);
    
    self.checked_users.subscribe(function (newValue) {
        console.log(newValue);
    }, self);
    
    // Behaviours
    self.goToFolder = function(folder) {
        location.hash = folder;
        self.header_name(this.params.folder + ' Tasks');
        self.titlebar_display(this.params.folder + ' Tasks');
        $("#tag_dropdown_options").hide();
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
            self.header_name(this.params.folder + ' Tasks');
            self.titlebar_display(this.params.folder + ' Tasks');
            $("#tag_dropdown_options").hide();
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
            this.app.runRoute('get', '#Active');
            //location.hash = '#Active';
        });
    }).run();
    
    self.show_new_task_modal = function(id) {
        //task_name_editor.setValue('afd');
        //task_description_editor.setValue('fs');
        //self.task_name_field(name);
        self.task_list_field('• ');
        //self.task_start_date_field(start_date);
        //self.task_due_date_field(due_date);
        setParentId(id);
        //setMode(mode);
        clear_all_globals();
        $('#new_task_modal').modal('show');
        
        $('#new_task_modal').on('shown', function() {
            console.log('new task modal shown');
            //task_name_editor.refresh();
            //task_description_editor.refresh();
            $("#task_list_field").highlightTextarea('highlight');
            //$("#task_name_input").highlightTextarea('highlight');
            $("#task_list_field").focus();
            set_caret(2);
        });
        
        $('#new_task_modal').on('hidden', function() {
            //self.task_name_field('');
            //self.task_description_field('');
            //self.task_start_date_field('');
            //self.task_due_date_field('');
            //task_name_editor.setValue('');
            //task_description_editor.setValue('');
            //task_name_editor.refresh();
            //task_description_editor.refresh();
            //$("#task_description_field2").highlightTextarea('highlight');
            //$("#task_name_input").highlightTextarea('highlight');
            self.task_list_field('• ');
            $("#task_list_field").highlightTextarea('highlight');
        });
    };
    
    self.show_edit_task_modal = function(id, name, description, start_date, due_date) {
        //task_name_editor.setValue(name);
        //task_description_editor.setValue(description);
        self.task_name_field(name);
        self.task_description_field(description);
        self.task_start_date_field(start_date);
        self.task_due_date_field(due_date);
        setParentId(id);
        //setMode(mode);
        clear_all_globals();
        $('#edit_task_modal').modal('show');
        
        $('#edit_task_modal').on('shown', function() {
            console.log('edit task modal shown');
            //task_name_editor.refresh();
            //task_description_editor.refresh();
            $("#task_description_field").highlightTextarea('highlight');
            $("#task_name_field").highlightTextarea('highlight');
            $("#task_name_field").focus();
            //set_caret(2);
        });
        
        $('#edit_task_modal').on('hidden', function() {
            self.task_name_field('');
            self.task_description_field('• ');
            self.task_start_date_field('');
            self.task_due_date_field('');
            $("#task_description_field").highlightTextarea('highlight');
            $("#task_name_field").highlightTextarea('highlight');
            //task_name_editor.setValue('');
            //task_description_editor.setValue('');
            //task_name_editor.refresh();
            //task_description_editor.refresh();
            //$("#task_description_field").highlightTextarea('highlight');
            //$("#task_name_field").highlightTextarea('highlight');
        });
    };
    
    self.close_task_modal = function() {
        $('#new_task_modal').modal('hide');
        $('#edit_task_modal').modal('hide');
        self.task_name_field('');
        self.task_list_field('• ');
        self.task_description_field('');
        self.task_start_date_field('');
        self.task_due_date_field('');
        //task_name_editor.setValue('');
        //task_description_editor.setValue('');
        //task_name_editor.refresh();
        //task_description_editor.refresh();
    };
    
    self.create_task = function() {
        /*if (self.task_name_field() == '') {
            alert("Task name cannot be empty");
            return
        }*/
        $('#task_modal').modal('hide');
        
        self.task_name_field(convert_tags_to_lower(self.task_name_field()));
        self.task_description_field(convert_tags_to_lower(self.task_description_field()));
        
        if (getParentID() == -1 || !getMode()) {
            //self.new_task_or_subtask();
            self.parse_list();
            self.send_list_to_server();
        }
        else {
            self.update_task();
        }
    };
    
    self.send_list_to_server = function() {
        if (self.task_list_field().match(/^\s*•{0,}\s*$/)) {
            alert('Task List cannot be empty');
            return;
        }
        $('#new_task_modal').modal('hide');
        self.parse_list();
        var json_data = ko.toJSON(self.task_dict());
        console.log(json_data);
        $.post('/tasks/new_list/', {
            new_list: json_data,
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
            //self.task_name_field('');
            //self.task_description_field('');
            //self.task_start_date_field('');
            //self.task_due_date_field('');
            //task_name_editor.setValue('');
            //task_description_editor.setValue('');
            //task_name_editor.refresh();
            //task_description_editor.refresh();
            self.task_list_field('');
            self.task_dict([]);
            show_popover();
        });
    }
    
    self.new_task_or_subtask = function() {
        /*self.tasks_list.splice(0, 0, {
            id: -9,
            name: self.task_name_field(),
            description: self.task_description_field(),
            start_date: self.task_start_date_field(),
            due_date: self.task_due_date_field(),
            subtasks: [],
            indent: 0,
            tags: [],
        });*/
            
        $.get('/tasks/new_list', {
            name: self.task_name_field(),
            new_list: self.task_description_field() == '' ? 'none': self.task_description_field(),
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
            show_popover();
            $.get('/tags/all', self.tags_list);
            self.task_name_field('');
            self.task_description_field('');
            self.task_start_date_field('');
            self.task_due_date_field('');
            task_name_editor.setValue('');
            task_description_editor.setValue('');
            task_name_editor.refresh();
            task_description_editor.refresh();
        });
    };
    
    self.update_task = function() {
        $('#edit_task_modal').modal('hide');
        $.get('/tasks/update', {
            name: self.task_name_field(),
            description: self.task_description_field() == '' ? 'none': self.task_description_field(),
            start_date: self.task_start_date_field(),
            due_date: self.task_due_date_field(),
            folder: self.chosenFolderId(),
            task_id: getParentID(),
        }, function(data) {
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
            self.task_name_field('');
            self.task_description_field('');
            self.task_start_date_field('');
            self.task_due_date_field('');
            //task_name_editor.setValue('');
            //task_description_editor.setValue('');
            //task_name_editor.refresh();
            //task_description_editor.refresh();
            show_popover();
        });
    };
    
    self.parse_list = function() {
        var lines = self.task_list_field().split(/\n\t*/);
        console.log(lines);
        var parsed_list = [], description_string = "";
        for (var i=0; i < lines.length; i++) {
            var returned_list = parse_dates_update_line(lines[i]);
            var start_date = returned_list[0];
            var due_date = returned_list[1];
            var new_line = returned_list[2];
            console.log('main line checking, ' + new_line);
            var level = new_line.match(/(\d*)•\s*/);
            //console.log('start date = "' + start_date + '" due_date = "' + due_date + '"');
            //if (level == null) {
                //new_line = new_line.replace(/^\t*»\s*/, '');
                //new_line = new_line.replace(/^\t*\s*/, '');
                //description_string += new_line + '\n';
            //}
            if (level != null) {
                var name = new_line;
                description_string = "";
                for (var j=i+1; j<lines.length; j++) {
                    console.log('checking line, "' + lines[j] + '"');
                    var inner_level = lines[j].match(/(\d*)•\s*/);
                    //console.log('start date = "' + start_date + '" due_date = "' + due_date + '"');
                    if (inner_level == null) {
                        returned_list = parse_dates_update_line(lines[j]);
                        start_date = returned_list[0] == "" ? start_date : returned_list[0];
                        due_date = returned_list[1] == "" ? due_date : returned_list[1];
                        new_line = returned_list[2];
                        new_line = new_line.replace(/^\t*\s*»\s*/, '');
                        console.log('after replacing », inner line = "' + new_line + '"');
                        new_line = new_line.replace(/^\t*\s*/, '');
                        description_string += new_line + '\n';
                    }
                    else{
                        i=j-1;
                        break;
                    }
                }
                
                console.log('level = "' + level[1] + '"');
                name = name.replace(level[0], '');
                console.log('name = "' + name + '"');
                console.log('description = "' + description_string + '"');
                if (level[1] == "") {
                    level[1] = '0';
                }
                self.task_dict.push({
                    'name': name,
                    'description': description_string == "" ? 'none' : description_string,
                    'start_date': start_date,
                    'due_date': due_date,
                    'level': level[1],
                });
                //description_string = "";
            }
            var drwef = '»(\s*[\S\s]*)\t*•';
        }
        
        console.log(self.task_dict());
        //return task_dict;
    };
    
    self.reset_start_date_field = function() {
        self.task_start_date_field('')
    };
    
    self.reset_due_date_field = function() {
        self.task_due_date_field('')
    };
    
    self.mark_done = function (new_status) {
        //alert(self.modify_selected());
        $.get('/tasks/modify/status', { task_id:self.modify_selected(), status: new_status, folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            show_popover();
        });
        //alert(self.modify_selected());
    };
    
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
            $("#dropdown").hide();
        });
    };
    
    self.get_tasks_by_tag = function(name) {
        $.get('/tags/get_tasks', { tag_name: name, folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            self.header_name(self.chosenFolderId() + ' Tasks having tag - ');
            show_popover();
            //$('#tag_dropdown_name').html(name);
            self.selected_tag(name);
            $("#tag_dropdown_options").show();
        });
    };
    
    self.set_search_option = function(option) {
        self.search_option(option);
    }
    
    self.call_search = function() {
        //alert(self.search_query());
        if (self.search_option() == 0) {
            console.log('search in tasks');
            $.get('/tasks/search/', { query: self.search_query(), folder: self.chosenFolderId() }, function(data) {
                self.tasks_list(data);
                self.header_name('Filtered tasks having - "' + self.search_query() + '" in name');
                self.search_query('');
                show_popover();
            });
        }
        else if (self.search_option() == 1) {
            console.log('search in users');
            window.location = '/user/search/?query=' + self.search_query();
        }
    };
    
    self.delete_tag = function() {
        //alert('to be deleted - ' + self.selected_tag());
        $.get('/tags/delete', { tag_name: self.selected_tag() }, self.tags_list);
    };
    
    self.change_tag_color = function() {
        $.get('/tags/modify/color/',{ tag_name: self.selected_tag(), new_color: self.tag_color() }, self.tags_list);
    };
    
    self.show_users = function(origin, query, user_list) {
        //console.log(query);
        document.getElementById('topbar_search_input').setAttribute('placeholder', 'Search in Users');
        console.log(origin);
        self.search_query(query);
        var obj = JSON.parse(user_list);
        console.log(obj);
        self.user_list(obj);
        //document.getElementById('user_option_button').setAttribute('class', 'btn active');
        if (origin == 'group') {
            self.titlebar_display('Groups and members');
        }
        else {
            self.titlebar_display('Users matching query "' + query + '"');
        }
        self.search_option(1);
        console.log(self.group_list());
    };
    
    self.get_user_profile = function(email) {
        $.get('/tasks/search/', { query: self.search_query(), folder: self.chosenFolderId() }, function(data) {
            self.tasks_list(data);
            self.header_name('Filtered tasks having - "' + self.search_query() + '" in name');
            self.search_query('');
            show_popover();
        });
    };
    
    self.show_more_users = function() {
        var users = document.getElementById('more_users');
        if (users == null) {
            users = document.getElementById('share_more_users');
        }
        users.style.display = 'none';
        $.post('/user/search/json/', { query: self.search_query(), visited: self.visited_users() }, function(data) {
            console.log(data[0]);
            //console.log(self.user_list());
            self.user_list.push(data[0]);
        });
    };
    
    self.add_user_to_group = function(email, group_old, group_new) {
        $.get('/groups/add/', { name: group_new, email: email }, function(data) {
            //console.log(data);
            var match = ko.utils.arrayFirst(self.user_list(), function(item) {
                //alert(data[0].id);
                return data[0].name === item.name;
            });
            if (match) {
                //alert(match.name);
                self.user_list.replace(match, data[0]);
                //alert(match.name);
            }
            else {
                alert("no match found");
            };
            $.post('/groups/list/', { name: group_old, visited: self.visited_users() }, function(data) {
                var match = ko.utils.arrayFirst(self.user_list(), function(item) {
                    //alert(data[0].id);
                    return data[0].name === item.name;
                });
                if (match) {
                    //alert(match.name);
                    self.user_list.replace(match, data[0]);
                    //alert(match.name);
                }
                else {
                    alert("no match found");
                }
            });
        });
    };
    
    self.remove_user_from_group = function(group, email) {
        $.get('/groups/remove/', { name: group, email: email }, function(data) {
            //console.log(data);
            var match = ko.utils.arrayFirst(self.user_list(), function(item) {
                //alert(data[0].id);
                return data[0].name === item.name;
            });
            if (match) {
                //alert(match.name);
                self.user_list.replace(match, data[0]);
                //alert(match.name);
            }
            else {
                alert("no match found");
            }
            $.post('/groups/list/', { name: 'Others', visited: self.visited_users() }, function(data) {
                var match = ko.utils.arrayFirst(self.user_list(), function(item) {
                    //alert(data[0].id);
                    return data[0].name === item.name;
                });
                if (match) {
                    //alert(match.name);
                    self.user_list.replace(match, data[0]);
                    //alert(match.name);
                }
                else {
                    //self.user_list.push(data[0]);
                }
            });
        });
    };
    
    self.new_group = function() {
        console.log('name = ' + self.new_group_name() + ' color = ' + self.tag_color());
        if (self.new_group_name() == '') {
            alert('Please enter a name');
            return;
        }
        $.get('/groups/new/', { name: self.new_group_name(), color: self.tag_color() }, function(data) {
            console.log(data);
            self.user_list(data);
            if (document.getElementById('more_users').style.display == 'none') {
                $.post('/groups/list/', { name: 'Others', visited: self.visited_users() }, function(data) {
                    self.user_list.push(data[0]);
                });
            }
            self.new_group_name('');
            self.tag_color('#F89406');
        });
    };
    
    self.delete_group = function(name) {
        console.log(name);
        $.get('/groups/delete/', { name: name }, function(data) {
            console.log(data);
            self.user_list(data);
            if (document.getElementById('more_users').style.display == 'none') {
                $.post('/groups/list/', { name: 'Others', visited: self.visited_users() }, function(data) {
                    self.user_list.push(data[0]);
                });
            }
        });
    };
    
    self.show_share_task_modal = function(id) {
        $.post('/groups/list/', {}, function(data) {
            self.user_list(data);
        });
        setShareId(id);
        $('#share_task_modal').modal('show');
        document.getElementById('share_more_users').style.display = 'block';
        
        $('#share_task_modal').on('shown', function() {
            console.log('share task modal shown');
        });
        
        $('#share_task_modal').on('hidden', function() {
            console.log('share task modal hidden');
        });
    };
    
    self.close_share_task_modal = function() {
        $('#share_task_modal').modal('hide');
    };
    
    self.share_task = function() {
        console.log('id = ' + getShareID());
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

function shortify_full_name(full_name) {
    return full_name.substring(0, USER_NAME_MAX_LENGTH + 8);
}

function get_size_for_name(full_name) {
    var length = full_name.length;
    var max_length = USER_NAME_MAX_LENGTH;
    if (length < max_length) {
        return '18px';
    }
    else if (length < max_length + 2) { //max 15
        return '16px';
    }
    else if (length < max_length + 5) { // max 17
        return '14px';
    }
    return '12px';
}

function shortify_email(email) {
    return email.substring(0, EMAIL_MAX_LENGTH);
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

/*function get_formatted_date(date_str) {
    var chunks = date_str.split('/');
    var formatted_date = chunks[1] + '/' + chunks[0] + '/' + chunks[2];
    return formatted_date
}*/

function get_formatted_date(date_str) {
    var chunks = date_str.split('/');
    var formatted_date = '20' + chunks[2] + '-' + chunks[1] + '-' + chunks[0];
    return formatted_date
}

function get_date_object(date_str) {
    if (date_str == '') {
        //console.log('given date was empty');
        return null
    }
    var formatted_date = get_formatted_date(date_str)
    //console.log('formatted date = ' + formatted_date);
    var date_object = new Date(formatted_date);
    //console.log('computed date object = ' + date_object);
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

function setMode(mode) {
    is_edit_task = mode;
}

function getMode() {
    return is_edit_task;
}

function setShareId(new_share_id) {
    shareId = new_share_id;
}

function getShareID() {
    return shareId
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
        if (text.indexOf(tags[i] + '</em>') == -1) {
            console.log('not found ' + tags[i] + ' replacing ...');
        text = text.replace(tags[i], " " + '<em class="label label-input">' + tags[i].toLowerCase().replace(/^ /, '') + '</em>');
        }
    }
    text = text.replace('<em class="label label-input"></em>', '>@<');
    //text = text.replace('<span class="label label-input"></span>', '@');
    
    console.log('at the end, text = "' + text + '"');
    return text;
}

function convert_tags_to_lower(text) {
    var tags_list = text.match(TAG_REGEX);
    if (tags_list == null) {
        return text;
    }
    
    for (var i=0; i < tags_list.length; i++) {
        text = text.replace(tags_list[i], tags_list[i].toLowerCase());
    }
    return text;
}

function start_codemirror(name_id, description_id) {
    var converted_tag = [], text = '', text2 = '';
    
    task_name_editor = new CodeMirror.fromTextArea(document.getElementById(name_id), {
		mode: 'diff2',
		parserfile: "../static/js/data/parsediff.js",
		//stylesheet: "../static/css/task_editor.css",
		electricChars: false,
		extraKeys: {
			Enter: function(cm) { return; },
			Tab: false,
		},
		lineWrapping: true,
        //tabindex: 1,
	});

    task_name_editor.setSize(466, 28);
    task_name_editor.setValue(a.task_name_field());
    task_name_editor.getWrapperElement().style["min-height"] = "28px";
    //task_name_editor.getWrapperElement().style["max-height"] = "64px";
    task_name_editor.getWrapperElement().style.fontWeight = "bold";
    task_name_editor.getWrapperElement().style.fontSize = "20px";
    task_name_editor.getWrapperElement().style["display"] = "none";
    task_name_editor.refresh();
    
    task_name_editor.on("change", function(cm, change) {
		//console.log("something changed! (" + cm.getDoc().getValue() + ")");
        a.task_name_field(cm.getDoc().getValue());
        console.log('new name value = "' + cm.getDoc().getValue() + '"');
	});
    
    task_description_editor = new CodeMirror.fromTextArea(document.getElementById(description_id), {
		mode: 'diff2',
		parserfile: "../static/js/data/parsediff.js",
		//stylesheet: "../static/css/task_editor.css",
		electricChars: false,
		extraKeys: {
			Enter: function(cm) { cm.replaceSelection("\n", "end"); },
			Tab: false,
		},
		lineWrapping: true,
        //tabindex: 2,
	});
    
    task_description_editor.setSize(466, 200);
    task_description_editor.setValue(a.task_description_field());
    task_description_editor.getWrapperElement().style["font-weight"] = "normal";
    task_description_editor.getWrapperElement().style["display"] = "none";
    task_description_editor.getWrapperElement().style.fontWeight = "normal";
    task_description_editor.getWrapperElement().style.fontSize = "14px";
    //task_description_editor.getWrapperElement().style["tabindex"] = 2;
    task_description_editor.refresh();
    //task_description_editor.getInputField().tabIndex = 2;
    
    task_description_editor.on("change", function(cm, change) {
        a.task_description_field(cm.getDoc().getValue());
        console.log('new des value = "' + cm.getDoc().getValue() + '"');
	});
}

function get_gravatar_image_url(email, size) {
    var gravatar_api = "http://www.gravatar.com/avatar/";
    var hashed_email = md5(email);
    var options = "?s=" + size + "&d=identicon";
    return gravatar_api + hashed_email + options;
}

function mark_selected2(id) {
    alert('id = ' + id);
    if (a.modify_selected().indexOf(id) > -1) {
        document.getElementById('for_marking' + id).style.backgroundColor = '#23AA2A';
    }
}

function parse_dates_update_line(line) {
    var start_date = '', due_date = '';
    var match = line.match(/start\s*:\s*(\d{1,2}\/\d{1,2}\/\d{2,4})|start\s*:\s*(\w{5,9})\s*/i);
    //console.log('match = ' + match + ' date = ' + RegExp.$1);
    if (match != null){
        start_date = match[1];
        console.log('start date = ' + start_date);
        if (start_date == undefined) {
            start_date = get_date_from_text(match[2]);
        }
        console.log('new start date = ' + start_date);
        line = line.replace(match[0], '');
    }
    match = line.match(/due\s*:\s*(\d{1,2}\/\d{1,2}\/\d{2,4})|due\s*:\s*(\w{5,9})\s*/i);
    if (match != null){
        due_date = match[1];
        if (due_date == undefined) {
            due_date = get_date_from_text(match[2]);
        }
        //console.log('due date = ' + due_date);
        line = line.replace(match[0], '');
    }
    //console.log('start date = "' + start_date + '" due_date = "' + due_date + '" line = "' + line + '"');
    return [start_date, due_date, line];
}

function get_date_from_text(text) {
    if (text == undefined) {
        return "";
    }
    else if (text.toLowerCase() == 'today') {
        var currentdate = new Date();
        var month = currentdate.getMonth() + 1;
        return currentdate.getDate() + '/' + month + '/' + currentdate.getFullYear();
    }
    else if (text.toLowerCase() == 'tomorrow') {
        var currentdate = new Date();
        currentdate.setDate(currentdate.getDate() + 1);
        var month = currentdate.getMonth() + 1;
        return currentdate.getDate() + '/' + month + '/' + currentdate.getFullYear();
    }
    else if (text.toLowerCase() == 'yesterday') {
        var currentdate = new Date();
        currentdate.setDate(currentdate.getDate() - 1);
        var month = currentdate.getMonth() + 1;
        return currentdate.getDate() + '/' + month + '/' + currentdate.getFullYear();
    }
    return "";
}

function get_profile_template(email) {
    window.location = '/user/profile/?email=' + email;
}

function hex2rgba(h) {
    console.log('hex color = ' + h);

    var r = parseInt((cutHex(h)).substring(0,2),16);
    var g = parseInt((cutHex(h)).substring(2,4),16);
    var b = parseInt((cutHex(h)).substring(4,6),16);
    function cutHex(h) {return (h.charAt(0)=="#") ? h.substring(1,7):h}

    return "rgba(" + r + "," + g + "," + b + ", 0.3)"
}

function prettify_group_name(name) {
    if (name == 'Others') {
        return '<i class="icon-check-empty">&nbsp;</i>Add'
    }
    if (name.length > GROUP_NAME_MAX_LENGTH) {
        return '<i class="icon-circle-blank">&nbsp;</i>' + name.substring(0, GROUP_NAME_MAX_LENGTH-2) + '...'
    }
    return '<i class="icon-circle-blank">&nbsp;</i>' + name
}

function get_attr_user_selection(name) {
    if (name.length < USER_NAME_MAX_LENGTH) {
        return {'width': '85px','lineHeight': '30px', 'marginLeft': '5px', 'fontSize': '14px'}
    }
    return {'width': '85px','lineHeight': '15px', 'marginLeft': '5px', 'fontSize': '12px'}
}

function prettify_name_user_selection(name) {
    var max = NAME_USER_SELECTION_MAX_LENGTH;
    if (name.length > max) {
        return name.substring(0, max-2) + '..'
    }
    return name
}
