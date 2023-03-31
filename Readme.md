### Simplest GPT Chat-bot Proxy

To run it you have to create `.env` file with variables like in `.env.example`

#### Run localy:
```bash
#Install dependencies
pip install -r rq.txt

#Run
python main.py
```

#### Run with docker:
```bash
#Build image
docker build .

#Run container
docker run --rm -d <IMAGE_HASH>
