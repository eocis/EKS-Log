# Node에서 Cloudwatch Log로 기록하기위한 권한 획득
# 실습 편의를 위해 'Cloudwatch Full Access' 권한 부여
resource "aws_iam_role_policy" "cw-policy" {
  name   = "node-cloudwatch-log-policy"
  role   = module.eks.worker_iam_role_name
  policy = jsonencode(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "autoscaling:Describe*",
                        "cloudwatch:*",
                        "logs:*",
                        "sns:*",
                        "iam:GetPolicy",
                        "iam:GetPolicyVersion",
                        "iam:GetRole"
                    ],
                    "Effect": "Allow",
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": "iam:CreateServiceLinkedRole",
                    "Resource": "arn:aws:iam::*:role/aws-service-role/events.amazonaws.com/AWSServiceRoleForCloudWatchEvents*",
                    "Condition": {
                        "StringLike": {
                            "iam:AWSServiceName": "events.amazonaws.com"
                        }
                    }
                }
            ]
        }
    )
}