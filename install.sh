python manage.py syncdb
cd GTGOnline
mkdir logs
echo "Created logs directory"
cd logs
mkdir Group_backend
touch Group_backend/group_logfile
echo "Created logfile for Groups"
mkdir Task_backend
touch Task_backend/task_logfile
echo "Created logfile for Tasks"
mkdir Tag_backend
touch Tag_backend/tag_logfile
echo "Created logfile for Tags"
mkdir User_backend
touch User_backend/user_logfile
echo "Created logfile for Users"
