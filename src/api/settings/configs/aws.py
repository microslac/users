from api.settings import env

AWS_REGION_NAME = env.str("AWS_REGION_NAME", default="")
AWS_BUCKET_NAME = env.str("AWS_BUCKET_NAME", default="")
AWS_BUCKET_KEY_ID = env.str("AWS_BUCKET_KEY_ID", default="")
AWS_BUCKET_KEY_SECRET = env.str("AWS_BUCKET_KEY_SECRET", default="")
AWS_BUCKET_URL = env.str("AWS_BUCKET_URL", default="")
