import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import time
from helpers.log import Log
from random import randint
from pprint import pprint


logger = Log(__file__).logger()


class Telegraf2Wavefront(object):

  def __init__(self):
    self.filePath = 'metrics.out'
    self.s3Bucket = 'intu-oim-dev-ihp-01-us-west-2'

  def readFile(self):
    with open(self.filePath, 'r') as fh:
      data = fh.read()
    lines = data.split('\n')
    return lines

  def run(self):
    lines = self.readFile()
    lines = lines[:10]
    data = '\n'.join(lines) + '\n'
    print(data)
    s3Client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    epochRandom = str(int(time.time())) + str(randint(1, 9000))
    s3Response = s3Client.put_object(Body=data, Bucket=self.s3Bucket, Key=epochRandom, ACL="bucket-owner-full-control")
    pprint(s3Response)
    logger.info('S3 Response: {}'.format(s3Response))
    return None



if __name__ == '__main__':
  logger.info('STARTED')
  try:
    T = Telegraf2Wavefront()
    T.run()
    msg = 'PROGRAM COMPLETED'
    print(msg)
    logger.info(msg)
  except:
    msg = 'PROGRAM FAILED'
    print(msg)
    logger.critical(msg, exc_info=True)
  logger.info('Done.')