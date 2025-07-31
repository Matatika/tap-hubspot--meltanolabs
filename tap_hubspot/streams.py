"""Stream type classes for tap-hubspot."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers
from typing_extensions import override

from tap_hubspot.client import (
    DynamicIncrementalHubspotStream,
    HubspotStream,
    PropertyStream,
)

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType


class ContactStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/contacts."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "contacts"
    path = "/objects/contacts"
    incremental_path = "/objects/contacts/search"
    primary_keys = ("id",)
    replication_key = "lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class UsersStream(HubspotStream):
    """https://developers.hubspot.com/docs/api/settings/user-provisioning."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = id keys for replication
    records_jsonpath = json response body
    """

    name = "users"
    path = "/users"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property("email", StringType),
        Property("roleIds", ArrayType(StringType)),
        Property("primaryteamid", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/settings/v3"


class OwnersStream(HubspotStream):
    """https://developers.hubspot.com/docs/api/crm/owners#endpoint?spec=GET-/crm/v3/owners/."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "owners"
    path = "/owners"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property("email", StringType),
        Property("firstName", StringType),
        Property("lastName", StringType),
        Property("userId", IntegerType),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class TicketPipelineStream(HubspotStream):
    """https://legacydocs.hubspot.com/docs/methods/tickets/get-all-tickets."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "ticket_pipelines"
    path = "/pipelines/tickets"
    primary_keys = ("createdAt",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("label", StringType),
        Property("displayOrder", IntegerType),
        Property("active", BooleanType),
        Property(
            "stages",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("displayOrder", IntegerType),
                    Property(
                        "metadata",
                        ObjectType(
                            Property("ticketState", StringType),
                            Property("isClosed", StringType),
                        ),
                    ),
                    Property("stageId", StringType),
                    Property("createdAt", IntegerType),
                    Property("updatedAt", IntegerType),
                    Property("active", BooleanType),
                ),
            ),
        ),
        Property("objectType", StringType),
        Property("objectTypeId", StringType),
        Property("pipelineId", StringType),
        Property("createdAt", IntegerType),
        Property("updatedAt", IntegerType),
        Property("default", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm-pipelines/v1"


class DealPipelineStream(HubspotStream):
    """https://legacydocs.hubspot.com/docs/methods/deals/get-all-deals."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "deal_pipelines"
    path = "/pipelines/deals"
    primary_keys = ("createdAt",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("label", StringType),
        Property("displayOrder", IntegerType),
        Property("active", BooleanType),
        Property(
            "stages",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("displayOrder", IntegerType),
                    Property(
                        "metadata",
                        ObjectType(
                            Property("isClosed", BooleanType),
                            Property("probability", StringType),
                        ),
                    ),
                    Property("stageId", StringType),
                    Property("createdAt", IntegerType),
                    Property("updatedAt", IntegerType),
                    Property("active", BooleanType),
                ),
            ),
        ),
        Property("objectType", StringType),
        Property("objectTypeId", StringType),
        Property("pipelineId", StringType),
        Property("createdAt", IntegerType),
        Property("updatedAt", IntegerType),
        Property("default", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm-pipelines/v1"


class EmailSubscriptionStream(HubspotStream):
    """https://legacydocs.hubspot.com/docs/methods/email/get_subscriptions."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = id keys for replication
    records_jsonpath = json response body
    """

    name = "email_subscriptions"
    path = "/subscriptions"
    primary_keys = ("id",)
    records_jsonpath = "$[subscriptionDefinitions][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("portalId", IntegerType),
        Property("name", StringType),
        Property("description", StringType),
        Property("active", BooleanType),
        Property("internal", BooleanType),
        Property("category", StringType),
        Property("channel", StringType),
        Property("internalName", StringType),
        Property("businessUnitId", IntegerType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/email/public/v1"


class PropertyTicketStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_tickets"
    path = "/properties/tickets"


class PropertyDealStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_deals"
    path = "/properties/deals"


class PropertyContactStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_contacts"
    path = "/properties/contacts"


class PropertyCompanyStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_companies"
    path = "/properties/company"


class PropertyProductStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_products"
    path = "/properties/product"


class PropertyLineItemStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_line_items"
    path = "/properties/line_item"


class PropertyEmailStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_emails"
    path = "/properties/email"


class PropertyPostalMailStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_postal_mails"
    path = "/properties/postal_mail"


class PropertyGoalStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "goal_targets"
    path = "/properties/goal_targets"


class PropertyCallStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_calls"
    path = "/properties/call"


class PropertyMeetingStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_meetings"
    path = "/properties/meeting"


class PropertyTaskStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_tasks"
    path = "/properties/task"


class PropertyCommunicationStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "property_communications"
    path = "/properties/communication"


class PropertyNotesStream(PropertyStream):
    """https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    """

    name = "properties"
    path = "/properties/notes"

    def get_records(self, context: Context | None) -> t.Iterable[dict[str, t.Any]]:
        """Merges all the property stream data into a single property table."""
        property_ticket = PropertyTicketStream(self._tap)
        property_deal = PropertyDealStream(self._tap)
        property_contact = PropertyContactStream(self._tap)
        property_company = PropertyCompanyStream(self._tap)
        property_product = PropertyProductStream(self._tap)
        property_lineitem = PropertyLineItemStream(self._tap)
        property_email = PropertyEmailStream(self._tap)
        property_postalmail = PropertyPostalMailStream(self._tap)
        property_call = PropertyCallStream(self._tap)
        property_goal = PropertyGoalStream(self._tap)
        property_meeting = PropertyMeetingStream(self._tap)
        property_task = PropertyTaskStream(self._tap)
        property_communication = PropertyCommunicationStream(self._tap)
        return (
            list(property_ticket.get_records(context))
            + list(property_deal.get_records(context))
            + list(property_contact.get_records(context))
            + list(property_company.get_records(context))
            + list(property_product.get_records(context))
            + list(property_lineitem.get_records(context))
            + list(property_email.get_records(context))
            + list(property_postalmail.get_records(context))
            + list(property_call.get_records(context))
            + list(property_goal.get_records(context))
            + list(property_meeting.get_records(context))
            + list(property_task.get_records(context))
            + list(property_communication.get_records(context))
            + list(super().get_records(context))
        )


class CompanyStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/companies.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "companies"
    path = "/objects/companies"
    incremental_path = "/objects/companies/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class DealStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/deals."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "deals"
    path = "/objects/deals"
    incremental_path = "/objects/deals/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class FeedbackSubmissionsStream(HubspotStream):
    """https://developers.hubspot.com/docs/api/crm/feedback-submissions."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "feedback_submissions"
    path = "/objects/feedback_submissions"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("city", StringType),
                Property("createdDate", StringType),
                Property("domain", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("industry", StringType),
                Property("name", StringType),
                Property("phone", StringType),
                Property("state", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class LineItemStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/line-items."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "line_items"
    path = "/objects/line_items"
    incremental_path = "/objects/line_items/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class ProductStream(HubspotStream):
    """https://developers.hubspot.com/docs/api/crm/products."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "products"
    path = "/objects/products"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("description", StringType),
                Property("hs_cost_of_goods_sold", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_recurring_billing_period", StringType),
                Property("hs_sku", StringType),
                Property("name", StringType),
                Property("price", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class TicketStream(HubspotStream):
    """https://developers.hubspot.com/docs/api/crm/tickets."""

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "tickets"
    path = "/objects/tickets"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_pipeline", StringType),
                Property("hs_pipeline_stage", StringType),
                Property("hs_ticket_priority", StringType),
                Property("hubspot_owner_id", StringType),
                Property("subject", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class QuoteStream(HubspotStream):
    """https://developers.hubspot.com/docs/api/crm/quotes.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "quotes"
    path = "/objects/quotes"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("hs_createdate", StringType),
                Property("hs_expiration_date", StringType),
                Property("hs_quote_amount", StringType),
                Property("hs_quote_number", StringType),
                Property("hs_status", StringType),
                Property("hs_terms", StringType),
                Property("hs_title", StringType),
                Property("hubspot_owner_id", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class GoalStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/goals.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "goal_targets"
    path = "/objects/goal_targets"
    incremental_path = "/objects/goal_targets/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class CallStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/calls.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "calls"
    path = "/objects/calls"
    incremental_path = "/objects/calls/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class CommunicationStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/communications.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "communications"
    path = "/objects/communications"
    incremental_path = "/objects/communications/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class EmailStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/email."""

    name = "emails"
    path = "/objects/emails"
    incremental_path = "/objects/emails/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class MeetingStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/meetings.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "meetings"
    path = "/objects/meetings"
    incremental_path = "/objects/meetings/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class NoteStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/notes.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "notes"
    path = "/objects/notes"
    incremental_path = "/objects/notes/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class PostalMailStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/postal-mail.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "postal_mail"
    path = "/objects/postal_mail"
    incremental_path = "/objects/postal_mail/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class TaskStream(DynamicIncrementalHubspotStream):
    """https://developers.hubspot.com/docs/api/crm/tasks.

    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "tasks"
    path = "/objects/tasks"
    incremental_path = "/objects/tasks/search"
    primary_keys = ("id",)
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """Returns an updated path which includes the api version."""
        return "https://api.hubapi.com/crm/v3"


class FormsStream(HubspotStream):
    """https://developers.hubspot.com/docs/reference/api/marketing/forms/#get-%2Fmarketing%2Fv3%2Fforms%2F."""

    name = "forms"
    path = "/marketing/v3/forms"
    primary_keys = ("id",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("archived", th.BooleanType),
        th.Property(
            "fieldGroups",
            th.ArrayType(
                th.ObjectType(
                    th.Property("groupType", th.StringType),
                    th.Property("richTextType", th.StringType),
                    th.Property(
                        "fields",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("objectTypeId", th.StringType),
                                th.Property("name", th.StringType),
                                th.Property("label", th.StringType),
                                th.Property("description", th.StringType),
                                th.Property("required", th.BooleanType),
                                th.Property("hidden", th.BooleanType),
                                th.Property("defaultValue", th.StringType),
                                th.Property("placeholder", th.StringType),
                                th.Property("fieldType", th.StringType),
                                additional_properties=True,
                            ),
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "configuration",
            th.ObjectType(
                th.Property("language", th.StringType),
                th.Property("cloneable", th.BooleanType),
                th.Property(
                    "postSubmitAction",
                    th.ObjectType(
                        th.Property("type", th.StringType),
                        th.Property("value", th.StringType),
                    ),
                ),
                th.Property("editable", th.BooleanType),
                th.Property("archivable", th.BooleanType),
                th.Property("recaptchaEnabled", th.BooleanType),
                th.Property("notifyContactOwner", th.BooleanType),
                th.Property("notifyRecipients", th.ArrayType(th.StringType)),
                th.Property("createNewContactForNewEmail", th.BooleanType),
                th.Property("prePopulateKnownValues", th.BooleanType),
                th.Property("allowLinkToResetKnownValues", th.BooleanType),
                th.Property(
                    "lifecycleStages",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("objectTypeId", th.StringType),
                            th.Property("value", th.StringType),
                        ),
                    ),
                ),
            ),
        ),
        th.Property(
            "displayOptions",
            th.ObjectType(
                th.Property("renderRawHtml", th.BooleanType),
                th.Property("theme", th.StringType),
                th.Property("submitButtonText", th.StringType),
                th.Property("style", th.ObjectType(additional_properties=True)),
                th.Property("cssClass", th.StringType),
            ),
        ),
        th.Property(
            "legalConsentOptions",
            th.ObjectType(
                th.Property("subscriptionTypeIds", th.ArrayType(th.IntegerType)),
                th.Property("lawfulBasis", th.StringType),
                th.Property("privacyText", th.StringType),
                th.Property("type", th.StringType),
            ),
        ),
        th.Property("formType", th.StringType),
    ).to_dict()

    @override
    def get_child_context(self, record, context):  # noqa: ANN001, ANN201
        return {"form_id": record["id"]}


class FormSubmissionsStream(HubspotStream):
    """https://developers.hubspot.com/docs/reference/api/marketing/forms/v1#get-submissions-for-a-form."""

    parent_stream_type = FormsStream
    name = "form_submissions"
    path = "/form-integrations/v1/submissions/forms/{form_id}"
    primary_keys = ("conversionId",)
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property("conversionId", th.StringType),
        th.Property("submittedAt", th.IntegerType),
        th.Property(
            "values",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                    th.Property("objectTypeId", th.StringType),
                ),
            ),
        ),
        th.Property("pageUrl", th.URIReferenceType),
    ).to_dict()

    @override
    def get_url_params(self, context, next_page_token):  # noqa: ANN001, ANN201
        params = super().get_url_params(context, next_page_token)
        params["limit"] = 50  # max supported
        return params
