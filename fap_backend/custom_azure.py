from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'fapbackstorage' # Must be replaced by your <storage_account_name>
    account_key = 'KLvqtqr+spg3tjefN97WZfwH7Na1YNWJLgVwXh2DFPtUREVGhMHMMOUhmaFL6Pa7BjpdK9hxJYM73WF39UmEZA==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'fapbackstorage' # Must be replaced by your storage_account_name
    account_key = 'KLvqtqr+spg3tjefN97WZfwH7Na1YNWJLgVwXh2DFPtUREVGhMHMMOUhmaFL6Pa7BjpdK9hxJYM73WF39UmEZA==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None