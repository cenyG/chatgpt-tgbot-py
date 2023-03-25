### Simplest GPT Chat-bot Proxy

#### Shortcuts:
```bash
#Build image
docker build .

#Run container
docker run --rm -d <IMAGE_HASH>

#Run for testing
docker run -it --rm --entrypoint bash <IMAGE_HASH>

#Docker rm all containers
docker rm $(docker ps -aq)
```