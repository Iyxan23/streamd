# streamd

A for-fun streaming platform project making use of RTMP

Thanks to Ben Willber for sharing his way of building a video livestream using django and nginx's rtmp module, the link
to his article
is [here](https://benwilber.github.io/nginx/rtmp/live/video/streaming/2018/03/25/building-a-live-video-streaming-website-part-1-start-streaming.html).

### Nginx configuration
```conf
        ...
        location ~ ^/live/.+\.ts$ {
            expires max;
        }

        location ~ ^/live/[^/]+/index\.m3u8$ {
            expires -1d;
        }

        location / {
            # Use proxy_pass http://127.0.0.1:8000/; if you don't use wsgi
            wsgi_pass UPSTREAM;
            ...
        }
        ...

rtmp {
    server {
        listen 1935;

        application app {
            live on;

            # Don't allow RTMP playback
            deny play all;

            # Push the stream to the local HLS application
            push rtmp://127.0.0.1:1935/hls;

            # The on_publish callback will redirect the RTMP
            # stream to the streamer's username, rather than their
            # secret stream key.

            # change HOST to be 127.0.0.1:(django port) if you're doing this without server blocks
            on_publish http://HOST/start_stream;
            on_publish_done http://HOST/stop_stream;
        }

        application hls {
            live on;

            # Only accept publishing from localhost.
            # (the `app` RTMP ingest application)
            allow publish 127.0.0.1;
            deny publish all;
            deny play all;

            # Package streams as HLS
            hls on;
            hls_path /var/www/live;
            hls_nested on;
            hls_fragment_naming system;
            hls_datetime system;
        }
    }
}
```