# awscli password-store CredentialsProvider plugin

Enables fetching credentials from [pass](https://www.passwordstore.org/).

## Installation

To use this plugin, you must have `awscli` and `pass` configured.

The easiest way is to use pip:

```
pip install awscli-pass-credentials
```

Add this plugin to your awscli configuration file:
```
[plugins]
pass = awspass
```

Add AWS credentials to pass:
```
pass edit aws/default
```

Credentials should be in the following format:
```
aws_access_key_id = KEYID
aws_secret_access_key = SECRETKEY
```
