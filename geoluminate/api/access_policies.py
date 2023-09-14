from rest_access_policy import AccessPolicy

# Principal: *, admin, staff, authenticated, anonymous, group:name, id:id


class CoreAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["<safe_methods>"], "principal": ["authenticated", "anonymous"], "effect": "allow"},
        {
            # "action": ["*"],
            "action": ["<safe_methods>"],
            "principal": ["admin", "staff", "group:Reviewer"],
            "effect": "allow",
        },
    ]
