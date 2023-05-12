COMMUNITY_TYPES = (
    ("public", "Public"),
    ("restricted", "Restricted"),
    ("private", "Private"),
)

COLOR_CHOICES = (
    ("primary", "Primary"),
    ("orange", "Orange"),
    ("red", "Red"),
    ("pink", "Pink"),
    ("teal", "Teal"),
    ("green", "Green"),
    ("indigo", "Indigo"),
    ("grey", "Grey"),
    ("deep-purple", "Purple"),
    ("amber", "Amber"),
)

PUBLICATION_TYPE_CHOICES = (
    ("editor", "Editor"),
    ("media", "Media"),
    ("link", "Link"),
    ("poll", "Poll"),
)

REPORT_STATES = (
    ("pending", "Pending"),
    ("resolved", "Resolved"),
    ("ignored", "Ignored"),
)

RESOLVE_REPORT_STATES = (
    ("resolved", "Resolved"),
    ("ignored", "Ignored"),
)

MOD_CHOICES = (
    ("mod", "Moderator"),
    ("sub", "Sub Moderator"),
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("NB", "Non-Binary"),
    ("C", "I Refer To Myself As..."),
    ("XY", "I Prefer Not To Say"),
)

BAN_ITEM_MODEL_CHOICES = (
    ("publication", "publication"),
    ("comment", "comment"),
    ("profile", "profile"),
    ("community", "community"),
)
BAN_ITEM_APP_LABEL_CHOICES = (
    ("publication", "publication"),
    ("comment", "comment"),
    ("account", "account"),
    ("community", "community"),
)
