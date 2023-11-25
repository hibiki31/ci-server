# ci-server

gh webhook forward --repo=hibiki31/virty --events=EVENTS --url=http://localhost:8000/gh/virty

```
type -p curl >/dev/null || (apt update && apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& apt update \
&& apt install gh -y
```


gh webhook forward --repo=hibiki31/virty --events=pull_request,push --url=http://localhost:8000/gh/virty


```
curl -d @dump/2023-1125-153046.json -H "Content-Type: application/json" http://localhost:8000/gh/virty
```