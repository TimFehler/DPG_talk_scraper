# DPG talk scraper

- Scrape contributions by your research group from the DPG Verhandlungen website (https://www.dpg-verhandlungen.de)
- Serialize them to a YAML file
- Produce HTML elements (e.g. table) via a template from the intermediate YAML file, to publish them on your own static site, including links to the original online presence 

## Instructions 

To scrape the website you run
```bash
python3 talk_scraper.py
```

To produce HTML elements from the scraped talks you run
```bash
python3 talk_formater.py
```

---

The file `config.yml` is used to configure both the scraping and creation of HTML elements. Talks are scraped from search results for a specific conference. To control the query, you provide the base link of the search and the query strings:

`config.yml`:
```yaml
DPG24:
  title: Karlsruhe 2024
  url: https://www.dpg-verhandlungen.de/year/2024/conference/karlsruhe/search
  query_strings: [test]
  output_file: talks/dpg24.yml
```

Duplicates are removed on the basis of the abstract link as a unique identifier of the contribution, so it is possible to use several names to search for contributions. It should be sufficient for instance to use a query combination like `[location+name1, location+name2, location+name3]` to find all contributions of your group, replacing `location` with the city of your institute.

Multiple words used in a search are combined in a *AND* combination with a `+`, for *OR* combination make use of the multiplicity of query strings. **Important:** Query strings cannot contain empty spaces or special characters.

Should you want to make modifications, for instance, to the title or author list of individual contributions, you can edit the intermediate YAML file produced by the scraper, which is stored in `talks/` (or wherever you specified it in the config file).

## Dependencies

Install all necessary dependencies with 
```
pip install -r requirements.txt
```

## Author

2025-01: Tim Fehler