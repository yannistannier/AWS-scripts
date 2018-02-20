
### Test error template 
```
aws cloudformation validate-template --template-body file://spitch.template.yaml 
```

### Create stack
```
aws cloudformation create-stack --region eu-west-1 --template-body file://spitch.template.yaml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --stack-name spitchtv
```


### Update 

create change set
```
aws cloudformation create-change-set --stack-name spitchdev --template-body file://spitch.template.yaml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --change-set-name <Name>
```

describe change set
```
aws cloudformation describe-change-set --stack-name spitchdev --change-set-name <Name>
```

execute change set
```
aws cloudformation execute-change-set --stack-name spitchdev --change-set-name <Name>
```

delete change set
```
aws cloudformation delete-change-set --stack-name spitchdev --change-set-name <Name>
```