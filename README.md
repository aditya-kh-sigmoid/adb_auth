# Registration of Azure SPN into multiple Databricks Workspaces under a subscription.

Procedure:
1. import class `RegistrationBase`

```python
from databricks_reg import RegistrationBase
```
2. Save your credentials in respective variables

```python
client_id = "client id"
client_secret = "client secret"
tenant_id = "tenant id"
subscription_id = "subscription id"
```
But it is recommended to export your variables in a shell and then import them to your python script 

In Shell
```bash
export CLIENT_ID="client id"
export CLIENT_SECRET="client secret"
export TENANT_ID="tenant id"
export SUBSCRIPTION_ID="subscription id"
```

In Python
```python
import os

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
tenant_id = os.getenv('TENANT_ID')
subscription_id = os.getenv('SUBSCRIPTION_ID')
```
3. Create Registration object and run the `register()` method

```python
reg = RegistrationBase(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)

reg.register(subscription_id)
```