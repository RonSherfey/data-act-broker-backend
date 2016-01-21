from datetime import datetime, timedelta
import boto
import os
import inspect
import json
from boto import sts

class s3UrlHandler:
    """
    This class acts a wrapper for S3 URL Signing
    """
    BASE_URL = "https://s3.amazonaws.com/"
    ENABLE_S3 = True
    URL_LIFETIME = 2000
    STS_LIFETIME = 2000
    S3_ROLE = ""
    def __init__(self,name = None):
        """
        Creates the object for signing URLS

        arguments:
        name -- (String) Name of the S3 bucket
        user -- (int) User id folder of S3 bucket

        """
        if(name == None):
            self.bucketRoute = s3UrlHandler.getValueFromConfig("bucket")
        else:
            self.bucketRoute = name
        s3UrlHandler.S3_ROLE = s3UrlHandler.getValueFromConfig("role")

    def _signUrl(self,path,fileName,method="PUT") :
        """
        Creates the object for signing URLS

        arguments:

        fileName -- (String) File name of file to be uploaded to S3.

        returns signed url (String)

        """
        if(s3UrlHandler.ENABLE_S3) :
            s3connection = boto.connect_s3()
            if(method=="PUT") :
                return s3connection.generate_url(s3UrlHandler.URL_LIFETIME, method, self.bucketRoute, "/"+path+"/" +fileName,headers={'Content-Type': 'application/octet-stream'})
            return s3connection.generate_url(s3UrlHandler.URL_LIFETIME, method, self.bucketRoute, "/"+path+"/" +fileName)
        return s3UrlHandler.BASE_URL + "/"+self.bucketRoute +"/"+path+"/" +fileName

    def getSignedUrl(self,path,fileName,method="PUT"):
        """
        Signs a URL for PUT requests

        arguments:
        fileName -- (String) File name of file to be uploaded to S3.

        returns signed url (String)
        """
        if(method=="PUT"):
            self.s3FileName = s3UrlHandler.getTimeStampedFilename(fileName)
        else:
            self.s3FileName = fileName
        return self._signUrl(path,self.s3FileName, method)

    @staticmethod
    def getTimestampedFilename(filename) :
        """
        Gets a Timestamped file name to prevent conflicts on S3 Uploading
        """
        seconds = int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())
        return str(seconds)+"_"+fileName

    @staticmethod
    def gettValueFromConfig(value):
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        bucketFile = open(path+"/s3bucket.json","r").read()
        bucketDict = json.loads(bucketFile)
        return bucketDict[value]


    @staticmethod
    def getS3RolefromConfig():
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        bucketFile = open(path+"/s3bucket.json","r").read()
        bucketDict = json.loads(bucketFile)
        return bucketDict["bucket"]

    @staticmethod
    def doesFileExist(filename):
        """ Returns True if specified filename exists in the S3 bucket """
        # Get key
        s3connection = boto.connect_s3()
        bucket = s3connection.get_bucket(s3UrlHandler.getBucketNameFromConfig())
        key = bucket.get_key(filename)
        if(key == None):
            return False
        else:
            return True

    def getTemporaryCredentials(self,user):
        """
        Gets token that allows for S3 Uploads for seconds set in STS_LIFETIME
        """
        stsConnection = boto.connect_sts()
        role = stsConnection.assume_role(s3UrlHandler.S3_ROLE,"FileUpload"+str(user) duration_seconds=s3UrlHandler.STS_LIFETIME)
        credentials ={}
        credentials["AccessKeyId"] =  role.access_key
        credentials["SecretAccessKey"] = role.secret_key
        credentials["SessionToken"] = role.session_token
        return credentials

    @staticmethod
    def getFileSize(filename):
        """ Returns file size in number of bytes for specified filename, or False if file doesn't exist """

        # Get key
        s3connection = boto.connect_s3()
        bucket = s3connection.get_bucket(s3UrlHandler.getBucketNameFromConfig())
        key = bucket.get_key(filename)
        if(key == None):
            return False
        else:
            return key.size
