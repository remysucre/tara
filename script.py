import os


def get_max_values(tns_file_name: str):
    max_indices = None

    with open(tns_file_name, mode='r') as tns_file:
        for line in tns_file.readlines():
            indices = [int(v) for v in line.split()[:-1]]
            if not max_indices:
                max_indices = indices
            else:
                for i in range(len(indices)):
                    max_indices[i] = max(max_indices[i], indices[i])
    
    print(tns_file_name)
    print(max_indices)

files = ['aka_name.tns', 'aka_title.tns', 'cast_info.tns', 'char_name.tns', 'company_type.tns', 'info_type.tns', 'movie_companies.tns', 'movie_info_idx.tns', 'title.tns']
for fi in files:
    get_max_values(os.path.join('imdb_tns', fi))
