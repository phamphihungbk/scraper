## Python Scrapper

Small scrapping script to extract data from FIT.

### Guideline:

Firstly, you need to run `make` to build and create docker instance. After docker instace is ready, then access 
into `scrapper-python` instance by using this command `docker exec -it scrapper-python bash`. Let's say you want to 
get number of facebook fanpage so just need to run `python3 Facebook_Scrape_v3.py` on `scrapper-python` instance. 
All commands were attached into `Makefile`

### Folder Structure

```bash
├── environment                # contains dockerfile
├── results                    # end result folder
└── src                        # main source code
```
