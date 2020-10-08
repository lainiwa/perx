from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="PERX",
    settings_files=['settings.toml', '.secrets.toml'],
)
