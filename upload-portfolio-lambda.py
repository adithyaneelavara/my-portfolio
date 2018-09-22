import boto3
import botocore
import zipfile
import io
import mimetypes

def lambda_handler(event, context):


	s3 = boto3.resource('s3')
	sns = boto3.resource('sns')
	topic = sns.Topic('arn:aws:sns:eu-west-1:945746314187:Deploy_Portfolio_Notification')
	location={
		"bucketName":'build.adithyaneelavara.info',
		"objectKey":'portfoliobuild.zip',
	}
	try:
		job = event.get('CodePipeline.job')
		
		if job:
			for artifact in job['data']['inputArtifacts']:
				if artifact['name'] =='MyAppBuild':
					location = artifact['location']['s3Location']
		
		print (f'Building Portfolio from Location:{location}')
		
		bucket = s3.Bucket('home.adithyaneelavara.info')
		build_bucket = s3.Bucket(location['bucketName'])
		    
		portfolio_zip = io.BytesIO()
		build_bucket.download_fileobj(location['objectKey'],portfolio_zip)
		    
		with zipfile.ZipFile(portfolio_zip) as myZip:
			for nm in myZip.namelist():
				obj= myZip.open(nm)
				bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
				bucket.Object(nm).Acl().put(ACL='public-read')
		topic.publish(Subject="Portfolio Build Success!!",Message='Portfolio was  deployed succesfully!!')
		if job:
			codepipeline = boto3.client('codepipeline')
			codepipeline.put_job_success_result(jobId=job['id'])
	except:
		topic.publish(Subject="Portfolio Build Failed!!",Message='Portfolio was not deployed succesfully!!')
		if job:
			codepipeline = boto3.client('codepipeline')
			codepipeline.put_job_failure_result(jobId=job['id'])
		raise		
	return "Job Done!"