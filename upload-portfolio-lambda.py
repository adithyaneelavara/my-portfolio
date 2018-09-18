import boto3
import botocore
import zipfile
import io
import mimetypes

s3 = boto3.resource('s3')
bucket = s3.Bucket('home.adithyaneelavara.info')
build_bucket = s3.Bucket('build.adithyaneelavara.info')

portfolio_zip = io.BytesIO()
build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myZip:
	for nm in myZip.namelist():
		obj= myZip.open(nm)
		bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
		bucket.Object(nm).Acl().put(ACL='public-read')

