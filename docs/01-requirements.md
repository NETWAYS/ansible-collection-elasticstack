# Requirements

There are some requirements that the user have to fulfill while using the collection. Some of them will be refactored and disappear from the list soon.

**Inventory names**

The collection provides roles for several tools (elasticsearch, kibana, ...). In some tasks hosts from the specific inventory group are fetched. The group names are customizable via variables. But using different inventory names than provided inside the variables will result in errors.

**elasticstack_ca_host**

This is a mandatory variable. It is used to define the host that will be used as "CA host". Per default it is already defined (first host inside the group `elasticstack_elasticsearch_group_name`). In case you are using different group names, this variable wont be set with a defualt value.