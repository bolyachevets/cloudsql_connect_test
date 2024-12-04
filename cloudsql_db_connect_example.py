# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from google.cloud.sql.connector import Connector


# locally works with Application Default Credentials (ADC) - i.e. gcloud login
# remotely  works by setting GOOGLE_APPLICATION_CREDENTIALS to service account path
# to test account locally - os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'auth-dev-sa-token.json'
def cloudsql_db_connect():
    try:
        # Initialize the Cloud SQL Connector
        connector = Connector()

        # Retrieve connection details from environment variables
        instance_connection_name = os.environ['DB_INSTANCE_CONNECTION_NAME']  # e.g., "project:region:instance"
        username = os.environ['DB_USER'] # https://github.com/GoogleCloudPlatform/cloud-sql-python-connector?tab=readme-ov-file#automatic-iam-database-authentication
        password = os.environ['DB_PASSWORD'] # if running authenticating of gcp via service account key, can use service account name instead of user/password combo
        dbname = os.environ['DB_DBNAME']

        connection = connector.connect(
            instance_connection_name,
            "pg8000",
            db=dbname,
            user=username,
            # password=password,
            enable_iam_auth=True, # will also need this enabled for running outside gcp
            ip_type='public', # if running in GCP, this should be private
        )

        # Create a cursor to execute a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Database version:", db_version[0])

    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        # Close the connection and connector
        if connection:
            connection.close()
        connector.close()


if __name__ == '__main__':
    cloudsql_db_connect()
