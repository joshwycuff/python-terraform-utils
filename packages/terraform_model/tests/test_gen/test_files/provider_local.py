from terraform_model.all import *
from providers import *


# required providers
RequiredProvider('local', version='2.2.2')

# providers
ProviderLocal()

# resources
LocalFile('file', filename='file.txt')
