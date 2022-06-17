import gpxpy

# This class mainly converts GPX files to CSV in the format: time in milliseconds, exact time, latitude, longitude
# Other reusable methods include parsing GPX files, gpx to list, time difference between two GPX points in ms 

class GPX_to_CSV:
    def __init__(self, gpx_file):
        self.gpx_file = gpx_file

    # parse gpx file
    def read_gpx(self, filename):
        gpx_file = open(filename, 'r')
        gpx = gpxpy.parse(gpx_file)
        return gpx

    # get time difference in ms between two gpx points
    def get_time_diff(self, point1, point2):
        time1 = point1.time
        time2 = point2.time
        time_diff = time2 - time1
        return time_diff.total_seconds() * 1000

    # get gpx file to a list of lists of lat, lng, time, timestamp
    def gpx_to_list(self):
        gpx = self.read_gpx(self.gpx_file)
        gpx_list = []
        temp = None
        time = 0  # in ms
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if not temp:
                        gpx_list.append(
                            [time, point.time, point.latitude, point.longitude])
                    else:
                        time += self.get_time_diff(temp, point)
                        gpx_list.append(
                            [time, point.time, point.latitude, point.longitude])
                    temp = point
        return gpx_list

    # make a csv file with time, timestamp, latitude, longitude
    def list_to_csv(self, f):
        f.write('relative_timestamp,timestamp,lat,lng\n')
        for item in self.gpx_to_list():
            f.write(str(item[0]) + ',' + str(item[1]) + ',' +
                    str(item[2]) + ',' + str(item[3]) + '\n')

    # creates the csv file
    def convert(self, filename):
        # create a csv file with the fileame
        with open(f"{filename}.csv", 'w') as f:
            self.list_to_csv(f)


GPX_to_CSV('test.gpx').convert('new_csv')
