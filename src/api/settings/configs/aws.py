from api.settings import env

AWS_REGION_NAME = env.str("AWS_REGION_NAME", default="")
AWS_BUCKET_NAME = env.str("AWS_BUCKET_NAME", default="")
