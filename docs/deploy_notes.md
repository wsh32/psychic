# Deployment notes

Currently deploying psychic onto an Ubuntu 18.04 VM. This process should be
similar for a VPS running Ubuntu 18.04 or 16.04. I'll be deploying using
`gunicorn` and `nginx`. See [this
page](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/modwsgi/) on
the django documentation for more details.

> Note that I will be referencing paths as `/path/to/something` here. To
> reference the git path, I'll be using `/path/to/git/`, meaning the folder
> where the `.git` folder exists. For example, if I clone in `/home/wsh32/git/`,
> `/path/to/git/` refers to `/home/wsh32/git/psychic`.

1. Install python3 and headers

```bash
sudo apt-get install python3 python3-dev
```

2. Install and set up virtualenv

```bash
python3 -m pip install virtualenv
python3 -m virtuanenv /path/to/virtualenv/

source /path/to/virtualenv/bin/activate
pip install -r requirements.txt

deactivate
```

3. Collect django static files

Before running gunicorn, we must collect all of the static files for django's
deployment server as it does not serve static files.

```bash
source /path/to/virtualenv/bin/activate
./manage.py collectstatic
deactivate
```

3. Test gunicorn

```bash
/path/to/virtualenv/bin/gunicorn psychic.wsgi:application --bind 0.0.0.0:8000
```

Navigate to _SERVER IP_:8000 in a web browser and you should see a preview of the
site. Note that this is still a dev version, not a production version!

4. Configure gunicorn service

Edit `/etc/systemd/system/gunicorn.service`

```
[Unit]
Description=Gunicorn application server handling psychic
Requires=gunicorn.socket
After=network.target

[Service]
PIDFile=/run/gunicorn/pid
User=_username_
Group=www-data
RuntimeDirectory=gunicorn
WorkingDirectory=/path/to/git/psychic/
ExecStart=/path/to/virtualenv/bin/gunicorn --pid /run/gunicorn/pid   \
                            --bind unix:/run/gunicorn/socket psychic.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Edit `/etc/systemd/system/gunicorn.socket`

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn/socket

[Install]
WantedBy=sockets.target
```

Edit `/etc/tmpfiles.d/gunicorn.conf`

```
d /run/gunicorn 0755 _username_ www-data -
```

5. Enable gunicorn process

```bash
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn.socket
```

6. Install nginx

```bash
sudo apt-get install nginx
```

7. Configure nginx proxy pass

Create and edit `/etc/nginx/sites-available/psychic`

```
server {
    listen 80;
    server_name _hostname or P address_;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root = /path/to/git/psychic/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn/socket;
    }
}
```

Add this as an enabled site

```bash
sudo ln -s /etc/nginx/sites-available/psychic /etc/nginx/sites-enabled
```

Test the nginx configuration for syntax errors
```bash
sudo nginx -t
```

If there are no errors, enable the nginx server

```bash
sudo service nginx restart
```

