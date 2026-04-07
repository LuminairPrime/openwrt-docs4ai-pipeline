## Scenario 26
```sh
# Source the native shell JSON helper
. /usr/share/libubox/jshn.sh

# Load JSON string from $payload
load_json "$payload"

# Enter the network object
json_select network

# Read the proto and device fields
json_get_var proto proto
json_get_var device device

# Navigate back out cleanly
json_select ..
json_select ..
```

## Scenario 27
```javascript
// Call runtime network-interface dump over ubus
ubus.call('network.interface', 'dump', {}, function(err, data) {
    if (err) {
        console.error('Ubus call failed:', err);
        return;
    }

    // Extract the first non-loopback IPv4 address for the lan interface
    const lanInterface = data.interfaces.find(iface => 
        iface.interface === 'lan' && 
        iface.ipv4-address && 
        iface.ipv4-address.length > 0
    );

    if (lanInterface) {
        // Filter out loopback addresses (127.0.0.0/8)
        const nonLoopbackAddress = lanInterface['ipv4-address'].find(addr => 
            !addr.address.startsWith('127.')
        );

        if (nonLoopbackAddress) {
            console.log('First non-loopback IPv4 address for lan:', nonLoopbackAddress.address);
            // Use the address as needed
        } else {
            console.log('No non-loopback IPv4 address found for lan interface');
        }
    } else {
        console.log('LAN interface not found or has no IPv4 address');
    }
});
```

## Scenario 17
OpenWrt ucode is a lightweight, embeddable bytecode interpreter and virtual machine designed specifically for OpenWrt. It was created to provide a safe, sandboxed execution environment for configuration scripts and plugins that need to interact with the system without the overhead or security risks of full-blown interpreters like bash or Lua. Ucode is good for writing system configuration scripts, network protocols, and daemon plugins that require direct system access while maintaining security through its sandboxed execution model. Its small footprint makes it ideal for resource-constrained embedded devices running OpenWrt.

## Scenario 01
```sh
#!/bin/sh /etc/rc.common
# OpenWrt init script for my_daemon

START=99
STOP=10

start() {
    # Read hostname from config file
    config_load my_daemon
    config_get hostname my_daemon hostname
    
    # Apply hostname if configured
    if [ -n "$hostname" ]; then
        hostname "$hostname"
    fi
    
    # Start the daemon
    service_start /usr/bin/my_daemon
}

stop() {
    service_stop /usr/bin/my_daemon
}

restart() {
    stop
    start
}

# Restart if it crashes
watchdog() {
    if ! pidof my_daemon > /dev/null; then
        logger -t my_daemon "Daemon crashed, restarting..."
        restart
    fi
}
```

## Scenario 03
```c
#include <libubox/blobmsg_json.h>
#include <libubus.h>

static struct ubus_method my_plugin_methods[] = {
    UBUS_METHOD("getStatus", NULL, NULL),
};

static struct ubus_object_type my_plugin_object_type =
    UBUS_OBJECT_TYPE("my_plugin", my_plugin_methods);

static struct ubus_object my_plugin_object = {
    .name = "my_plugin",
    .type = &my_plugin_object_type,
    .methods = my_plugin_methods,
    .n_methods = ARRAY_SIZE(my_plugin_methods),
};

static void my_plugin_connect_handler(struct ubus_context *ctx)
{
    ubus_add_object(ctx, &my_plugin_object);
}

int main(int argc, char **argv)
{
    struct ubus_context *ctx;
    const char *ubus_socket = NULL;
    
    ctx = ubus_connect(ubus_socket);
    if (!ctx) {
        fprintf(stderr, "Failed to connect to ubus\n");
        return -1;
    }
    
    ubus_set_connect_callback(ctx, my_plugin_connect_handler);
    
    ubus_add_uloop(ctx);
    
    uloop_run();
    
    ubus_free(ctx);
    return 0;
}
```

## Scenario 04
```erb
<% +section :class => "cbi-section" do %>
  <% firewalls = Map.new %>
  <% interfaces = Map.new %>
  
  <% uci:foreach("firewall", "zone") do |zone| %>
    <% firewalls[zone['.name']] = zone['.name'] %>
  <% end %>
  
  <% uci:foreach("network", "interface") do |iface| %>
    <% unless iface['.name'] =~ /^loopback$/ %>
      <% interfaces[iface['.name']] = iface['.name'] %>
    <% end %>
  <% end %>
  
  <% form_tag biweburl(:admin, "network", "firewall", "save") do %>
    <fieldset>
      <legend><%= translate("Firewall Zone Settings") %></legend>
      
      <div class="cbi-value">
        <label class="cbi-value-label" for="cbid.firewall.@zone[0].name"><%= translate("Zone Name") %></label>
        <div class="cbi-value-field">
          <%= select_tag "zone_name", options_for_select(firewalls) %>
        </div>
      </div>
      
      <div class="cbi-value">
        <label class="cbi-value-label" for="cbid.firewall.@zone[0].network"><%= translate("Network Interfaces") %></label>
        <div class="cbi-value-field">
          <%= select_tag "network_interfaces", options_for_select(interfaces), :multiple => true %>
        </div>
      </div>
      
      <div class="cbi-value">
        <label class="cbi-value-label" for="cbid.firewall.@zone[0].input"><%= translate("Input Policy") %></label>
        <div class="cbi-value-field">
          <%= select_tag "input_policy", options_for_select([["accept", "Accept"], ["drop", "Drop"], ["reject", "Reject"]]) %>
        </div>
      </div>
      
      <div class="cbi-value">
        <label class="cbi-value-label" for="cbid.firewall.@zone[0].output"><%= translate("Output Policy") %></label>
        <div class="cbi-value-field">
          <%= select_tag "output_policy", options_for_select([["accept", "Accept"], ["drop", "Drop"], ["reject", "Reject"]]) %>
        </div>
      </div>
      
      <div class="cbi-value">
        <label class="cbi-value-label" for="cbid.firewall.@zone[0].forward"><%= translate("Forward Policy") %></label>
        <div class="cbi-value-field">
          <%= select_tag "forward_policy", options_for_select([["accept", "Accept"], ["drop", "Drop"], ["reject", "Reject"]]) %>
        </div>
      </div>
    </fieldset>
    
    <div class="cbi-button">
      <%= submit_tag("save", translate("Save & Apply")) %>
      <%= submit_tag("apply", translate("Save")) %>
    </div>
  <% end %>
<% end %>
```