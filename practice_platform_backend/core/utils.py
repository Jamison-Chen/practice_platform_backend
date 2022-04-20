import hashlib
import os

from django.db import connection
from django.core.management import call_command
from django.conf import settings

from .models import tenant as Tenant
from .serializers import TenantSerializer
from ..account.models import user as User
from ..account.utils import validate_account_info


DEVELOPER_DOMAIN_NAME = "127.0.0.1"
DEVELOPER_SCHEMA_NAME = "public"

OFFICIAL_DOMAIN_NAME = "ce8a-210-242-50-84.ngrok.io"
OFFICIAL_SCHEMA_NAME = "official"


def get_tenants_map():
    m = {
        DEVELOPER_DOMAIN_NAME: DEVELOPER_SCHEMA_NAME,
        OFFICIAL_DOMAIN_NAME: OFFICIAL_SCHEMA_NAME,
    }
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        for each in Tenant.objects.all():
            m[each.domain_name] = each.schema_name

        # Switch back to the official schema
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))
    return m


def get_request_domain_name(request):
    return request.get_host().split(":")[0].lower()  # ignore port


def get_tenant_schema_name(domainName):
    return get_tenants_map().get(domainName)


def validate_domain_name(request):
    if get_request_domain_name(request) != OFFICIAL_DOMAIN_NAME:
        raise Exception("Unknown Origin.")
    newDomainName = request.POST.get("domain-name")
    if newDomainName in get_tenants_map():
        raise Exception("This domain name already exsists.")
    if (not newDomainName) or (" " in newDomainName):
        raise Exception("Illegal domain name.")


def create_tenant_schema(request):
    validate_domain_name(request)
    validate_account_info(request)  # Validate the manager user info
    with connection.cursor() as cursor:
        newDomainName = request.POST.get("domain-name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        newSchemaName = "_" + hashlib.sha1(newDomainName.encode("ascii")).hexdigest()

        # Migrate this new schema and create the admin user of this tenant
        call_command("migrate_one", newSchemaName)
        cursor.execute("SET search_path to {}".format(newSchemaName))
        User.objects.create_tenant_user(email, password, username=username)

        # Create an account for developers in this schema
        User.objects.create_superuser("admin@admin.com", "0000", username="Admin")

        # Append domain-schema pair into the public schema of the database
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        Tenant.objects.create(domain_name=newDomainName, schema_name=newSchemaName)

        # Switch the schema back
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))

        return {
            "domain-name": newDomainName,
            "username": username,
            "email": email,
            "password": password,
            "schema-name": newSchemaName,
        }


def read_tenant_info(request):
    domain_name = request.POST.get("fake-from-domain")
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        t = Tenant.objects.get(domain_name=domain_name)
        result = {
            "brand-name": t.brand_name or "",
            "tax-id-number": t.tax_id_number or "",
            "logo-url": settings.MEDIA_URL + str(t.logo) if t.logo else "",
            "tel": t.tel or "",
        }
        # Switch the schema back
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))
        return result


def update_tenant_info(request):
    domain_name = request.POST.get("fake-from-domain")
    brand_name = request.POST.get("brand-name")
    tax_id_number = request.POST.get("tax-id-number")
    logo = request.FILES.get("logo")
    tel = request.POST.get("tel")
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        t = Tenant.objects.get(domain_name=domain_name)
        new_brand_name = brand_name or t.brand_name
        new_tax_id_number = tax_id_number or t.tax_id_number
        new_logo = logo or t.logo
        new_tel = tel or t.tel

        t.brand_name = new_brand_name
        t.tax_id_number = new_tax_id_number
        t.tel = new_tel
        try:
            os.remove(str(settings.BASE_DIR) + str(settings.MEDIA_URL) + str(t.logo))
        except:
            pass
        t.logo = new_logo
        t.save()
        result = {
            "brand-name": new_brand_name,
            "tax-id-number": new_tax_id_number,
            "logo-url": settings.MEDIA_URL + str(t.logo),
            "tel": new_tel,
        }
        # Switch the schema back
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))
        return result


# This function is only for testing.
def remove_multiple_tenant_schema(request):
    if get_request_domain_name(request) != OFFICIAL_DOMAIN_NAME:
        raise Exception("Unknown Origin.")
    domainNameList = request.POST.get("domain_name_list").split(",")
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        for each in Tenant.objects.filter(domain_name__in=domainNameList):
            cursor.execute("DROP SCHEMA IF EXISTS {} CASCADE".format(each.schema_name))
        Tenant.objects.filter(domain_name__in=domainNameList).delete()
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))


# This function is only for testing.
def remove_all_tenant_schemas():
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        for each in Tenant.objects.all():
            cursor.execute("DROP SCHEMA IF EXISTS {} CASCADE".format(each.schema_name))
        Tenant.objects.all().delete()
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))


def list_all_tenants(request):
    if get_request_domain_name(request) != DEVELOPER_DOMAIN_NAME:
        raise Exception("Unknown Origin.")
    result = []
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(DEVELOPER_SCHEMA_NAME))
        queryset = Tenant.objects.all()
        serializer_class = TenantSerializer
        result = serializer_class(queryset, many=True).data
        cursor.execute("SET search_path to {}".format(OFFICIAL_SCHEMA_NAME))
    return result


def connect_to_official_schema(request):
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {};".format(OFFICIAL_SCHEMA_NAME))


def connect_to_tenant_schema(request):
    with connection.cursor() as cursor:
        # Use the domain name of the request to get schema name.
        # Possible Cases:
        # 1) The request was from a registered tenant domain
        # 2) The request was from the official website domain
        #    to register a new domain or simply fetch data of the official website
        # 3) The request was from the localhost
        #    to manage the developer account in the development team
        schemaName = get_tenant_schema_name(get_request_domain_name(request))
        if not schemaName:
            raise Exception("This domain doesn't have a dedicated schema.")
        cursor.execute("SET search_path to {};".format(schemaName))


def fake_connect_to_tenant_schema(request):
    ############## This function is for testing only. ##########################
    ############## For the reason that we don't actually use ###################
    ############## dedicatede domain as the host name at the frontend. #########
    with connection.cursor() as cursor:
        schemaName = get_tenant_schema_name(request.POST.get("fake-from-domain"))
        if not schemaName:
            raise Exception("This domain doesn't have a dedicated schema.")
        cursor.execute("SET search_path to {};".format(schemaName))
