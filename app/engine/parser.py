import csv

class Parser:

    canada_provinces_mapping = {
        "01": "AB",
        "02": "BC",
        "03": "MB",
        "04": "NB",
        "05": "NL",
        "07": "NS",
        "08": "ON",
        "09": "PE",
        "10": "QC",
        "11": "SK",
        "12": "YT",
        "13": "NT",
        "14": "NU"
    }

    country_mapping = {
        "CA": "Canada",
        "US": "USA"
    }

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
                city_data[int(row['id'])]['country'] = self.country_mapping[row['country']]
                if row['country'] == "CA":
                    city_data[int(row['id'])]['admin1'] = \
                        self.canada_provinces_mapping[row['admin1']]
                else:
                    city_data[int(row['id'])]['admin1'] = row['admin1']

        return city_data

    def run(self):
        ext = self.filepath.split('.')[-1] 
        if ext == 'tsv':
            return self.parse_tsv(self.filepath)
        else:
            Exception('Extension `{}` not implemented in Parser'.format(ext))
