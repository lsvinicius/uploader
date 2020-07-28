This project was made as an effort of mine to learn the basics
of docker.

The project consists of a backend where text files are uploaded and backend
sends the files to a storage server. The file size limit is 15MB.

Both backend and storage are supposed to run in the same host machine, in the same
docker network, however, this is not mandatory.

### Get containers up and running 

In order to run the application in containers, you first need to install [Docker].

#### Build images
Project Dockerfile contains three images `base`, `stg` and `prod`.
`base` image is supposed to be used by `stg` and `prod` images.

To build images, go to the root folder of the project and type the following:
```
# build stg image
docker build -t uploader-stg:latest --target stg .

# build prod image
docker build -t uploader-prod:latest --target prod .
```

#### Create network

The backend searches for `storage` node in the network in order to save the files.

Since default docker bridge network does not support name resolution, there also some security related concerns
and it is legacy, we will use a user-defined bridge network.

```
# create docker network
docker network create -d bridge uploader-net
```

For more info about bridge networks, see [here][bridge-networks].

#### Create containers

Now that images and network are created, we just need to create the containers:

```
#create stg container
docker run -d --publish 8000:8000 --name backend-stg --network uploader-net -v uploader-stg-vol:/home/uploader_app/.uploader  uploader-stg

#create prod container
docker run -d --publish 9000:8000 --name backend-prod --network uploader-net -v uploader-prod-vol:/home/uploader_app/.uploader uploader-prod

#create storage container
docker run -d --publish 27017:27017 --name storage --network uploader-net mongo
```

### Configuring application
You may change application configuration by changing the values in the `dev.py`, 
`prod.py` or `stg.py` files located in config folder.

Note however that `dev.py` is for host machine and `prod.py` do not
have `PORT` variable because this is set in `Dockerfile`.

[Docker]: https://docs.docker.com/engine/install/

[bridge-networks]: https://docs.docker.com/network/bridge/