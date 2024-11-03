import reflex as rx

class HacktxConfig(rx.Config):
    pass

config = HacktxConfig(
    app_name="hacktx_24",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)