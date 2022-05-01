

class Geometry:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return str(self.lat) + "," + str(self.lng) + "\n"

    def get_latlng(self):
        return self.lat, self.lng

    def get_json(self):
        return {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [self.lat, self.lng]},
         "properties": {}
         }


class ProcessFile:

    def __init__(self, filename, write=True):
        self.filename = filename
        self.file = open(filename, "a") if write else open(filename, "r")

    def add_geometry_to_file(self, geometry):
        self.file = open(self.filename, "a")
        self.file.write(str(geometry))
        self.close_file()

    def close_file(self):
        self.file.close()

    def get_geometry_from_file(self, input_file_path):
        geometry_list = []
        with open(input_file_path, "r") as fp:
            lines = fp.readlines()
            for line in lines:
                coordinates = line.strip().split(",")
                print ("getting_coordinates", coordinates)
                lat, lng = float(coordinates[0]), float(coordinates[1])
                g = Geometry(lat, lng)
                geometry_list.append(g)
        return geometry_list









