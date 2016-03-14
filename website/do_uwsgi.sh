killall uwsgi
uwsgi -s /tmp/uwsgi.sock -w app:app --logto app-log.txt &
chmod 666 /tmp/uwsgi.sock
