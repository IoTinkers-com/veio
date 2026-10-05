import re
import urllib.request

url = ("https://cmr.earthdata.nasa.gov/search/granules.echo10"
       "?short_name=VNP46A3&temporal=2025-08-01T00:00:00Z/2025-08-28T23:59:59Z"
       "&bounding_box=-73.5,0.5,-59.5,12.5&page_size=100")
body = urllib.request.urlopen(url, timeout=60).read().decode()
pairs = re.findall(r"VNP46A3\.(A\d{7})\.(h\d+v\d+)\.\d+\.[^\"<>]*?\.h5", body)
print("granules:", len(pairs), "| tiles:", sorted(set(t for _, t in pairs)))
print("dates:", sorted(set(d for d, _ in pairs)))
