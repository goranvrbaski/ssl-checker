# SSL expiration date checker

## Requirements
- Python 3.6

or just Docker :)


## Usage 

Example usage of SSL expiration date checker

```bash
python app.py --help

positional arguments:
  domains               domain names

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS, --days DAYS  number of days

```


### Python
```bash
python app.py google.com,yahoo.com -d 65
```

### Docker

```bash 
docker run goranvrbaski/ssl-checker google.com,yahoo.com -d 65
```

### Example output
```bash
python app.py google.com,yahoo.com -d 65 
2019-05-06 21:01:54,986 | WARNING | google.com expires in 63 days(s)
2019-05-06 21:01:55,477 | INFO | yahoo.com expires in 174 days(s)

```

- WARNING - ssl certificate is hitting threshold and needs renewal
- INFO - ssl certificate is not hitting threshold
- ERROR - error occured while checking ssl certificate