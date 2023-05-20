from models.info import Info


class AccManager:
    status_info = {
        "-1": "Administrator",
        "0": "Not confirmed by Discord",
        "1": "Confirmed by Discord",
    }

    def __init__(self, app, discord):
        self.discord = discord
        self.app = app

    def check_if_admin(self):
        '''
        Checks, if current user is admin
        '''
        current_user = self.get_current_user()
        user_id = current_user.get("id")
        status = self.get_status(user_id)

        return status == -1

    def get_user_from_database(self, id):
        return Info.query.filter_by(id=id).first()

    def get_status(self, user_id):
        user_id = int(user_id)
        user = self.get_user_from_database(id=user_id)

        return user.status if user else None

    def get_current_user(self):
        user = self.discord.fetch_user()

        is_verified = 1 if user.verified else 0

        id, email, name, avatar = (
            user.id,
            user.email,
            f"{user.name}#{user.discriminator}",
            user.avatar_url or user.default_avatar_url,
        )

        result = {
            "id": id,
            "email": email,
            "name": name,
            "avatar": avatar,
            "is_verified": is_verified,
        }

        return result

    def get_users(self):
        return [user for user in Info.query.all()]
