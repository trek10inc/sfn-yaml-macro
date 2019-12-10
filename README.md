# AWS StepFunctions YAML Macro

Use YAML to define your Amazon States Language for your AWS CloudFormation-defined StepFunctions state machines

Made with ❤️ by Trek10. Available on the [AWS Serverless Application Repository](https://aws.amazon.com/serverless)

## Usage

After deploying this into your account, you can use the `SFNYAML` transform:

```yml
Transform: [ AWS::Serverless-2016-10-31, SFNYAML ]
```

Then you can replace the JSON-defined `DefinitionString` with YAML-defined `DefinitionString` Amazon States Language:

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
      DefinitionString:
        StartAt: Hello
        States:
          Hello:
            Type: Task
            Resource: !GetAtt Function.Arn
            End: true
```

All of the CloudFormation intrinsic functions are supported, and used as expected

## Known Issues

- Does not support `AWS::NoValue` being used in the definition

## License

MIT No Attribution (undefined)
