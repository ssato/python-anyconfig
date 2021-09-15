# Test cases for anyconfig\_cli

- 10.json + o/10.json: an input with known file type, without any options to load, and dump to a JSON file without any output options
- 20.conf + o/20.json: an input with unknown file type and an "-I json" option to load, and dump to a JSON file without any output options
- 30.json + o/30.json: an input with unknown file type and an "-I json" option to load, and dump to a JSON file without '.json' file extension with "-O json" option
