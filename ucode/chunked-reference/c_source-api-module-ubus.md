---
title: 'ucode module: ubus'
module: ucode
origin_type: c_source
token_count: 8467
source_file: L1-raw/ucode/c_source-api-module-ubus.md
last_pipeline_run: '2026-07-01T13:51:57.973723+00:00'
source_commit: unknown
source_url: https://github.com/nicowillis/ucode/blob/unknown/lib/ubus.c
source_locator: lib/ubus.c
language: c
---

> **Source:** [https://github.com/nicowillis/ucode/blob/unknown/lib/ubus.c](https://github.com/nicowillis/ucode/blob/unknown/lib/ubus.c)
> **Kind:** c_source | **Commit:** unknown | **Method:** normalized
> **Normalized:** 2026-07-01

# ucode module: ubus

> **Live docs:** https://ucode.mein.io/module-ubus.html

---

## Ubus IPC

The `ubus` module provides functions for OpenWrt inter-process
communication, including access to ubus registered modules and their
methods, as well as monitoring and publish/subscribe activity on the
ubus message bus.

Functions can be individually imported using named import syntax:

```ucode
import { connect } from 'ubus';

const ubus = connect();
const result = ubus.call("session", "get", { key: "value" });
```

Alternatively, the module namespace can be imported using a wildcard
import:

```ucode
import * as ubus from 'ubus';

const ctx = ubus.connect();
```

The `ubus` module may also be loaded via the `-lubus` interpreter switch.

## Architecture

Ubus uses a broker pattern architecture with three main components:
- **`ubusd`**: The central message router/broker that manages
  registrations and forwards messages between objects
- **Server objects**: Interfaces/daemons that register methods for
  clients to call
- **Client objects**: Callers that invoke server object methods

All connections go through `ubusd`, significantly reducing the number
of IPC connections compared to traditional client-server models.

## Communication Schemes

Ubus provides three delivery schemes for IPC:

1. **Invoke** (one-to-one): Direct method calls to a specific object
   by ID
2. **Subscribe/Notify** (one-to-many, group by object): Notifications
   sent to all subscribers of a particular object
3. **Event Broadcast** (one-to-many, group by event): Events broadcast
   to all listeners registered for a matching event pattern

## Roles in Ubus

- **Object**: Process registered to `ubusd`, including services and
  service callers
- **Method**: Procedures provided by objects; servers can provide
  multiple methods
- **Data**: Information in JSON format carried by requests or replies
- **Subscriber**: Object subscribed to a target service; notified when
  the target sends notifications
- **Event**: Identified by a string event pattern; objects can register
  to events and send data with matching patterns
- **Event Registrant**: Object registered to an event pattern; receives
  forwarded data when matching messages are received

## Data Format

All data is transferred in JSON format via `blobmsg`. Method calls,
requests, and replies all use JSON for data serialization.

## Usage Examples

### Basic connection and method call
```ucode
const ubus = require("ubus");

// Connect to ubus and call a method
const conn = ubus.connect();
if (conn) {
    const result = conn.call("network.interface", "status", {});
    printf("Interface status: %.J\n", result);
    conn.disconnect();
}
```

### Asynchronous method invocation with callback
```ucode
const ubus = require("ubus");

// Typical pattern: async call with callback
const conn = ubus.connect();

conn.defer("some.object", "some_method", {}, (rc, result) => {
    if (rc == 0) {
        printf("Result: %.J\n", result);
    }
});
```

### Persistent connection pattern
```ucode
const ubus = require("ubus");

// Keep connection alive to prevent GC
const ubus_conn = ubus.connect();

function handle_request(request) {
    ubus_conn.defer("some.object", "some_method", {}, (rc, data) => {
        request.reply({ result: data });
    });
}
```

### Publishing an object
```ucode
const ubus = require("ubus");

const conn = ubus.connect();
const obj = conn.publish("my.service", {
    "hello": (req, msg) => {
        req.reply({ message: "Hello from " + msg.name });
    }
});
```

### Event broadcasting
```ucode
const ubus = require("ubus");

const conn = ubus.connect();

// Register as event listener
const listener = conn.listener("my.event.*", (pattern, data) => {
    printf("Received event: %s %.J\n", pattern, data);
});

// Send an event
conn.event("my.event.test", { data: "test payload" });
```

**See**: https://openwrt.org/docs/techref/ubus  

### ubus.error([numeric]) ⇒ `string` \| `number`
Query ubus error information.

Returns a string containing a description of the last ubus error when
the *numeric* argument is absent or false.

Returns a ubus status code number when the *numeric* argument is `true`.

Returns `null` if there is no error information.

**Kind**: instance method of [`ubus`](#module_ubus)  

| Param | Type | Description |
| --- | --- | --- |
| [numeric] | `boolean` | Whether to return a numeric status code (`true`) or a human readable error message (false). |

### ubus.connect([socket], [timeout]) ⇒ [`connection`](#module_ubus.connection)
Establish a connection to the ubus bus.

Connects to the specified ubus socket path or the default socket if none
is provided.

Returns a connection resource on success.

Returns `null` if the connection could not be established.

**Kind**: instance method of [`ubus`](#module_ubus)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [socket] | `string` |  | The path to the ubus socket to connect to. If omitted, the default socket path is used. |
| [timeout] | `number` | `30` | The timeout in seconds to use for subsequent ubus operations. |

### ubus.open\_channel(fd, cb, [disconnect_cb], [timeout]) ⇒ [`channel`](#module_ubus.channel)
Connect to a ubus channel from a file descriptor.

Creates a channel connection from an existing file descriptor, typically
received from a method call. The callback will be invoked for incoming
messages on the channel.

Returns a channel connection resource.

Returns `null` if the channel could not be created.

**Kind**: instance method of [`ubus`](#module_ubus)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `module:fs.file` \| `module:socket.socket` |  | The file descriptor or resource of the channel to connect to. When a plain integer fd is passed, the ubus channel takes ownership and closes it on disconnect. When a resource object with a `fileno()` method is passed, the resource retains ownership of the fd; the channel merely detaches from it on disconnect without closing. |
| cb | `function` |  | Callback invoked for incoming messages on the channel. |
| [disconnect_cb] | `function` |  | Optional callback invoked when the channel is disconnected. |
| [timeout] | `number` | `30` | The timeout in seconds for subsequent operations. |

### ubus.guard([handler]) ⇒ `function` \| `boolean`
Get or set the ubus exception handler.

When called without arguments, returns the currently registered exception
handler function. When called with a function argument, registers it as
the exception handler for ubus operations.

Returns the current exception handler when called without arguments.

Returns `true` when a new handler was set.

**Kind**: instance method of [`ubus`](#module_ubus)  

| Param | Type | Description |
| --- | --- | --- |
| [handler] | `function` | The exception handler function to register. |

### ubus.connection
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [connect()](#module_ubus+connect)
- [open_channel()](#module_ubus+open_channel)

* [.connection](#module_ubus.connection)
    * [.list([object_name])](#module_ubus.connection+list) ⇒ `Array.<string>`
    * [.call(object, method, [data], [return], [fd], [fd_cb])](#module_ubus.connection+call) ⇒ `\*`
    * [.defer(object, method, [data], [cb], [data_cb], [fd], [fd_cb])](#module_ubus.connection+defer) ⇒ [`deferred`](#module_ubus.deferred)
    * [.publish(object_name, [methods], [subscribe_callback])](#module_ubus.connection+publish) ⇒ [`object`](#module_ubus.object)
    * [.listener(pattern, cb)](#module_ubus.connection+listener) ⇒ [`listener`](#module_ubus.listener)
    * [.event(event_type, [event_data])](#module_ubus.connection+event) ⇒ `boolean`
    * [.subscriber(notify_callback, remove_callback, [subscription_patterns])](#module_ubus.connection+subscriber) ⇒ [`subscriber`](#module_ubus.subscriber)
    * [.disconnect()](#module_ubus.connection+disconnect) ⇒ `boolean`
    * [.error([numeric])](#module_ubus.connection+error) ⇒ `string` \| `number`

#### connection.list([object_name]) ⇒ `Array.<string>`
List available ubus objects.

Queries the ubus bus for registered objects. If an object name pattern
is provided, returns signatures for matching objects. Otherwise, returns
a list of all registered object paths.

Returns an array of object paths or object signatures.

Returns `null` if the list operation failed.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| [object_name] | `string` | Optional object name pattern to filter results. When provided, returns signatures for matching objects; otherwise returns all object paths. |

#### connection.call(object, method, [data], [return], [fd], [fd_cb]) ⇒ `\*`
Invoke a ubus method synchronously.

Calls the specified method on a ubus object and waits for the response.

Returns the method response data, or an array of responses if multiple
replies were received.

Returns `null` if the call failed.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| object | `string` \| `number` |  | The object name (string) or object ID (number) to call the method on. |
| method | `string` |  | The name of the method to invoke. |
| [data] | `Object` |  | Optional method arguments as an object with field names and values. |
| [return] | `string` \| `boolean` | `"\"single\""` | Controls how multiple responses are handled: `"single"` returns only the first response, `"multiple"` returns an array of all responses, `"ignore"` discards the response. |
| [fd] | `number` |  | Optional file descriptor to send along with the call. |
| [fd_cb] | `function` |  | Optional callback function invoked when a file descriptor is received. |

#### connection.defer(object, method, [data], [cb], [data_cb], [fd], [fd_cb]) ⇒ [`deferred`](#module_ubus.deferred)
Invoke a ubus method asynchronously.

Initiates a non-blocking call to the specified method on a ubus object.
The provided callback will be invoked when the response is received or on
timeout.

Returns a deferred request resource representing the pending operation.

Returns `null` if the deferred call could not be initiated.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| object | `string` | The object name to call the method on. |
| method | `string` | The name of the method to invoke. |
| [data] | `Object` | Optional method arguments as an object with field names and values. |
| [cb] | `function` | Callback function invoked when the operation completes. Receives status code and response data as arguments. |
| [data_cb] | `function` | Optional callback invoked for intermediate data notifications. |
| [fd] | `number` | Optional file descriptor to send along with the call. |
| [fd_cb] | `function` | Optional callback function invoked when a file descriptor is received. |

**Example**  
```ucode
// Asynchronous call with callback - typical pattern for RPC handlers
const conn = connect();

const req = conn.defer("some.object", "some_method", {}, (rc, data) => {
    if (rc == 0)
        printf("Result: %.J\n", data);
});
```
**Example**  
```ucode
// Persistent connection pattern - avoid GC by keeping reference
const ubus = connect();

function get_status(req) {
    // Use persistent ubus connection for async calls
    return ubus.defer("some.object", "some_method", {}, (rc, data) => {
        req.reply({ result: data });
    });
}
```

#### connection.publish(object_name, [methods], [subscribe_callback]) ⇒ [`object`](#module_ubus.object)
Publish a ubus object on the bus.

Registers a new object with the specified name and methods on the ubus
bus. The object can define method handlers and an optional subscribe
callback.

Returns an object resource representing the published object.

Returns `null` if the object could not be registered.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| object_name | `string` | The name to register the object under. |
| [methods] | `Object` | Optional object defining methods with `call` functions and optional `args` type specifications. |
| [subscribe_callback] | `function` | Optional callback invoked when a subscriber connects to the object. |

**Example**  
```ucode
const conn = connect();
const obj = conn.publish("my.service", {
    "hello": {
        call: (req, msg) => {
            req.reply({ message: "Hello, " + msg.name });
        },
        args: { name: "string" }
    }
});
```

#### connection.listener(pattern, cb) ⇒ [`listener`](#module_ubus.listener)
Register an event listener.

Registers a callback to be invoked when events matching the specified
pattern are received. The listener receives the event type and data.

Returns a listener resource that can be removed via
[remove()](#module_ubus.listener+remove).

Returns `null` if the listener could not be registered.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| pattern | `string` | The event type pattern to match, supporting wildcards (e.g., `` `system.*` ``, `` `my.event.?` ``). |
| cb | `function` | Callback invoked when a matching event is received. Receives the event type string and event data object as arguments. |

**Example**  
```ucode
const conn = connect();
const listener = conn.listener("system.*", (type, data) => {
    printf("Event %s: %.J\n", type, data);
});
```

#### connection.event(event_type, [event_data]) ⇒ `boolean`
Send a ubus event.

Broadcasts an event of the specified type with optional data to all
registered event listeners.

Returns `true` on success.

Returns `null` if the event could not be sent.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| event_type | `string` | The type string identifying the event. |
| [event_data] | `Object` | Optional event data as an object with field names and values. |

**Example**  
```ucode
const conn = connect();
conn.event("system.boot", { host: "router1", uptime: 3600 });
```

#### connection.subscriber(notify_callback, remove_callback, [subscription_patterns]) ⇒ [`subscriber`](#module_ubus.subscriber)
Register a ubus subscriber.

Creates a subscriber that can receive notifications from ubus objects.
The subscriber can define notify and remove callbacks, and optional
subscription patterns for automatic object discovery.

Returns a subscriber resource representing the registered subscriber.

Returns `null` if the subscriber could not be registered.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| notify_callback | `function` | Callback invoked when a notification is received from a subscribed object. |
| remove_callback | `function` | Callback invoked when a subscribed object is removed from the bus. |
| [subscription_patterns] | `Array.<string>` | Optional array of glob patterns for automatic object subscription. |

**Example**  
```ucode
const conn = connect();
const sub = conn.subscriber(
    (event) => {
        printf("Received: type=%s, data=%.J\n",
               event.type, event.data);
    },
    (objid) => {
        printf("Object removed: %d\n", objid);
    },
    ["network.interface.*"]  // Auto-subscribe to matching objects
);
// Subscribe to a specific object
sub.subscribe("some.object");
```

#### connection.disconnect() ⇒ `boolean`
Disconnect from the ubus bus.

Closes the connection to the ubus bus and releases associated resources.
All pending requests are aborted.

Returns `true` on success.

**Kind**: instance method of [`connection`](#module_ubus.connection)  
**Example**  
```ucode
const conn = connect();
// … do work …
conn.disconnect();
```

#### connection.error([numeric]) ⇒ `string` \| `number`
Query ubus error information.

Returns a string containing a description of the last ubus error when
the *numeric* argument is absent or false.

Returns a ubus status code number when the *numeric* argument is `true`.

Returns `null` if there is no error information.

**Kind**: instance method of [`connection`](#module_ubus.connection)  

| Param | Type | Description |
| --- | --- | --- |
| [numeric] | `boolean` | Whether to return a numeric status code (`true`) or a human readable error message (false). |

### ubus.channel
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [open_channel()](#module_ubus+open_channel)
- [new_channel()](#module_ubus.request+new_channel)

* [.channel](#module_ubus.channel)
    * [.request(method, [data], [return], [fd], [fd_cb])](#module_ubus.channel+request) ⇒ `\*`
    * [.defer(method, [data], [cb], [data_cb], [fd], [fd_cb])](#module_ubus.channel+defer) ⇒ [`deferred`](#module_ubus.deferred)
    * [.error([numeric])](#module_ubus.channel+error) ⇒ `string` \| `number`

#### channel.request(method, [data], [return], [fd], [fd_cb]) ⇒ `\*`
Send a request on a channel connection.

Similar to call() but uses object ID 0 for channel-based communication.

Returns the method response data.

Returns `null` if the request failed.

**Kind**: instance method of [`channel`](#module_ubus.channel)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| method | `string` |  | The name of the method to invoke. |
| [data] | `Object` |  | Optional method arguments as an object with field names and values. |
| [return] | `string` \| `boolean` | `"\"single\""` | Controls how multiple responses are handled. |
| [fd] | `number` |  | Optional file descriptor to send along with the request. |
| [fd_cb] | `function` |  | Optional callback function invoked when a file descriptor is received. |

**Example**  
```text
const chan = open_channel(…);
const result = chan.request("method_name", { arg: "value" });
```

#### channel.defer(method, [data], [cb], [data_cb], [fd], [fd_cb]) ⇒ [`deferred`](#module_ubus.deferred)
Send an asynchronous request on a channel connection.

Similar to defer() but uses object ID 0 for channel-based communication.

Returns a deferred request resource representing the pending operation.

Returns `null` if the deferred call could not be initiated.

**Kind**: instance method of [`channel`](#module_ubus.channel)  

| Param | Type | Description |
| --- | --- | --- |
| method | `string` | The name of the method to invoke. |
| [data] | `Object` | Optional method arguments as an object with field names and values. |
| [cb] | `function` | Callback function invoked when the operation completes. |
| [data_cb] | `function` | Optional callback invoked for intermediate data notifications. |
| [fd] | `number` | Optional file descriptor to send along with the request. |
| [fd_cb] | `function` | Optional callback function invoked when a file descriptor is received. |

**Example**  
```text
const chan = open_channel(…);
const req = chan.defer("method_name", { arg: "value" },
    (status, data) => {
        printf("Status: %d\n", status);
    });
```

#### channel.error([numeric]) ⇒ `string` \| `number`
Query ubus error information.

Returns a string containing a description of the last ubus error when
the *numeric* argument is absent or false.

Returns a ubus status code number when the *numeric* argument is `true`.

Returns `null` if there is no error information.

**Kind**: instance method of [`channel`](#module_ubus.channel)  

| Param | Type | Description |
| --- | --- | --- |
| [numeric] | `boolean` | Whether to return a numeric status code (`true`) or a human readable error message (false). |

### ubus.deferred
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [defer()](module:ubus#defer)
- [defer()](#module_ubus.channel+defer)

* [.deferred](#module_ubus.deferred)
    * [.completed()](#module_ubus.deferred+completed) ⇒ `boolean`
    * [.await()](#module_ubus.deferred+await) ⇒ `boolean`
    * [.abort()](#module_ubus.deferred+abort) ⇒ `boolean`

#### deferred.completed() ⇒ `boolean`
Check if a deferred request has completed.

Returns `true` if the deferred request has finished.

Returns `false` if the request is still pending.

**Kind**: instance method of [`deferred`](#module_ubus.deferred)  

#### deferred.await() ⇒ `boolean`
Wait synchronously for a deferred request to complete.

Blocks until the deferred request completes or times out.

Returns `true` if the request completed.

Returns `false` if the request was already completed.

**Kind**: instance method of [`deferred`](#module_ubus.deferred)  

#### deferred.abort() ⇒ `boolean`
Abort a pending deferred request.

Cancels an asynchronous request that has not yet completed.

Returns `true` if the request was aborted.

Returns `false` if the request was already completed.

**Kind**: instance method of [`deferred`](#module_ubus.deferred)  

### ubus.object
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [publish()](module:ubus#publish)
- [subscriber()](module:ubus#subscriber)

* [.object](#module_ubus.object)
    * [.notify(type, [data], [data_cb], [status_cb], [cb], [timeout])](#module_ubus.object+notify) ⇒ [`notify`](#module_ubus.notify) \| `number`
    * [.remove()](#module_ubus.object+remove) ⇒ `boolean`
    * [.subscribed()](#module_ubus.object+subscribed) ⇒ `boolean`

#### object.notify(type, [data], [data_cb], [status_cb], [cb], [timeout]) ⇒ [`notify`](#module_ubus.notify) \| `number`
Send a notification from a ubus object.

Sends an asynchronous notification of the specified type to all
subscribers of the object. Optional callbacks can be provided to handle
data, status, and completion events.

Returns a notification request resource for asynchronous operations.

Returns a status code number when a synchronous timeout is specified.

Returns `null` if the notification could not be sent.

**Kind**: instance method of [`object`](#module_ubus.object)  

| Param | Type | Description |
| --- | --- | --- |
| type | `string` | The notification type string. |
| [data] | `Object` | Optional notification data as an object with field names and values. |
| [data_cb] | `function` | Optional callback invoked for each data notification received. |
| [status_cb] | `function` | Optional callback invoked for status updates. |
| [cb] | `function` | Optional callback invoked when the notification operation completes. |
| [timeout] | `number` | Optional timeout in milliseconds. If specified, the operation waits synchronously for completion. |

**Example**  
```ucode
const obj = publish("my.service", {
    "trigger": (req, msg) => {
        obj.notify("update", { key: "value" }, (idx, ret) => {
            printf("Notification %d: status %d\n", idx, ret);
        });
        req.reply({ sent: true });
    }
});
```

#### object.remove() ⇒ `boolean`
Remove a ubus object from the bus.

Unregisters the object from the ubus bus, making it no longer accessible
to other clients.

Returns `true` on success.

Returns `null` if the object could not be removed.

**Kind**: instance method of [`object`](#module_ubus.object)  
**Example**  
```ucode
const obj = publish("my.service", { … });
// … do work …
obj.remove();
```

#### object.subscribed() ⇒ `boolean`
Check if a ubus object has subscribers.

Returns `true` if there are active subscribers to the object.

Returns `false` if no subscribers are currently connected.

**Kind**: instance method of [`object`](#module_ubus.object)  
**Example**  
```ucode
const obj = publish("my.service", {
    "trigger": (req, msg) => {
        if (obj.subscribed()) {
            obj.notify("update", { data: "value" });
        }
        req.reply({ notified: obj.subscribed() });
    }
});
```

### ubus.request
**Kind**: static class of [`ubus`](#module_ubus)  
**See**: [publish()](module:ubus#publish)  

* [.request](#module_ubus.request)
    * [.reply([reply], [rcode])](#module_ubus.request+reply) ⇒ `boolean`
    * [.defer()](#module_ubus.request+defer) ⇒ `boolean`
    * [.get_fd()](#module_ubus.request+get_fd) ⇒ `number`
    * [.set_fd(fd)](#module_ubus.request+set_fd) ⇒ `boolean`
    * [.error([rcode])](#module_ubus.request+error) ⇒ `boolean`
    * [.reply(data)](#module_ubus.request+reply) ⇒ `boolean`
    * [.new_channel(cb, [disconnect_cb], [timeout])](#module_ubus.request+new_channel) ⇒ [`channel`](#module_ubus.channel)

#### request.reply([reply], [rcode]) ⇒ `boolean`
Send a reply to a deferred ubus method call.

Sends the specified reply data to the caller of a deferred method
request. After sending the reply, the request context is finished unless
`more` is set to `true`.

Returns `true` on success.

Returns `null` if an error occurred or the reply was already sent.

**Kind**: instance method of [`request`](#module_ubus.request)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [reply] | `Object` |  | The reply data to send as an object with field names and values. |
| [rcode] | `number` | `0` | Optional status code to return. Use negative values to indicate more replies will follow. |

**Example**  
```ucode
// In a published object method handler
publish("my.service", {
    "hello": (req, msg) => {
        req.reply({ message: "Hello, " + msg.name });
    }
});
```

#### request.defer() ⇒ `boolean`
Defer completion of a ubus method call.

Marks the current request as deferred, allowing the handler to complete
the request asynchronously at a later time by calling reply().

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`request`](#module_ubus.request)  
**Example**  
```ucode
// In a published object method handler
publish("my.service", {
    "async_method": (req, msg) => {
        req.defer();
        // Do async work...
        req.reply({ result: "done" });
    }
});
```

#### request.get\_fd() ⇒ `number`
Get the caller's file descriptor from a ubus method call.

Returns the UNIX file descriptor number that was passed by the caller,
or -1 if no file descriptor was sent.

**Kind**: instance method of [`request`](#module_ubus.request)  
**Returns**: `number` - The file descriptor number, or -1 if none was provided.  

#### request.set\_fd(fd) ⇒ `boolean`
Set a file descriptor to send with a ubus method reply.

Associates a file descriptor with the current request to be sent back to
the caller along with the reply.

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`request`](#module_ubus.request)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` | The file descriptor number to send. |

**Example**  
```ucode
// In a published object method handler
publish("my.service", {
    "get_fd": (req, msg) => {
        let fd = some_file_descriptor;
        req.set_fd(fd);
        req.reply({ info: "fd sent" });
    }
});
```

#### request.error([rcode]) ⇒ `boolean`
Finish a ubus method call with an error status.

Completes the current deferred request with the specified error status
code without sending any reply data.

Returns `true` on success.

Returns `null` if an error occurred or the reply was already sent.

**Kind**: instance method of [`request`](#module_ubus.request)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [rcode] | `number` | `UBUS_STATUS_UNKNOWN_ERROR` | The error status code to return. |

**Example**  
```ucode
// In a published object method handler
publish("my.service", {
    "process": (req, msg) => {
        if (!msg.input) {
            req.error(UBUS_STATUS_INVALID_ARGUMENT);
            return;
        }
        req.reply({ result: "ok" });
    }
});
```

#### request.reply(data) ⇒ `boolean`
Send a reply to an asynchronous method call.

Sends the specified data as a reply to the incoming method call. This
function should be called within a published object's method handler.

Returns `true` on success.

Returns `null` if the reply could not be sent.

**Kind**: instance method of [`request`](#module_ubus.request)  

| Param | Type | Description |
| --- | --- | --- |
| data | `\*` | The data to send as reply. Can be any JSON-serializable value. |

**Example**  
```ucode
// Synchronous reply
const obj = publish("my.service", {
    hello: (req, msg) => {
        req.reply({ message: "Hello " + msg.name });
    }
});
```
**Example**  
```ucode
// Asynchronous reply after defer completes
const obj = publish("my.service", {
    some_method: (req) => {
        ubus_conn.defer("other.object", "other_method", {},
            (rc, data) => {
                req.reply({ result: data });
            });
    }
});
```

#### request.new\_channel(cb, [disconnect_cb], [timeout]) ⇒ [`channel`](#module_ubus.channel)
Create a new ubus channel from a method call context.

Creates a bidirectional channel communication path in response to an
incoming method call. The callback will be invoked for incoming messages
on the channel.

Returns a channel connection resource.

Returns `null` if the channel could not be created.

**Kind**: instance method of [`request`](#module_ubus.request)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| cb | `function` |  | Callback invoked for incoming messages on the channel. |
| [disconnect_cb] | `function` |  | Optional callback invoked when the channel is disconnected. |
| [timeout] | `number` | `30` | The timeout in seconds for subsequent operations. |

### ubus.notify
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [notify()](#module_ubus.object+notify)
- [subscriber()](module:ubus#subscriber)

* [.notify](#module_ubus.notify)
    * [.completed()](#module_ubus.notify+completed) ⇒ `boolean`
    * [.abort()](#module_ubus.notify+abort) ⇒ `boolean`

#### notify.completed() ⇒ `boolean`
Check if a notification request has completed.

Returns `true` if the notification request has finished.

Returns `false` if the request is still pending.

**Kind**: instance method of [`notify`](#module_ubus.notify)  
**Example**  
```ucode
const n = obj.notify("method", { data: "value" });
if (n.completed()) {
    printf("Notification sent\n");
}
```

#### notify.abort() ⇒ `boolean`
Abort a pending notification request.

Cancels an asynchronous notification request that has not yet completed.

Returns `true` if the request was aborted.

Returns `false` if the request was already completed.

**Kind**: instance method of [`notify`](#module_ubus.notify)  
**Example**  
```ucode
const n = obj.notify("method", { data: "value" });
if (!n.completed()) {
    n.abort();
}
```

### ubus.listener
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [listener()](module:ubus#listener)
- [event()](module:ubus#event)

#### listener.remove() ⇒ `boolean`
Remove an event listener from the bus.

Unregisters the event handler, stopping it from receiving further events.

Returns `true` on success.

Returns `null` if the listener could not be removed.

**Kind**: instance method of [`listener`](#module_ubus.listener)  
**Example**  
```ucode
const listener = conn.listener("my.event.*", (type, data) => {
    printf("Event: %s, Data: %.J\n", type, data);
});
// … later …
listener.remove();
```

### ubus.subscriber
**Kind**: static class of [`ubus`](#module_ubus)  
**See**

- [subscriber()](module:ubus#subscriber)
- [notify()](#module_ubus.object+notify)
- [subscribed()](#module_ubus.object+subscribed)

* [.subscriber](#module_ubus.subscriber)
    * [.subscribe(object_name)](#module_ubus.subscriber+subscribe) ⇒ `boolean`
    * [.unsubscribe(object_name)](#module_ubus.subscriber+unsubscribe) ⇒ `boolean`
    * [.remove()](#module_ubus.subscriber+remove) ⇒ `boolean`

#### subscriber.subscribe(object_name) ⇒ `boolean`
Subscribe to a ubus object.

Registers interest in notifications from the specified object.

Returns `true` on success.

Returns `null` if the subscription failed.

**Kind**: instance method of [`subscriber`](#module_ubus.subscriber)  

| Param | Type | Description |
| --- | --- | --- |
| object_name | `string` | The name of the object to subscribe to. |

**Example**  
```ucode
const conn = connect();
const sub = conn.subscriber("my.object", (event) => {
    printf("Notification: type=%s, data=%.J\n", event.type, event.data);
});
// … later, to re-subscribe …
sub.subscribe("my.object");
```

#### subscriber.unsubscribe(object_name) ⇒ `boolean`
Unsubscribe from a ubus object.

Stops receiving notifications from the specified object.

Returns `true` on success.

Returns `null` if the unsubscription failed.

**Kind**: instance method of [`subscriber`](#module_ubus.subscriber)  

| Param | Type | Description |
| --- | --- | --- |
| object_name | `string` | The name of the object to unsubscribe from. |

**Example**  
```ucode
const sub = conn.subscriber("my.object", (event) => { … });
// … later, to unsubscribe temporarily …
sub.unsubscribe("my.object");
```

#### subscriber.remove() ⇒ `boolean`
Remove a subscriber from the bus.

Unregisters the subscriber, stopping it from receiving further
notifications.

Returns `true` on success.

Returns `null` if the subscriber could not be removed.

**Kind**: instance method of [`subscriber`](#module_ubus.subscriber)  
**Example**  
```ucode
const sub = conn.subscriber("my.object", (event) => { … });
// … when done …
sub.remove();
```

### ubus~Ubus status codes
**Kind**: inner typedef of [`ubus`](#module_ubus)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| STATUS_OK | `number` | Operation successful |
| STATUS_INVALID_COMMAND | `number` | Invalid command |
| STATUS_INVALID_ARGUMENT | `number` | Invalid argument |
| STATUS_METHOD_NOT_FOUND | `number` | Method not found |
| STATUS_NOT_FOUND | `number` | Object not found |
| STATUS_NO_DATA | `number` | No data available |
| STATUS_PERMISSION_DENIED | `number` | Permission denied |
| STATUS_TIMEOUT | `number` | Operation timed out |
| STATUS_NOT_SUPPORTED | `number` | Operation not supported |
| STATUS_UNKNOWN_ERROR | `number` | Unknown error |
| STATUS_CONNECTION_FAILED | `number` | Connection failed |
| STATUS_NO_MEMORY | `number` | Out of memory (new) |
| STATUS_PARSE_ERROR | `number` | Parse error (new) |
| STATUS_SYSTEM_ERROR | `number` | System error (new) |
| STATUS_CONTINUE | `number` | Virtual code for continued replies |

### ubus~Ubus system object IDs
**Kind**: inner typedef of [`ubus`](#module_ubus)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| SYSTEM_OBJECT_ACL | `number` | System object ACL identifier, used to query ACL data via [call()](module:ubus#call) with an integer object ID |
