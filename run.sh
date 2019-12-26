netconvert --osm-files map.osm -o test.net.xml
python randomTrips.py -n test.net.xml -r test.rou.xml -p 0.5