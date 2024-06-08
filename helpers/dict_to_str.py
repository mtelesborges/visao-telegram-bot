from typing import Dict


def dict_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [
        f"{key}: {value}"
        for key, value in user_data.items()
        if key not in ["texto_foto"]
    ]
    return "\n".join(facts).join(["\n", "\n"])
