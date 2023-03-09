# wmrecg
西瓜新鮮度辨識 (flutter + flask + docker)
```
docker build -t wmrecg .
docker stop wmrecgct
docker run -d -p 40250:40250 --mount type=bind,source=/home/mi2s/JiaDian/wmrecg/backend/wav,target=/app/wav --name wmrecgct wmrecg
```

