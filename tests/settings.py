SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_standardized_responses",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
ROOT_URLCONF = 'tests.urls'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'drf_standardized_responses.renderers.StandardResponseRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'drf_standardized_responses.pagination.StandardPagination',
    'EXCEPTION_HANDLER': 'drf_standardized_responses.exceptions.standardized_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
