# To run this app:
```
docker network create app-network
```

```
docker rm app-container
docker build -t app-image .
docker run --net app-network -p 8000:8000 --name app-container app-image
```

```
docker rm text-container
docker build -t text-image .
docker run --net app-network -p 8001:8001 --name text-container text-image
```

```
docker rm video-container
docker build -t video-image .
docker run --net app-network -p 8002:8002 --name video-container video-image
```