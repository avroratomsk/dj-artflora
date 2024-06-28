INSTALLED_APPS = [
    # "django.contrib.admin",
    "admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'ckeditor',
    'ckeditor_uploader',
    "debug_toolbar",
    'sorl.thumbnail',
    "home",
    "shop",
    "users",
    "reviews",
    "service",
    "cart",
    "order",
    "payment",
    "coupons",
    'allauth',
    'allauth.account',
    "favorites",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "artflora",
        "USER": "artflora",
        "PASSWORD": "1111",
        "HOST": "localhost",
        "PORT": "5432",
    }
}