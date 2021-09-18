# Test cases for anyconfig\_cli

- 10.json + o/10.json: no args, no options
- 20.json + o/20.json: no args, an wrong option
- 30.json + o/30.json: an input with unknown file type, no options
- 40.json + o/40.json: an input with unknown file type, an -I (input type) option gives an unknown file type
- 50.json + o/50.json: an input with known file type, an -o option gives file with known file type and an -O (output type) option gives an unknown file type
