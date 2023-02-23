import requests

class RegistrationBase:
    def __init__(self, client_id: str , client_secret: str, tenant_id: str, scope = '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.scope = scope

    def get_access_token(self):
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f"client_id={self.client_id}&grant_type=client_credentials&scope={self.scope}%2F.default&client_secret={self.client_secret}"
        response = requests.post(url=url, headers=headers, data=data)


        try:
            response.raise_for_status()
            if 'access_token' in response.json():
                return response.json()['access_token']
            else:
                print('provide correct SPN credentials')
        except Exception as e:
            print(e)

    def get_management_token(self):
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f"client_id={self.client_id}&grant_type=client_credentials&resource=https%3A%2F%2Fmanagement.core.windows.net%2F&client_secret={self.client_secret}"
        response = requests.post(url=url, headers=headers, data=data)

        try:
            response.raise_for_status()
            if 'access_token' in response.json():
                return response.json()['access_token']
            else:
                print('provide correct SPN credentials')
        except Exception as e:
            print(e)

    def register(self, subscription_id):
        access_token = self.get_access_token()
        management_token = self.get_management_token()

        if access_token and management_token:
            failures = []

            resource_ids = self.list_resource_ids(subscription_id, management_token)
            for resource_id in resource_ids:
                url = self.get_workspaceUrl(resource_id, management_token) + '/api/2.0/'
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'X-Databricks-Azure-SP-Management-Token': management_token,
                    'X-Databricks-Azure-Workspace-Resource-Id': resource_id
                }

                response = requests.post(url=url, headers=headers)
                try:
                    response.json()
                except:
                    failures.append({'resource_id': resource_id, 'response': response.text})

            if failures == []:
                print('registered to all workspaces successfully')
            else:
                print('Failed registrations:', failures)


    def get_workspaceUrl(self, resource_id, management_token):
        url = f"https://management.azure.com{resource_id}?api-version=2018-04-01"
        headers = {
            "Authorization": f"Bearer {management_token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return 'https://' + response.json()['properties']['workspaceUrl']
        
        except requests.exceptions.RequestException as e:
            print(f"Error getting workspace URL: {e}")
            return None
        
    def get_workspace_details(self, resource_id, management_token):
        url = f"https://management.azure.com{resource_id}?api-version=2018-04-01"
        headers = {
            "Authorization": f"Bearer {management_token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error getting workspace URL: {e}")
            return None

    def list_resource_ids(self, subscription_id, management_token):
        url = f"https://management.azure.com/subscriptions/{subscription_id}/resources?api-version=2021-04-01"
        headers = {'Authorization': f'Bearer {management_token}'}
        response = requests.get(url=url, headers=headers)
        resource_ids = []

        try:
            response.raise_for_status()
            # return response.json()
            for i in response.json()['value']:
                if i['type'] == "Microsoft.Databricks/workspaces":
                    resource_ids.append(i['id'])
            return resource_ids

        except Exception as e:
            print('Error:', e)
