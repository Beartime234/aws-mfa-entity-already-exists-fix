import unittest
import handler


class HandlerTests(unittest.TestCase):
    def test_handler(self):
        with self.assertRaises(SystemExit):  # Check that will exit if error code is incorrect
            handler.lambda_handler({"detail": {"errorCode": "random"}}, {})

    def test_form_mfa_device_arn(self):
        self.assertEqual(handler.form_mfa_arn("123456789012", "testUser", "/"),
                         "arn:aws:iam::123456789012:mfa/testUser")
        self.assertEqual(handler.form_mfa_arn("123456789012", "testUser", "/somepath/"),
                         "arn:aws:iam::123456789012:mfa/somepath/testUser")
        self.assertNotEqual(handler.form_mfa_arn("123456789012", "testUser", "/somepath/"),
                            "arn:aws:iam::123456789012:mfa/testUser")


test_event = {'version': '0', 'id': '1234', 'detail-type': 'AWS API Call via CloudTrail',
              'source': 'aws.iam', 'account': '123456789012', 'time': '2019-11-24T07:38:30Z', 'region': 'us-east-1', 'resources': [],
              'detail': {'eventVersion': '1.05', 'userIdentity': {'type': 'IAMUser', 'principalId': 'SCRUBBED',
                                                                  'arn': 'arn:aws:iam::123456789012:user/testUser',
                                                                  'accountId': '123456789012', 'accessKeyId': 'SCRUBBED',
                                                                  'userName': 'testUser', 'sessionContext':
                                                                      {'attributes': {'mfaAuthenticated': 'true', 'creationDate': '2019-11-24T07:27:15Z'}}, 'invokedBy': 'signin.amazonaws.com'},'eventTime': '2019-11-24T07:38:30Z', 'eventSource': 'iam.amazonaws.com', 'eventName': 'CreateVirtualMFADevice', 'awsRegion': 'us-east-1', 'sourceIPAddress': '1.1.1.1', 'userAgent': 'signin.amazonaws.com', 'errorCode': 'EntityAlreadyExistsException', 'errorMessage': 'MFADevice entity at the same path and name already exists.', 'requestParameters': {'virtualMFADeviceName': 'test', 'path': '/'}, 'responseElements': None, 'requestID': 'SCRUBBED', 'eventID': 'SCRUBBED', 'eventType': 'AwsApiCall'}}

if __name__ == '__main__':
    unittest.main()
