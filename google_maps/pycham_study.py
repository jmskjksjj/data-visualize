gmap_keys = "AIzaSyCJjpyQ1_1dhC_IyXeS3Gg_BCckVmcuYx8"
import googlemaps
gmaps = googlemaps.Client(key=gmap_keys)
tmp = gmaps.geocode("서울영등포경찰서", language="ko")
tmp[0]["formatted_address"].split()[2]
tmp