def load_plugins(mode="1"):
    if mode == "1":
        return [
            "elementor", "contact-form-7", "woocommerce",
            "wp-file-manager", "wordfence", "yoast-seo"
        ]
    elif mode == "2":
        with open("data/plugins.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    elif mode == "3":
        raw = input("Enter plugin names comma separated: ")
        return [x.strip() for x in raw.split(",")]
    return []