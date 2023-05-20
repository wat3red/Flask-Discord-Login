import json5


class Settings:
    __slots__ = ("DISCORD_CLIENT_ID", "DISCORD_CLIENT_SECRET", "DISCORD_REDIRECT_URI")

    def handle_error(self, exc):
        print(exc)
        exit(-1)

    def __init__(self):
        try:
            settings_file = "config.json"
            user_settings = json5.load(open(settings_file))

            for user_setting_key in user_settings:
                setattr(self, user_setting_key, user_settings[user_setting_key])

        except IndexError as exc:
            self.handle_error(f"Provide config name. Exception: {exc}")
        except FileNotFoundError as exc:
            self.handle_error(f"File not found. Exception: {exc}")
        except json5.JSONDecodeError as exc:
            self.handle_error(f"Json error. Exception: {exc}")
        except AttributeError as exc:
            self.handle_error(f"No setting available. Exception: {exc}")
