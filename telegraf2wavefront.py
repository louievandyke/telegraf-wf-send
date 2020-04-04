import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import time, json
from helpers.log import Log
from random import randint
from pprint import pprint


logger = Log(__file__).logger()


class Telegraf2Wavefront(object):

  def __init__(self):
    self.filePath = '/tmp/metrics.out'
    self.s3Bucket = 'intu-oim-prd-ihp-01-us-west-2'
    self.s3Client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

  def readFile(self):
    with open(self.filePath, 'rb') as fh:
      data = fh.read().decode('ascii')
    lines = data.split('\n')

    currentLines = [] # THIS WILL ADD CURRENT TIMESTAMP NO MATTER HOW OLD METRICS ARE
    for line in lines:
      if line:
        lineList = line.split(' ')
        lineList[2] = str(int(time.time()*1000))
        currentLines.append(' '.join(lineList))
    lines = currentLines
    return lines

  def run(self):
    lines = self.readFile()
    logger.info('first metric:\n{}'.format(lines[0]))
    logger.info('{} metrics to send'.format(len(lines)))
    data = '\n'.join(lines) + '\n'
    epochRandom = str(int(time.time())) + str(randint(1, 9000))
    s3Response = self.s3Client.put_object(
      Body=data, 
      Bucket=self.s3Bucket,
      Key='oh_my_goodness',
      ACL="bucket-owner-full-control"
    )
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
  logger.info('Done.\n')