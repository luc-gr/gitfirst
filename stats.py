import os

from pandas_datapackage_reader import read_datapackage

from util import *

def update_stats():
    data = read_datapackage("data")
    filters = data['filters']
    filename = os.path.join('data', filters._metadata['path'])
    images = data['images']

    # Apply stats
    images.fillna('', inplace=True)
    # print(images.head)
    filters.dropna(subset=['Code', 'Column'], inplace=True)
    # print(filters.head)

    filters['Count'] = filters.apply(
        lambda row: (
            (row['Code'] == '.*' and len(
                images.loc[
                    images[row['Column']].str.len() > 0
                ]
            )) or len(
                images.loc[
                    images[row['Column']].str.match('^' + row['Code'] + '$', case=True) |
                    images[row['Column']].str.contains(' ' + row['Code'] + ' ') |
                    images[row['Column']].str.match('^' + row['Code'] + '[ |,]', case=True) |
                    images[row['Column']].str.endswith(' ' + row['Code'])
                ]
            )
        ), axis = 1
    )

    print(filters.head(n=50))

    print("Writing to %s" % filename)
    filters.to_csv(filename, index=False)


if __name__ == '__main__':
    update_stats()
