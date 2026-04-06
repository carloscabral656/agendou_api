class UserController:
    def __init__(self, create_user_use_case):
        self.create_user_use_case = create_user_use_case

    def create_user(self, payload: dict):
        user = self.create_user_use_case.execute(
            name=payload["name"],
            email=payload["email"]
        )
        return {"name": user.name, "email": user.email}