# cdepviz
Visualize dependencies in a C/C++ project.
cdepviz creates a directed graph based on a set of files and `#include` directives in those files, and outputs a **.dot** file for rendering with Graphviz.  

## Usage
```bash
ruby cdepviz.rb # Look for files in working directory
```
```bash
ruby cdepviz.rb src/ # Look for files in src/
```
## Options
* `-e` / `--exclude`: Exclude directory from search
* `-o` / `--output`: Output file
## Example
![Example](./example.png)