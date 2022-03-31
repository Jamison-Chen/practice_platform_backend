import hashlib

from django.db import connection
from django.core.management import call_command

from .models import tenant
from ..account.models import user


DEVELOPER_DOMAIN_NAME = "127.0.0.1"
DEVELOPER_SCHEMA_NAME = "public"

OFFICIAL_DOMAIN_NAME = "598c-210-242-50-84.ngrok.io"
OFFICIAL_SCHEMA_NAME = "official"


def get_tenants_map():
    m = {
        DEVELOPER_DOMAIN_NAME: DEVELOPER_SCHEMA_NAME,
        OFFICIAL_DOMAIN_NAME: OFFICIAL_SCHEMA_NAME,
    }
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        for each in tenant.objects.all():
            m[each.domain_name] = each.schema_name

        # Switch back to the official schema
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))
    return m


def get_request_domain_name(request):
    return request.get_host().split(":")[0].lower()  # remove port


def get_tenant_schema_name(domainName):
    return get_tenants_map().get(domainName)


def create_tenant_schema(request):
    if get_request_domain_name(request) != OFFICIAL_DOMAIN_NAME:
        raise Exception("Unknown Origin.")
    with connection.cursor() as cursor:
        newDomainName = request.POST.get("domain_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if newDomainName in get_tenants_map():
            raise Exception("This domain name already exsists.")

        newSchemaName = "_" + hashlib.sha1(newDomainName.encode("ascii")).hexdigest()

        # Migrate this new schema and create the admin user of this tenant
        call_command("migrate_one", newSchemaName)
        cursor.execute("SET search_path to {}".format(newSchemaName))
        user.objects.create_tenant_user(email, password, username=username)

        # Create an account for developers in this schema
        user.objects.create_superuser("admin@admin.com", "0000", username="Admin")

        # Append domain-schema pair into the public schema of the database
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        tenant.objects.create(domain_name=newDomainName, schema_name=newSchemaName)

        # Switch the schema back
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))

        return {
            "domain_name": newDomainName,
            "username": username,
            "email": email,
            "password": password,
            "schema_name": newSchemaName,
        }


# This function is only for testing.
def remove_multiple_tenant_schema(request):
    if get_request_domain_name(request) != OFFICIAL_DOMAIN_NAME:
        raise Exception("Unknown Origin.")
    domainNameList = request.POST.get("domain_name_list").split(",")
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        for each in tenant.objects.filter(domain_name__in=domainNameList):
            cursor.execute("DROP SCHEMA IF EXISTS {} CASCADE".format(each.schema_name))
        tenant.objects.filter(domain_name__in=domainNameList).delete()
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))


def connect_to_tenant_schema(request):
    with connection.cursor() as cursor:
        # Use the domain name of the request to get schema name.
        # Possible Cases:
        # 1) from a registered tenant domain
        # 2) from the official website domain
        #    to register a new domain or simply fetch data of the official website
        # 3) from the localhost
        #    to manage the developer account in the development team
        schemaName = get_tenant_schema_name(get_request_domain_name(request))
        if not schemaName:
            raise Exception("This domain doesn't have a dedicated schema.")
        cursor.execute("SET search_path to {};".format(schemaName))
