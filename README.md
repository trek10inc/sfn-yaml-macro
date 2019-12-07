# AWS StepFunctions YAML Macro

Use YAML to define your Amazon States Language for your AWS CloudFormation-defined StepFunctions state machines

Made with ❤️ by Trek10. Available on the [AWS Serverless Application Repository](https://aws.amazon.com/serverless)

## Usage

After deploying this into your account, you can use the `SFNYAML` transform:

```yml
Transform: [ AWS::Serverless-2016-10-31, SFNYAML ]
```

Then you can replace the `DefinitionString` (JSON-defined Amazon States Language) with `Definition` (YAML):

```yml
  MyStateMachine:
    Type: AWS::StepFunctions::StateMachine
    Properties:
      RoleArn: !GetAtt ExecutionRole.Arn
      # DefinitionString: !Sub |
      #   {
      #     "StartAt": "Hello"
      #     "States": {
      #       "Hello": {
      #         "Type": "Task",
      #         "Resource": "${Function.Arn}",
      #         "End": true
      #       }
      #     }
      #   }
      Definition:
        StartAt: Hello
        States:
          Hello:
            Type: Task
            Resource: !GetAtt Function.Arn
            End: true
```

All of the CloudFormation intrinsic functions are supported, and used as expected

## License

MIT No Attribution (undefined)

https://console.aws.amazon.com/serverlessrepo/home?region=us-east-1#/published-applications/arn:aws:serverlessrepo:us-east-1:031669591898:applications~sfn-yaml-macro
