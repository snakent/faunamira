# faunamira

nginx config:

server {
    server_name faunamira.ru www.faunamira.ru fauna-mira.ru www.fauna-mira.ru faunamira.com www.faunamira.com;
    access_log  /var/log/nginx/example.log;
    client_max_body_size 64M;

    location /static/ {
        root /home/fauna/faunamira;
        expires 30d;
    }

    location /media/ {
        root /home/fauna/faunamira/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Host $http_host;
        proxy_redirect off;
    }

    location /chat/stream/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }

    listen 443 ssl http2; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/faunamira.ru/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/faunamira.ru/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.faunamira.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    
    if ($host = faunamira.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = www.fauna-mira.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = fauna-mira.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    
    if ($host = www.faunamira.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = faunamira.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    server_name 185.93.109.126 faunamira.ru www.faunamira.ru fauna-mira.ru www.fauna-mira.ru faunamira.com www.faunamira.com;

    listen 80;
    return 404; # managed by Certbot
}
