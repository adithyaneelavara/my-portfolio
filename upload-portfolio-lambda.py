import boto3
import botocore
import zipfile
import io
import mimetypes

def lambda_handler(event, context):


	s3 = boto3.resource('s3')
	sns = boto3.resource('sns')
	topic = sns.Topic('arn:aws:sns:eu-west-1:945746314187:Deploy_Portfolio_Notification')

	try:
		bucket = s3.Bucket('home.adithyaneelavara.info')
		build_bucket = s3.Bucket('build.adithyaneelavara.info')
		    
		portfolio_zip = io.BytesIO()
		build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)
		    
		with zipfile.ZipFile(portfolio_zip) as myZip:
			for nm in myZip.namelist():
				obj= myZip.open(nm)
				bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
				bucket.Object(nm).Acl().put(ACL='public-read')
		topic.publish(Subject="Portfolio Build Success!!",Message='Portfolio was  deployed succesfully!!')
	except:
		topic.publish(Subject="Portfolio Build Failed!!",Message='Portfolio was not deployed succesfully!!')
		raise		
	return "Job Done!"