import configparser
import re
import subprocess

import botocore.credentials
import botocore.session


class PassCredentialsProvider(botocore.credentials.CredentialProvider):
    METHOD = "password-store"

    def __init__(self, profile):
        self.profile = profile

    def load(self):
        creds = subprocess.check_output(["pass", "aws/{0}".format(self.profile)])

        cf = configparser.ConfigParser()
        cf.read_string("[DEFAULT]\n" + creds.decode("utf-8"))

        creds_dict = cf.defaults()

        return botocore.credentials.Credentials(
            access_key=creds_dict['aws_access_key_id'],
            secret_key=creds_dict['aws_secret_access_key'],
            token=creds_dict.get('token'),
            method=self.METHOD,
        )


def pass_profiles():
    return {
        re.sub("aws/(.*)\.gpg", "\\1", line): {}
        for line in subprocess.check_output(["pass", "git", "ls-files", "aws"]).decode("utf-8").split("\n")
    }


def awscli_initialize(x):
    p = botocore.credentials.create_credential_resolver
    b = botocore.session.Session._build_profile_map

    def build_profile_map(self):
        return { **pass_profiles(), **b(self) }

    def fn(session, cache=None):
        resolver = p(session, cache)

        profile_name = session.get_config_variable('profile') or 'default'

        resolver.providers.insert(0, PassCredentialsProvider(profile_name))

        return resolver

    botocore.credentials.create_credential_resolver = fn
    botocore.session.Session._build_profile_map = build_profile_map
