import os
import prepenv

SPIDERS_RESULTS_SUCCESSFUL_JSON_FOLDER = os.path.join(prepenv.MANGA_SPIDERS_DATA, 'results_successful')

SPIDERS_JSON_FILE_PATHS = []

dir_contents = os.listdir(SPIDERS_RESULTS_SUCCESSFUL_JSON_FOLDER)

for x in range(len(dir_contents)):
    if dir_contents[x] == 'processed':
        continue
    else:
        SPIDERS_JSON_FILE_PATHS.append(os.path.join(
            SPIDERS_RESULTS_SUCCESSFUL_JSON_FOLDER, dir_contents[x]
        ))
