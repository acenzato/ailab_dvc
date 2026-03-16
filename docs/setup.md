Create a new empty [uv](https://docs.astral.sh/uv/) project. 

```bash
uv init <project-name>
```

Having a `src` directory where all code will be placed is recommended.

```bash
cd <project-name>
mkdir src
mv main.py src/main.py
```

## DVC Setup

Now let's setup `dvc`.
First we need to install it. On linux the recommended way to do it is to install it in your project's venv. This keeps the python, dvc and all other packages versions in sync.

```bash
uv add dvc
```

> **NOTE:** if you are using a remote storage like AWS S3 or Azure Blob Storage you need to install the extra features for DVC: `uv add dvc[s3]` or `uv add dvc[azure]`

Now activate the virtual environment and initialize the DVC repo

```bash
source .venv/bin/activate
dvc init
```

> **NOTE for Windows users:** to activate the venv in Windows the command is slightly different: `.venv\Scripts\activate`

DVC has now created a `.dvc` directory where its cache and configuration files will be stored

### Git Hooks
We like to have fine-grained control over our project but we don't like to have silent data errors and version mismatches. So we let DVC install some [git hooks](https://git-scm.com/book/ms/v2/Customizing-Git-Git-Hooks). This tells git to execute some DVC actions automatically every time we perform a git action like `checkout`, `push` or `pull`. It essentially allows git to auto-execute all DVC commands necessary to sync the data on your filesystem with the metadata tracked by git.

```bash
dvc install
dvc config core.autostage true
```

### DVC remote configuration
DVC needs a remote storage where data will be persisted. This enables to:
- share data with other people
- have data available wherever you are
- **huge** storage space
- 11 9s durability

As an example let's add an S3 remote storage:
```bash
dvc remote add <name> <s3://bucket-name/path/to/data/storage>
dvc remote default <name>
```
Each remote should be given a name. It is recommended not to put DVC data in the root of the bucket. If need arises to place other stuff in the bucket you would mix it up with DVC data. It is possible to migrate the data storage but it breaks hitory and reproducibility so try to avoid it.
```
