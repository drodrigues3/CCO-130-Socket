curl 'https://c.tile.openstreetmap.org/4/4/7.png' \
  -H 'dnt: 1' \
  -H 'accept-encoding: gzip, deflate, br' \
  -H 'accept-language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'\
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36' \
  -H 'accept: image/webp,image/apng,image/*,*/*;q=0.8' \
  -H 'referer: https://www.openstreetmap.org/' \
  -H 'authority: c.tile.openstreetmap.org' \
  -H 'cookie: _osm_totp_token=778467' \
  --compressed
