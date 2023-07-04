# DockMaven (dmvn)

DockMaven provides solution for simplify usage maven with docker container "maven-builder-*"
It is well-designed to work with PocketEngine project.

### Usage: 
```bash
dmvn [arguments...]|[list]
```

### OptionContext:
- `list *`               - prints configuration from selected package, to print every package separated use additional argument `-f`

### Arguments:
- `--help|help|-?`       - print help info and exit
- `--version|version|-v` - print version info and exit
- `--mvn-projects-dir`   - print maven project configuration path variable and exit
- `--project`            - select maven project configuration path notice that configuration will not be applied only for selected package but every package starting from "projects/" directory to selected path 
- `--mvn-clean`          - clean project scr before execution
- `--package`            - pdocker image package
- `--app-name`           - pdocker image name
- `--src-path`           - project scr path
- `--mvn-image-name`     - image name of maven builder
- `--mvn-container-env-app-name`       - target file name (in target directory)
- `--mvn-container-env-target-dir`     - target path (subdirectory of src)
- `--mvn-container-env-build-cmd`      - maven build command
- `--mvn-container-env-build-profiles` - maven profiles

## Example project structure

- `/$DMVN_PROJECTS_DIR`
  - `/projects`
    - `/package` (example file with single line value overrides argument `--package` with example value "my/package")
    - `/project-path`
      - `/to`
        - `/project1`
          - `/app-name` (example file with single line value overrides argument `--app-name` with example value "my-app")
          - `/mvn-image-name` (example file with single line value overrides argument `--mvn-image-name` with example value "maven-builder-jdk-17")
        - `/project2`
          - `/package` (example file with single line value overrides argument `--package` with example value "other/package")
          - `/app-name` (example file with single line value overrides argument `--app-name` with example value "my-app2")

Now if we use command:
```bash
dmvn --project project-path/to/project1 --project project-path/to/project2 --project project-path/to --mvn-image-name maven-builder-jdk-8
```
Script will perform 3 maven processes, each with arguments for:
- first process
  - `--package my/package` from file `/$DMVN_PROJECTS_DIR/projects/package`
  - `--app-name my-app` from file `/$DMVN_PROJECTS_DIR/projects/project-path/to/project1/app-name`
  - `--mvn-image-name maven-builder-jdk-17` from file `/$DMVN_PROJECTS_DIR/projects/project-path/to/project1/mvn-image-name`
- second process
  - `--package other/package` from file `/$DMVN_PROJECTS_DIR/projects/project-path/to/project2/package`
  - `--app-name my-app2` from file `/$DMVN_PROJECTS_DIR/projects/project-path/to/project2/app-name`
  - `--mvn-image-name maven-builder-jdk-8` from command line
- third process
  - `--package my/package` from file `/$DMVN_PROJECTS_DIR/projects/package`
  - `--mvn-image-name maven-builder-jdk-8` from command line
