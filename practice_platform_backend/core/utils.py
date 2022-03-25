from django.db import connection
from django.core.management import call_command
import hashlib
from .models import tenant
from ..account.models import user

DEVELOPER_DOMAIN_NAME = "127.0.0.1"
DEVELOPER_SCHEMA_NAME = "public"

OFFICIAL_DOMAIN_NAME = "b14b-114-24-67-212.ngrok.io"
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
        username = request.POST.get("domain_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if newDomainName in get_tenants_map():
            raise Exception("This domain name already exsists.")

        newSchemaName = "_" + hashlib.sha1(newDomainName.encode("ascii")).hexdigest()

        # migrate this new schema and create admin user of this schema
        call_command("migrate_one", newSchemaName)
        user.objects.create_tenant_user(email, password, username=username)
        user.objects.create_superuser("admin@admin.com", "0000", username="Admin")

        # Append domain-schema pair into database
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        tenant.objects.create(domain_name=newDomainName, schema_name=newSchemaName)

        # Switch the schema back
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))


def connect_to_tenant_schema(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {};".format(DEVELOPER_SCHEMA_NAME))
        schemaName = get_tenant_schema_name(get_request_domain_name(request))

        # Switch back to the official schema
        cursor.execute("SET search_path to {};".format(OFFICIAL_SCHEMA_NAME))

        if not schemaName:
            raise Exception("This domain doesn't have a dedicated schema.")
        cursor.execute("SET search_path to {};".format(schemaName))
