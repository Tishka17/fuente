### Fuente

Config loading library with multiple sources

Features:

* Well-known sources
* Custom values merging rules
* Loading into clean dataclasses

### Quick start

1. Create classes for your config

```python
from dataclasses import dataclass


@dataclass
class Config:
    value: str
```

2. Import required config source

```python
from fuente.sources.env import EnvSource
```

3. Create config loader providing source and config type.

```python
from fuente.make_loader import config_loader

loader = config_loader(EnvSource(prefix="MYAPP"), config=Config)
```

4. Load data

```python
config = loader.load()
```

### Running example

```shell
pip install .

cd example
export MYAPP_DATABASE_URI="sqlite:///"
python example.py --blacklist=x,y
```

### Customization

1. You can provide custom merging rules based on adaptix predicates. 
They make sense once you have multiple sources.
```python
loader = config_loader(
    EnvSource(prefix="MYAPP_"),
    ArgParseSource(parser=arg_parser),
    recipe=[
        merge(P[Config].log_level, UseFirst()),
        merge(P[Config].blacklist, Unite()),
    ],
    config=Config,
)
```

2. Set error handling mode. You can skip unparsed fields, the whole source if it has errors of fail. Use `error_mode` argument

3. Configure each source. Depenging on type, you can pass additional arguments to each config source. It can be prefix/separator or additional parsing rules
