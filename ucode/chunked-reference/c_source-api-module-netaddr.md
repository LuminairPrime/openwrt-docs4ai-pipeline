---
title: 'ucode module: netaddr'
module: ucode
origin_type: c_source
token_count: 10514
source_file: L1-raw/ucode/c_source-api-module-netaddr.md
last_pipeline_run: '2026-11-01T18:17:43.472245+00:00'
source_commit: unknown
source_url: https://github.com/nicowillis/ucode/blob/unknown/lib/netaddr.c
source_locator: lib/netaddr.c
language: c
---

> **Source:** [https://github.com/nicowillis/ucode/blob/unknown/lib/netaddr.c](https://github.com/nicowillis/ucode/blob/unknown/lib/netaddr.c)
> **Kind:** c_source | **Commit:** unknown | **Method:** normalized
> **Normalized:** 2026-11-01

# ucode module: netaddr

> **Live docs:** https://ucode.mein.io/module-netaddr.html

---

## Network Address

The `netaddr` module provides functions and the `netaddr.range` object type
for parsing, validating and manipulating IP addresses, network prefixes and
MAC addresses.

Address ranges are represented by `netaddr.range` instances which carry the
address, its family and a prefix size (CIDR notation). Instances are
created with the `new()`, `IPv4()`, `IPv6()` or `MAC()` functions:

  ```ucode
  import * as netaddr from 'netaddr';

  const addr = netaddr.new('10.24.0.1/24');
  const addr = netaddr.new('10.24.0.1/255.255.255.0');
  const addr = netaddr.new('10.24.0.1', '255.255.255.0');  // separate netmask
  const addr = netaddr.new('10.24.0.1/24', 16);            // override netmask

  const addr6 = netaddr.new('fe80::221:63ff:fe75:aa17/64');
  const addr6 = netaddr.new('fe80::221:63ff:fe75:aa17/ffff:ffff:ffff:ffff::');

  const mac = netaddr.new('00:11:22:cc:dd:ee');
  const mac = netaddr.MAC('C0:B6:F9:00:00:00/24');
  ```

The `checkv4()`, `checkv6()` and `checkmac()` functions provide
non-throwing validation, returning the canonical string representation of
the given address or `null` if the argument is not a valid address of the
respective family:

  ```ucode
  netaddr.checkv4('127.0.0.1');  // "127.0.0.1"
  netaddr.checkv6('::1');        // "::1"
  netaddr.checkmac('00:11:22:cc:dd:ee');  // "00:11:22:CC:DD:EE"
  netaddr.checkv4('nonsense');   // null
  ```

### netaddr.new(address, [netmask]) ⇒ [`range`](#module_netaddr.range)
Construct a new `netaddr.range` instance, auto-detecting the address family.

Raises a runtime exception if the given argument does not represent a
valid address or if the given optional netmask is of a different family.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| `number` \| `Array.<number>` \| `object` | A valid IPv4 or IPv6 address, optionally with prefix size (CIDR notation) or netmask separated by slash, an unsigned number, an array of bytes, or a sockaddr-like object (see below). Numbers are interpreted as MAC addresses, except when used with the [v4](#module_netaddr+v4) or [v6](#module_netaddr+v6) constructors. The address family of byte arrays is determined by their length: `4` for IPv4, `6` for MAC and `16` for IPv6. A sockaddr-like object has the following properties: - `address` (string, mandatory): the address value - `family` (number, optional): `AF_INET` (2), `AF_INET6` (10) or   `AF_PACKET` (17, MAC); guessed from `address` if omitted - `interface` (string|number, optional): scope for `AF_INET6` addresses,   either an interface name or index |
| [netmask] | `string` \| `number` | A valid IPv4 or IPv6 netmask or a number containing a prefix size in bits (`0..32` for IPv4, `0..128` for IPv6). Overrides the mask embedded in the first argument if specified. |

**Example**  
```ucode
const addr = netaddr.new('10.24.0.1/24');
const addr = netaddr.new('10.24.0.1/255.255.255.0');
const addr = netaddr.new('10.24.0.1', '255.255.255.0');  // separate netmask
const addr = netaddr.new('10.24.0.1/24', 16);            // override netmask

const addr6 = netaddr.new('fe80::221:63ff:fe75:aa17/64');
const addr6 = netaddr.new('fe80::221:63ff:fe75:aa17/ffff:ffff:ffff:ffff::');

const mac = netaddr.new('00:11:22:cc:dd:ee');
const mac = netaddr.new(0x001122ccddeeff);

const addr = netaddr.new([ 10, 24, 0, 1 ]);          // IPv4
const addr6 = netaddr.new([ 0xfe, 0x80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ]);

const addr = netaddr.new({ address: '10.24.0.1' });  // family guessed
const addr = netaddr.new({ family: 2, address: '10.24.0.1' });
const addr6 = netaddr.new({ family: 10, address: 'fe80::1', interface: 'lo' });
```

### netaddr.v4(address, [netmask]) ⇒ [`range`](#module_netaddr.range)
Construct a new IPv4 `netaddr.range` instance.

Raises a runtime exception if the given argument does not represent a
valid IPv4 address or if the given optional netmask is of a different
family.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| `number` \| `Array.<number>` \| `object` | A valid IPv4 address, optionally with prefix size (CIDR notation) or netmask separated by slash, an unsigned number representing the address in host byte order, an array of exactly `4` bytes, or a sockaddr-like object with `family` `AF_INET` (or an address guessed as IPv4). |
| [netmask] | `string` \| `number` | A valid IPv4 netmask or a number containing a prefix size between `0` and `32` bit. Overrides the mask embedded in the first argument if specified. |

**Example**  
```ucode
const addr = netaddr.IPv4('10.24.0.1/24');
const addr = netaddr.IPv4('10.24.0.1/255.255.255.0');
const addr = netaddr.IPv4('10.24.0.1', '255.255.255.0');  // separate netmask
const addr = netaddr.IPv4('10.24.0.1/24', 16);            // override netmask
```

### netaddr.v6(address, [netmask], [scope]) ⇒ [`range`](#module_netaddr.range)
Construct a new IPv6 `netaddr.range` instance.

Raises a runtime exception if the given argument does not represent a
valid IPv6 address or if the given optional netmask is of a different
family.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| `number` \| `Array.<number>` \| `object` | A valid IPv6 address, optionally with prefix size (CIDR notation) or netmask separated by slash, an unsigned number representing the last 32 bit of the address, an array of exactly `16` bytes, or a sockaddr-like object with `family` `AF_INET6` (or an address guessed as IPv6), optionally carrying an `interface` scope. |
| [netmask] | `string` \| `number` | A valid IPv6 netmask or a number containing a prefix size between `0` and `128` bit. Overrides the mask embedded in the first argument if specified. |
| [scope] | `string` \| `number` | An optional address scope for link-local addresses (`fe80::/10`), either an interface name or numeric index. |

**Example**  
```ucode
const addr6 = netaddr.IPv6('fe80::221:63ff:fe75:aa17/64');
const addr6 = netaddr.IPv6('fe80::221:63ff:fe75:aa17/ffff:ffff:ffff:ffff::');
const addr6 = netaddr.IPv6('fe80::221:63ff:fe75:aa17', 'ffff:ffff:ffff:ffff::');
const addr6 = netaddr.IPv6('fe80::221:63ff:fe75:aa17/64', 128);  // override
const addr6 = netaddr.IPv6('fe80::221:63ff:fe75:aa17', 64, 'eth0');
```

### netaddr.mac(address, [netmask]) ⇒ [`range`](#module_netaddr.range)
Construct a new MAC `netaddr.range` instance.

Raises a runtime exception if the given argument does not represent a
valid ethernet MAC address or if the given optional mask is of a
different family.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| `number` \| `Array.<number>` \| `object` | A valid ethernet MAC address, optionally with prefix size (CIDR notation) or mask separated by slash, an unsigned number representing the last 32 bit of the address, an array of exactly `6` bytes, or a sockaddr-like object with `family` `AF_PACKET`. |
| [netmask] | `string` \| `number` | A valid MAC address mask or a number containing a prefix size between `0` and `48` bit. Overrides the mask embedded in the first argument if specified. |

**Example**  
```ucode
const intel_macs = netaddr.MAC('C0:B6:F9:00:00:00/24');
const intel_macs = netaddr.MAC('C0:B6:F9:00:00:00/FF:FF:FF:0:0:0');
const intel_macs = netaddr.MAC('C0:B6:F9:00:00:00', 'FF:FF:FF:0:0:0');
const intel_macs = netaddr.MAC('C0:B6:F9:00:00:00/24', 48);  // override mask
```

### netaddr.checkv4(address) ⇒ `string`
Verify an IPv4 address.

Checks whether the given argument is a preexisting `netaddr.range` IPv4 address
instance or a string literal convertible to an IPv4 address and returns a
plain string containing the canonical representation of the address.

Returns `null` if the argument is not a valid IPv4 address. This function
is intended to aid in safely verifying address literals without having to
deal with exceptions.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| [`range`](#module_netaddr.range) | A valid IPv4 address or existing `netaddr.range` IPv4 instance. |

**Example**  
```ucode
netaddr.checkv4(netaddr.new('127.0.0.1'));  // "127.0.0.1"
netaddr.checkv4('127.0.0.1');          // "127.0.0.1"
netaddr.checkv4('nonsense');           // null
netaddr.checkv4(123);                  // null
netaddr.checkv4(null);                 // null
```

### netaddr.checkv6(address) ⇒ `string`
Verify an IPv6 address.

Checks whether the given argument is a preexisting `netaddr.range` IPv6 address
instance or a string literal convertible to an IPv6 address and returns a
plain string containing the canonical representation of the address.

Returns `null` if the argument is not a valid IPv6 address. This function
is intended to aid in safely verifying address literals without having to
deal with exceptions.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| [`range`](#module_netaddr.range) | A valid IPv6 address or existing `netaddr.range` IPv6 instance. |

**Example**  
```ucode
netaddr.checkv6(netaddr.new('0:0:0:0:0:0:0:1'));  // "::1"
netaddr.checkv6('0:0:0:0:0:0:0:1');          // "::1"
netaddr.checkv6('nonsense');                 // null
netaddr.checkv6(123);                        // null
netaddr.checkv6(null);                       // null
```

### netaddr.checkmac(address) ⇒ `string`
Verify an ethernet MAC address.

Checks whether the given argument is a preexisting `netaddr.range` MAC address
instance or a string literal convertible to an ethernet MAC and returns a
plain string containing the canonical representation of the address.

Returns `null` if the argument is not a valid MAC address. This function
is intended to aid in safely verifying address literals without having to
deal with exceptions.

**Kind**: instance method of [`netaddr`](#module_netaddr)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| [`range`](#module_netaddr.range) | A valid MAC address or existing `netaddr.range` MAC instance. |

**Example**  
```ucode
netaddr.checkmac(netaddr.new('00-11-22-cc-dd-ee'));  // "00:11:22:CC:DD:EE"
netaddr.checkmac('00:11:22:cc:dd:ee');          // "00:11:22:CC:DD:EE"
netaddr.checkmac('nonsense');                   // null
netaddr.checkmac(123);                          // null
netaddr.checkmac(null);                         // null
```

### netaddr.range
**Kind**: static class of [`netaddr`](#module_netaddr)  
**See**

- [new()](#module_netaddr+new)
- [v4()](#module_netaddr+v4)
- [v6()](#module_netaddr+v6)
- [mac()](#module_netaddr+mac)

**Properties**

| Name | Type | Description |
| --- | --- | --- |
| bits | `number` | The prefix size in bits (read/write). `32` for IPv4, `128` for IPv6, `48` for MAC addresses. |
| family | `number` | The address family (read-only): `4` for IPv4, `6` for IPv6, `1` for MAC addresses. |
| scope | `number` | The address scope as a numeric interface index (read/write). Only meaningful for IPv6 and MAC address instances. |
| scopeid | `string` | The address scope as an interface name (read/write). Accepts an interface name or numeric index for assignment. `null` if no scope is set. Only meaningful for IPv6 and MAC address instances. |
| netmask | `string` | The netmask as a string, e.g. `"255.255.255.0"` (read-only). |
| host | [`range`](#module_netaddr.range) | The host address as a new range with a full-width prefix (read-only). |
| mapped4 | [`range`](#module_netaddr.range) | The mapped IPv4 address as a new range, or `null` if the instance is not an IPv6 mapped IPv4 address (read-only). |
| unscopename | `string` | The interface name of the address scope, or an empty string if no scope is set (read-only). |
| size | `number` | The number of addresses in this range, or `null` if the value does not fit into a 64 bit signed integer (read-only). |

* [.range](#module_netaddr.range)
    * [.is4()](#module_netaddr.range+is4) ⇒ `boolean`
    * [.is4rfc1918()](#module_netaddr.range+is4rfc1918) ⇒ `boolean`
    * [.is4linklocal()](#module_netaddr.range+is4linklocal) ⇒ `boolean`
    * [.is6()](#module_netaddr.range+is6) ⇒ `boolean`
    * [.is6linklocal()](#module_netaddr.range+is6linklocal) ⇒ `boolean`
    * [.is6mapped4()](#module_netaddr.range+is6mapped4) ⇒ `boolean`
    * [.ismac()](#module_netaddr.range+ismac) ⇒ `boolean`
    * [.ismaclocal()](#module_netaddr.range+ismaclocal) ⇒ `boolean`
    * [.ismacmcast()](#module_netaddr.range+ismacmcast) ⇒ `boolean`
    * [.lower(addr)](#module_netaddr.range+lower) ⇒ `boolean`
    * [.higher(addr)](#module_netaddr.range+higher) ⇒ `boolean`
    * [.equal(addr)](#module_netaddr.range+equal) ⇒ `boolean`
    * [.prefix([mask])](#module_netaddr.range+prefix) ⇒ `number`
    * [.network([mask])](#module_netaddr.range+network) ⇒ [`range`](#module_netaddr.range)
    * [.mask([mask])](#module_netaddr.range+mask) ⇒ [`range`](#module_netaddr.range)
    * [.broadcast([mask])](#module_netaddr.range+broadcast) ⇒ [`range`](#module_netaddr.range)
    * [.scoped()](#module_netaddr.range+scoped) ⇒ [`range`](#module_netaddr.range)
    * [.unscoped()](#module_netaddr.range+unscoped) ⇒ [`range`](#module_netaddr.range)
    * [.tomac()](#module_netaddr.range+tomac) ⇒ [`range`](#module_netaddr.range)
    * [.tolinklocal()](#module_netaddr.range+tolinklocal) ⇒ [`range`](#module_netaddr.range)
    * [.contains(addr)](#module_netaddr.range+contains) ⇒ `boolean`
    * [.add(amount, [inplace])](#module_netaddr.range+add) ⇒ [`range`](#module_netaddr.range) \| `boolean` \| `null`
    * [.sub(amount, [inplace])](#module_netaddr.range+sub) ⇒ [`range`](#module_netaddr.range) \| `boolean` \| `null`
    * [.minhost()](#module_netaddr.range+minhost) ⇒ [`range`](#module_netaddr.range)
    * [.maxhost()](#module_netaddr.range+maxhost) ⇒ [`range`](#module_netaddr.range)
    * [.string()](#module_netaddr.range+string) ⇒ `string`
    * [.tostring()](#module_netaddr.range+tostring) ⇒ `string`
    * [.__get__(key)](#module_netaddr.range+__get__) ⇒ `number` \| `string` \| `null`
    * [.__set__(key, value)](#module_netaddr.range+__set__) ⇒ `null`

#### range.is4() ⇒ `boolean`
Checks whether the CIDR instance is an IPv4 address range.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the CIDR is an IPv4 range, else `false`  

#### range.is4rfc1918() ⇒ `boolean`
Checks whether the CIDR instance is within the private RFC1918 address
space.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the entire range of this CIDR lies within
one of the ranges `10.0.0.0-10.255.255.255`, `172.16.0.0-172.31.0.0` or
`192.168.0.0-192.168.255.255`, else `false`  
**Example**  
```ucode
const addr = netaddr.new('192.168.45.2/24');
addr.is4rfc1918();  // true
```

#### range.is4linklocal() ⇒ `boolean`
Checks whether the CIDR instance is an IPv4 link local (Zeroconf)
address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the entire range of this CIDR lies within
the range `169.254.0.0-169.254.255.255`, else `false`  
**Example**  
```ucode
const addr = netaddr.new('169.254.34.125');
addr.is4linklocal();  // true
```

#### range.is6() ⇒ `boolean`
Checks whether the CIDR instance is an IPv6 address range.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the CIDR is an IPv6 range, else `false`  

#### range.is6linklocal() ⇒ `boolean`
Checks whether the CIDR instance is an IPv6 link local address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the entire range of this CIDR lies within
the `fe80::/10` range, else `false`  
**Example**  
```ucode
const addr = netaddr.new('fe92:53a:3216:af01:221:63ff:fe75:aa17/64');
addr.is6linklocal();  // true
```

#### range.is6mapped4() ⇒ `boolean`
Checks whether the CIDR instance is an IPv6 mapped IPv4 address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the address is an IPv6 mapped IPv4 address
in the form `::ffff:1.2.3.4`  
**Example**  
```ucode
const addr = netaddr.new('::ffff:192.168.1.1');
addr.is6mapped4();  // true
```

#### range.ismac() ⇒ `boolean`
Checks whether the CIDR instance is an ethernet MAC address range.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the CIDR is a MAC address range, else
`false`  

#### range.ismaclocal() ⇒ `boolean`
Checks whether the CIDR instance is a locally administered (LAA) MAC
address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the MAC address sets the locally
administered bit  
**Example**  
```ucode
const mac = netaddr.new('02:C0:FF:EE:00:01');
mac.ismaclocal();  // true
```

#### range.ismacmcast() ⇒ `boolean`
Checks whether the CIDR instance is a multicast MAC address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if the MAC address sets the multicast bit  
**Example**  
```ucode
const mac = netaddr.new('01:00:5E:7F:00:10');
mac.ismacmcast();  // true
```

#### range.lower(addr) ⇒ `boolean`
Checks whether this CIDR instance is lower than the given argument.

The comparison follows these rules:

- An IPv4 address is always lower than an IPv6 address and IPv6
  addresses are considered lower than MAC addresses
- Prefix sizes are ignored

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if this CIDR is lower than the given
address, else `false`. Returns `null` if the argument cannot be
converted to a CIDR instance.  

| Param | Type | Description |
| --- | --- | --- |
| addr | `string` \| [`range`](#module_netaddr.range) | An `netaddr.range` instance or a string convertible by `new()` to compare against. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1');
addr.lower(addr);                         // false
addr.lower('10.10.10.10/24');             // false
addr.lower(netaddr.new('::1'));                // true
addr.lower(netaddr.new('192.168.200.1'));      // true
addr.lower(netaddr.new('00:14:22:01:23:45'));  // true
```

#### range.higher(addr) ⇒ `boolean`
Checks whether this CIDR instance is higher than the given argument.

The comparison follows these rules:

- An IPv4 address is always lower than an IPv6 address and IPv6
  addresses are considered lower than MAC addresses
- Prefix sizes are ignored

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if this CIDR is higher than the given
address, else `false`. Returns `null` if the argument cannot be
converted to a CIDR instance.  

| Param | Type | Description |
| --- | --- | --- |
| addr | `string` \| [`range`](#module_netaddr.range) | An `netaddr.range` instance or a string convertible by `new()` to compare against. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1');
addr.higher(addr);                        // false
addr.higher('10.10.10.10/24');            // true
addr.higher(netaddr.new('::1'));               // false
addr.higher(netaddr.new('192.168.200.1'));     // false
addr.higher(netaddr.new('00:14:22:01:23:45')); // false
```

#### range.equal(addr) ⇒ `boolean`
Checks whether this CIDR instance is equal to the given argument.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if this CIDR is equal to the given address,
else `false`. Returns `null` if the argument cannot be converted to a
CIDR instance.  

| Param | Type | Description |
| --- | --- | --- |
| addr | `string` \| [`range`](#module_netaddr.range) | An `netaddr.range` instance or a string convertible by `new()` to compare against. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1');
addr.equal(addr);                 // true
addr.equal('192.168.1.1');        // true
addr.equal(netaddr.new('::1'));        // false

const addr6 = netaddr.new('::1');
addr6.equal('0:0:0:0:0:0:0:1/64');  // true

const mac = netaddr.new('00:14:22:01:23:45');
mac.equal('0:14:22:1:23:45');  // true
```

#### range.prefix([mask]) ⇒ `number`
Get or set the prefix size of this CIDR instance.

If the optional mask parameter is given, the prefix size of this CIDR is
altered, else the current prefix size is returned.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `number` - The bit count of the (new) prefix size  

| Param | Type | Description |
| --- | --- | --- |
| [mask] | `number` \| `string` | A number containing the number of bits (`0..32` for IPv4, `0..128` for IPv6 or `0..48` for MAC addresses) or a string containing a valid netmask. |

**Example**  
```ucode
const range = netaddr.new('192.168.1.1/255.255.255.0');
range.prefix();  // 24

range.prefix(16);
range.prefix();  // 16

range.prefix('255.255.255.255');
range.prefix();  // 32
```

#### range.network([mask]) ⇒ [`range`](#module_netaddr.range)
Derive the network address of this CIDR instance.

Returns a new CIDR instance representing the network address of this
instance with all host parts masked out. The used prefix size can be
overridden by the optional mask parameter.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A CIDR instance representing the network
address  

| Param | Type | Description |
| --- | --- | --- |
| [mask] | `number` \| `string` | A number containing the number of bits (`0..32` for IPv4, `0..128` for IPv6 or `0..48` for MAC addresses) or a string containing a valid netmask. |

**Example**  
```ucode
const range = netaddr.new('192.168.62.243/255.255.0.0');
range.network();                // "192.168.0.0"
range.network(24);              // "192.168.62.0"
range.network('255.255.255.0'); // "192.168.62.0"

const range6 = netaddr.new('fd9b:62b3:9cc5:0:221:63ff:fe75:aa17/64');
range6.network();               // "fd9b:62b3:9cc5::"
```

#### range.mask([mask]) ⇒ [`range`](#module_netaddr.range)
Derive the netmask of this CIDR instance.

Constructs a CIDR instance representing the netmask of this instance.
The used prefix size can be overridden by the optional mask parameter.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A CIDR instance representing the netmask  

| Param | Type | Description |
| --- | --- | --- |
| [mask] | `number` \| `string` | A number containing the number of bits (`0..32` for IPv4, `0..128` for IPv6 or `0..48` for MAC addresses) or a string containing a valid netmask. |

**Example**  
```ucode
const range = netaddr.new('172.19.37.45/16');
range.mask();            // "255.255.0.0"
range.mask(24);          // "255.255.255.0"
range.mask('255.0.0.0'); // "255.0.0.0"
```

#### range.broadcast([mask]) ⇒ [`range`](#module_netaddr.range)
Derive the broadcast address of this CIDR instance.

Constructs a CIDR instance representing the broadcast address of this
instance. The used prefix size can be overridden by the optional mask
parameter.

This function has no effect on IPv6 or MAC address instances, it will
return `null` in this case.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the
broadcast address if this instance is an IPv4 range, else `null`  

| Param | Type | Description |
| --- | --- | --- |
| [mask] | `number` \| `string` | A number containing the number of bits (`0..32` for IPv4) or a string containing a valid netmask. |

**Example**  
```ucode
const range = netaddr.new('172.19.37.45/16');
range.broadcast();            // "172.19.255.255"
range.broadcast(24);          // "172.19.37.255"
range.broadcast('255.0.0.0'); // "172.255.255.255"
```

#### range.scoped() ⇒ [`range`](#module_netaddr.range)
Derive the scoped address of this CIDR instance.

Constructs a copy of the given IPv6 or MAC address instance carrying
the associated address scope, if any.

This function has no effect on IPv4 instances, it will return `null`
in this case. If no scope is associated with the address, `null` is
returned.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the
scoped address  
**Example**  
```ucode
const addr = netaddr.new('fe80::1234');
addr.scope = 2;
addr.scoped();  // "fe80::1234%eth0"  (if index 2 is eth0)
```

#### range.unscoped() ⇒ [`range`](#module_netaddr.range)
Derive the unscoped IPv6 address of this CIDR instance.

Constructs a copy of the given IPv6 CIDR instance and drops the
associated address scope information.

This function has no effect on IPv4 instances or MAC address instances,
it will return `null` in this case.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the
unscoped IPv6 address  
**Example**  
```ucode
const addr = netaddr.new('fe80::1234%eth0');
addr.unscoped();  // "fe80::1234"
```

#### range.tomac() ⇒ [`range`](#module_netaddr.range)
Derive the MAC address of this IPv6 link local CIDR instance.

Constructs a CIDR instance representing the MAC address contained in the
IPv6 link local address of this instance.

This function has no effect on IPv4 instances, MAC address instances or
IPv6 instances which are not a link local address, it will return `null`
in this case.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the MAC
address if this instance is an IPv6 link local address, else `null`  
**Example**  
```ucode
const addr = netaddr.new('fe80::6666:b3ff:fe47:e1b9');
addr.tomac();  // "64:66:B3:47:E1:B9"
```

#### range.tolinklocal() ⇒ [`range`](#module_netaddr.range)
Derive the IPv6 link local address from this MAC address CIDR instance.

Constructs a CIDR instance representing the IPv6 link local address of
the MAC address represented by this instance.

This function has no effect on IPv4 instances or IPv6 instances, it will
return `null` in this case.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the IPv6
link local address  
**Example**  
```ucode
const mac = netaddr.new('64:66:B3:47:E1:B9');
mac.tolinklocal();  // "fe80::6666:b3ff:fe47:e1b9"
```

#### range.contains(addr) ⇒ `boolean`
Test whether this CIDR contains the given range.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `boolean` - `true` if this instance fully contains the given
address, else `false`. Returns `null` if the argument cannot be
converted to a CIDR instance.  

| Param | Type | Description |
| --- | --- | --- |
| addr | `string` \| [`range`](#module_netaddr.range) | An `netaddr.range` instance or a string convertible by `new()` to test. |

**Example**  
```ucode
const range = netaddr.new('10.24.0.0/255.255.0.0');
range.contains('10.24.5.1');  // true
range.contains('::1');        // false
range.contains('10.0.0.0/8'); // false

const range6 = netaddr.new('fe80::/10');
range6.contains('fe80::221:63f:fe75:aa17/64');         // true
range6.contains('fd9b:6b3:c5:0:221:63f:fe75:aa17/64'); // false

const intel_macs = netaddr.MAC('C0:B6:F9:00:00:00/24');
intel_macs.contains('C0:B6:F9:A3:C:11');  // true
intel_macs.contains('64:66:B3:47:E1:B9'); // false
```

#### range.add(amount, [inplace]) ⇒ [`range`](#module_netaddr.range) \| `boolean` \| `null`
Add the given amount to this CIDR instance. If the result would overflow
the maximum address space, the result is set to the highest possible
address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) \| `boolean` \| `null` - When adding inplace: `true` if the addition succeeded or `false` when
the addition overflowed. When deriving a new CIDR: a new instance
representing the value of this instance plus the added amount or the
highest possible address if the addition overflowed the available
address space. Returns `null` if the amount argument is not
convertible.  

| Param | Type | Description |
| --- | --- | --- |
| amount | `number` \| `string` \| [`range`](#module_netaddr.range) | A numeric value, an `netaddr.range` instance or a string convertible by `new()`. |
| [inplace] | `boolean` | If `true`, modify this instance instead of returning a new derived CIDR instance. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1/24');
addr.add(250);          // "192.168.1.251/24"
addr.add('0.0.99.0');   // "192.168.100.1/24"

addr.add(256, true);    // true
addr;                   // "192.168.2.1/24"

addr.add('255.0.0.0', true);  // false (overflow)
addr;                         // "255.255.255.255/24"

const addr6 = netaddr.new('fe80::221:63f:fe75:aa17/64');
addr6.add(256);          // "fe80::221:63f:fe75:ab17/64"

const mac = netaddr.new('00:14:22:01:23:45');
mac.add(256);            // "00:14:22:01:24:45"
```

#### range.sub(amount, [inplace]) ⇒ [`range`](#module_netaddr.range) \| `boolean` \| `null`
Subtract the given amount from this CIDR instance. If the result would
underflow the lowest possible address, the result is set to the lowest
possible address.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) \| `boolean` \| `null` - When subtracting inplace: `true` if the subtraction succeeded or
`false` when the subtraction underflowed. When deriving a new CIDR: a
new instance representing the value of this instance minus the
subtracted amount or the lowest address if the subtraction underflowed.
Returns `null` if the amount argument is not convertible.  

| Param | Type | Description |
| --- | --- | --- |
| amount | `number` \| `string` \| [`range`](#module_netaddr.range) | A numeric value, an `netaddr.range` instance or a string convertible by `new()`. |
| [inplace] | `boolean` | If `true`, modify this instance instead of returning a new derived CIDR instance. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1/24');
addr.sub(256);         // "192.168.0.1/24"
addr.sub('0.168.0.0'); // "192.0.1.1/24"

addr.sub(256, true);   // true
addr;                  // "192.168.0.1/24"

addr.sub('255.0.0.0', true);  // false (underflow)
addr;                         // "0.0.0.0/24"

const addr6 = netaddr.new('fe80::221:63f:fe75:aa17/64');
addr6.sub(256);         // "fe80::221:63f:fe75:aa17/64"

const mac = netaddr.new('00:14:22:01:23:45');
mac.sub(256);           // "00:14:22:01:22:45"
```

#### range.minhost() ⇒ [`range`](#module_netaddr.range)
Derive the lowest usable host address of this CIDR instance.

For IPv4 ranges this is the network address plus one, except for
point-to-point `/31` ranges where the network address itself is the
first usable host; for IPv6 ranges the lowest address in the range
(the "network" address); for host addresses and MAC addresses the
address itself.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the lowest
usable host address of this instance  
**Example**  
```ucode
const range = netaddr.new('172.19.37.45/16');
range.minhost();  // "172.19.0.1"
```

#### range.maxhost() ⇒ [`range`](#module_netaddr.range)
Derive the highest usable host address of this CIDR instance.

For IPv4 ranges this is the broadcast address minus one, except for
point-to-point `/31` ranges where the broadcast address itself is the
last usable host; for IPv6 ranges the highest address in the range
(the "broadcast" address); for host addresses and MAC addresses the
address itself.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: [`range`](#module_netaddr.range) - A new CIDR instance representing the highest
usable host address of this instance  
**Example**  
```ucode
const range = netaddr.new('172.19.37.45/16');
range.maxhost();  // "172.19.255.254"
```

#### range.string() ⇒ `string`
Get the string representation of this CIDR instance.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `string` - A string representation of this CIDR  
**Example**  
```ucode
const addr = netaddr.new('172.19.37.45/16');
addr.string();  // "172.19.37.45/16"
```

#### range.tostring() ⇒ `string`
Get the string representation of this CIDR instance.

This method is invoked by `print()` and string interpolation to render
the instance, see [string()](#module_netaddr.range+string).

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `string` - A string representation of this CIDR  
**Example**  
```ucode
const addr = netaddr.new('172.19.37.45/16');

print(addr);   // "172.19.37.45/16"
`${addr}`;     // "172.19.37.45/16"
```

#### range.\_\_get\_\_(key) ⇒ `number` \| `string` \| `null`
Property access for `netaddr.range` instances.

Invoked by the interpreter for property reads which do not match a
method of this type, e.g. `addr[0]`, `addr.bits` or `addr.netmask`.

The following keys are supported:

| Key | Description |
| --- | --- |
| `0 .. n-1` | The individual address bytes, negative indices count from the end |
| `bits` | The prefix size in bits |
| `family` | The address family (`AF_INET`, `AF_INET6` or `AF_PACKET`) |
| `scope` | The address scope (numeric interface index) for IPv6 and MAC instances |
| `scopeid` | The address scope as an interface name (or `null` if not set) |
| `netmask` | The netmask as a string, e.g. `"255.255.255.0"` |
| `host` | The host address as a new range (full-width prefix) |
| `mapped4` | The mapped IPv4 address as a new range (or `null` if not a mapped IPv4) |
| `unscopename` | The interface name of the address scope (or an empty string) |
| `size` | The number of addresses in this range (or `null` if too large) |

**Kind**: instance method of [`range`](#module_netaddr.range)  

| Param | Type | Description |
| --- | --- | --- |
| key | `number` \| `string` | The property key to read. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1/24');

addr[0];       // 192
addr[-1];      // 1
addr.bits;     // 24
addr.family;   // 2
addr.netmask;  // "255.255.255.0"
addr.host;     // netaddr.range "192.168.1.1" (full-width prefix)
addr.size;     // 256
```

#### range.\_\_set\_\_(key, value) ⇒ `null`
Property assignment for `netaddr.range` instances.

Invoked by the interpreter for property writes, e.g. `addr[0] = 10` or
`addr.bits = 16`.

The following keys are supported:

- Numeric keys write the individual address bytes (value range `0..255`,
  negative indices count from the end of the address).
- The `bits` key sets the prefix size in bits (`0..32` for IPv4,
  `0..128` for IPv6, `0..48` for MAC addresses).
- The `scope` key sets the address scope (numeric interface index)
  for IPv6 and MAC address instances.
- The `scopeid` key sets the address scope to the given interface
  name or numeric index for IPv6 and MAC address instances.
- The `host`, `mapped4`, `unscopename` and `size` keys are read-only
  computed properties; writes to them are silently ignored.

Writes to other keys or with invalid values are silently ignored.

**Kind**: instance method of [`range`](#module_netaddr.range)  
**Returns**: `null` - Always returns `null`, the return value is discarded by
the interpreter.  

| Param | Type | Description |
| --- | --- | --- |
| key | `number` \| `string` | The property key to write. |
| value | `number` | The value to assign. |

**Example**  
```ucode
const addr = netaddr.new('192.168.1.1/24');

addr[3] = 10;     // "192.168.1.10/24"
addr[-1] = 10;    // "192.168.1.10/24"
addr.bits = 16;   // "192.168.1.10/16"
```
