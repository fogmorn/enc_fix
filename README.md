# enc_fix
Checks that file is `UTF-8` encoded and fix it if not.

If file isn't in `UTF-8` or partitly, script converts file using `ex` (vim) editor.

You may see results in `pre-commit.git.log` file.

## Dependencies
- `Vim` editor (may it better to use `iconv`).

## Usage
Simply put this script in project root folder and run folloing:
```
./enc_fix.git.py "`find . -type f -print | egrep -v '\.git|mp3|<file_extension_to_exclude>'`" > enc_fix.git.log
```
