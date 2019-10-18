import csv
from app.engine.data import canada_provinces_mapping, country_mapping

class Parser:
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def parse_tsv(filepath):
        city_data = {}
        with open(filepath, encoding="UTF-8") as tsvfile:
            reader = csv.DictReader(tsvfile, 
                dialect="excel-tab", delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                city_data[int(row['id'])] = {}
                city_data[int(row['id'])]['name'] = row['name']
                city_data[int(row['id'])]['alt_name'] = row['alt_name']
                city_data[int(row['id'])]['lat'] = row['lat']
                city_data[int(row['id'])]['long'] = row['long']
                city_data[int(row['id'])]['country'] = country_mapping[row['country']]
                if row['country'] == "CA":
                    city_data[int(row['id'])]['admin1'] = \
                        canada_provinces_mapping[row['admin1']]
                else:
                    city_data[int(row['id'])]['admin1'] = row['admin1']

        return city_data

    def run(self):
        ext = self.filepath.split('.')[-1] 
        if ext == 'tsv':
            return self.parse_tsv(self.filepath)
        else:
            Exception('Extension `{}` not implemented in Parser'.format(ext))
