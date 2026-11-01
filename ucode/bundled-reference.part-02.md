---
module: ucode
total_token_count: 17946
section_count: 3
is_monolithic: false
is_sharded_part: true
part_number: 2
part_count: 2
generated: '2026-11-01T18:18:06.554594+00:00'
---

# ucode Bundled Reference (Part 2 of 2)

> **Contains:** 3 documents
> **Tokens:** ~17946 (cl100k_base)
> **Index:** [./bundled-reference.md](./bundled-reference.md)

---

# ucode module: uci

> **Live docs:** https://ucode.mein.io/module-uci.html

---

## OpenWrt UCI configuration

The `uci` module provides access to the native OpenWrt
[libuci](https://github.com/openwrt/uci) API for reading and
manipulating UCI configuration files.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { cursor } from 'uci';

  let ctx = cursor();
  let hostname = ctx.get_first('system', 'system', 'hostname');
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as uci from 'uci';

  let ctx = uci.cursor();
  let hostname = ctx.get_first('system', 'system', 'hostname');
  ```

Additionally, the uci module namespace may also be imported by invoking
the `ucode` interpreter with the `-luci` switch.

### uci.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`uci`](#module_uci)  
**Example**  
```ucode
// Trigger error
const ctx = cursor();
ctx.set("not_existing_config", "test", "1");

// Print error (should yield "Entry not found")
print(ctx.error(), "\n");
```

### uci.cursor([config_dir], [delta_dir], [config2_dir], Parser) ⇒ [`cursor`](#module_uci.cursor)
Instantiate uci cursor.

A uci cursor is a context for interacting with uci configuration files. It's
purpose is to cache and hold changes made to loaded configuration states
until those changes are written out to disk or discared.

Unsaved and uncommitted changes in a cursor instance are private and not
visible to other cursor instances instantiated by the same program or other
processes on the system.

Returns the instantiated cursor on success.

Returns `null` on error, e.g. if an invalid path argument was provided.

**Kind**: instance method of [`uci`](#module_uci)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [config_dir] | `string` | `"/etc/config"` | The directory to search for configuration files. It defaults to the well known uci configuration directory `/etc/config` but may be set to a different path for special purpose applications. |
| [delta_dir] | `string` | `"/tmp/.uci"` | The directory to save delta records in. It defaults to the well known `/tmp/.uci` path which is used as default by the uci command line tool. By changing this path to a different location, it is possible to isolate uncommitted application changes from the uci cli or other processes on the system. |
| [config2_dir] | `string` | `"/var/run/uci"` | The directory to keep override config files in. Files are in the same format as in config_dir, but can individually override ones from that directory. It defaults to the uci configuration directory `/var/run/uci` but may be set to a different path for special purpose applications, or even disabled by setting this parameter to an empty string. |
| Parser | [`ParserFlags`](#module_uci.cursor.ParserFlags) |  | flags to change. |

### uci.cursor
**Kind**: static class of [`uci`](#module_uci)  
**See**: [cursor()](#module_uci+cursor)  

* [.cursor](#module_uci.cursor)
    * _instance_
        * [.load(config)](#module_uci.cursor+load) ⇒ `boolean`
        * [.unload(config)](#module_uci.cursor+unload) ⇒ `boolean`
        * [.get(config, section, [option])](#module_uci.cursor+get) ⇒ `string` \| `Array.<string>`
        * [.get_all(config, [section])](#module_uci.cursor+get_all) ⇒ `Object.<string, module:uci.cursor.SectionObject>` \| [`SectionObject`](#module_uci.cursor.SectionObject)
        * [.get_first(config, type, [option])](#module_uci.cursor+get_first) ⇒ `string` \| `Array.<string>`
        * [.add(config, type)](#module_uci.cursor+add) ⇒ `string`
        * [.set(config, section, option_or_type, [value])](#module_uci.cursor+set) ⇒ `boolean`
        * [.delete(config, section, [option])](#module_uci.cursor+delete) ⇒ `boolean`
        * [.list_append(config, section, option, value)](#module_uci.cursor+list_append) ⇒ `boolean`
        * [.list_remove(config, section, option, value)](#module_uci.cursor+list_remove) ⇒ `boolean`
        * [.rename(config, section, option_or_name, [name])](#module_uci.cursor+rename) ⇒ `boolean`
        * [.reorder(config, section, index)](#module_uci.cursor+reorder) ⇒ `boolean`
        * [.save([config])](#module_uci.cursor+save) ⇒ `boolean`
        * [.commit([config])](#module_uci.cursor+commit) ⇒ `boolean`
        * [.revert([config])](#module_uci.cursor+revert) ⇒ `boolean`
        * [.changes([config])](#module_uci.cursor+changes) ⇒ `Object.<string, Array.<module:uci.cursor.ChangeRecord>>`
        * [.foreach(config, type, callback)](#module_uci.cursor+foreach) ⇒ `boolean`
        * [.configs()](#module_uci.cursor+configs) ⇒ `Array.<string>`
        * [.error()](#module_uci.cursor+error) ⇒ `string`
    * _static_
        * [.ParserFlags](#module_uci.cursor.ParserFlags) : `Object`
        * [.ChangeRecord](#module_uci.cursor.ChangeRecord) : `Array.<string>`
        * [.SectionObject](#module_uci.cursor.SectionObject) : `Object.<string, (boolean\|number\|string\|Array.<string>)>`
        * [.SectionCallback](#module_uci.cursor.SectionCallback) : `function`

#### cursor.load(config) ⇒ `boolean`
Explicitly reload configuration file.

Usually, any attempt to query or modify a value within a given configuration
will implicitly load the underlying file into memory. By invoking `load()`
explicitly, a potentially loaded stale configuration is discarded and
reloaded from the file system, ensuring that the latest state is reflected in
the cursor.

Returns `true` if the configuration was successfully loaded.

Returns `null` on error, e.g. if the requested configuration does not exist.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to load, e.g. `"system"` to load `/etc/config/system` into the cursor. |

#### cursor.unload(config) ⇒ `boolean`
Explicitly unload configuration file.

The `unload()` function forcibly discards a loaded configuration state from
the cursor so that the next attempt to read or modify that configuration
will load it anew from the file system.

Returns `true` if the configuration was successfully unloaded.

Returns `false` if the configuration was not loaded to begin with.

Returns `null` on error, e.g. if the requested configuration does not exist.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to unload. |

#### cursor.get(config, section, [option]) ⇒ `string` \| `Array.<string>`
Query a single option value or section type.

When invoked with three arguments, the function returns the value of the
given option, within the specified section of the given configuration.

When invoked with just a config and section argument, the function returns
the type of the specified section.

In either case, the given configuration is implicitly loaded into the cursor
if not already present.

Returns the configuration value or section type on success.

Returns `null` on error, e.g. if the requested configuration does not exist
or if an invalid argument was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to query, e.g. `"system"` to query values in `/etc/config/system`. |
| section | `string` | The name of the section to query within the configuration. |
| [option] | `string` | The name of the option to query within the section. If omitted, the type of the section is returned instead. |

**Example**  
```text
const ctx = cursor(…);

// Query an option, extended section notation is supported
ctx.get('system', '@system[0]', 'hostname');

// Query a section type (should yield 'interface')
ctx.get('network', 'lan');
```

#### cursor.get\_all(config, [section]) ⇒ `Object.<string, module:uci.cursor.SectionObject>` \| [`SectionObject`](#module_uci.cursor.SectionObject)
Query a complete section or configuration.

When invoked with two arguments, the function returns all values of the
specified section within the given configuration as dictionary.

When invoked with just a config argument, the function returns a nested
dictionary of all sections present within the given configuration.

In either case, the given configuration is implicitly loaded into the cursor
if not already present.

Returns the section or configuration dictionary on success.

Returns `null` on error, e.g. if the requested configuration does not exist
or if an invalid argument was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to query, e.g. `"system"` to query values in `/etc/config/system`. |
| [section] | `string` | The name of the section to query within the configuration. If omitted a nested dictionary containing all section values is returned. |

**Example**  
```text
const ctx = cursor(…);

// Query all lan interface details
ctx.get_all('network', 'lan');

// Dump the entire dhcp configuration
ctx.get_all('dhcp');
```

#### cursor.get\_first(config, type, [option]) ⇒ `string` \| `Array.<string>`
Query option value or name of first section of given type.

When invoked with three arguments, the function returns the value of the
given option within the first found section of the specified type in the
given configuration.

When invoked with just a config and section type argument, the function
returns the name of the first found section of the given type.

In either case, the given configuration is implicitly loaded into the cursor
if not already present.

Returns the configuration value or section name on success.

Returns `null` on error, e.g. if the requested configuration does not exist
or if an invalid argument was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to query, e.g. `"system"` to query values in `/etc/config/system`. |
| type | `string` | The section type to find the first section for within the configuration. |
| [option] | `string` | The name of the option to query within the section. If omitted, the name of the section is returned instead. |

**Example**  
```text
const ctx = cursor(…);

// Query hostname in first anonymous "system" section of /etc/config/system
ctx.get_first('system', 'system', 'hostname');

// Figure out name of first network interface section (usually "loopback")
ctx.get_first('network', 'interface');
```

#### cursor.add(config, type) ⇒ `string`
Add anonymous section to given configuration.

Adds a new anonymous (unnamed) section of the specified type to the given
configuration. In order to add a named section, the three argument form of
`set()` should be used instead.

In contrast to other query functions, `add()` will not implicitly load the
configuration into the cursor. The configuration either needs to be loaded
explicitly through `load()` beforehand, or implicitly by querying it through
one of the `get()`, `get_all()`, `get_first()` or `foreach()` functions.

Returns the autogenerated, ephemeral name of the added unnamed section
on success.

Returns `null` on error, e.g. if the targeted configuration was not loaded or
if an invalid section type value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to add the section to, e.g. `"system"` to modify `/etc/config/system`. |
| type | `string` | The type value to use for the added section. |

**Example**  
```text
const ctx = cursor(…);

// Load firewall configuration
ctx.load('firewall');

// Add unnamed `config rule` section
const sid = ctx.add('firewall', 'rule');

// Set values on the newly added section
ctx.set('firewall', sid, 'name', 'A test');
ctx.set('firewall', sid, 'target', 'ACCEPT');
…
```

#### cursor.set(config, section, option_or_type, [value]) ⇒ `boolean`
Set option value or add named section in given configuration.

When invoked with four arguments, the function sets the value of the given
option within the specified section of the given configuration to the
provided value. A value of `""` (empty string) can be used to delete an
existing option.

When invoked with three arguments, the function adds a new named section to
the given configuration, using the specified type.

In either case, the given configuration is implicitly loaded into the cursor
if not already present.

Returns the `true` if the named section was added or the specified option was
set.

Returns `null` on error, e.g. if the targeted configuration was not found or
if an invalid value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to set values in, e.g. `"system"` to modify `/etc/config/system`. |
| section | `string` | The section name to create or set a value in. |
| option_or_type | `string` | The option name to set within the section or, when the subsequent value argument is omitted, the type of the section to create within the configuration. |
| [value] | `Array.<(string\|boolean\|number)>` \| `string` \| `boolean` \| `number` | The option value to set. |

**Example**  
```text
const ctx = cursor(…);

// Add named `config interface guest` section
ctx.set('network', 'guest', 'interface');

// Set values on the newly added section
ctx.set('network', 'guest', 'proto', 'static');
ctx.set('network', 'guest', 'ipaddr', '10.0.0.1/24');
ctx.set('network', 'guest', 'dns', ['8.8.4.4', '8.8.8.8']);
…

// Delete 'disabled' option in first wifi-iface section
ctx.set('wireless', '@wifi-iface[0]', 'disabled', '');
```

#### cursor.delete(config, section, [option]) ⇒ `boolean`
Delete an option or section from given configuration.

When invoked with three arguments, the function deletes the given option
within the specified section of the given configuration.

When invoked with two arguments, the function deletes the entire specified
section within the given configuration.

In either case, the given configuration is implicitly loaded into the cursor
if not already present.

Returns the `true` if specified option or section has been deleted.

Returns `null` on error, e.g. if the targeted configuration was not found or
if an invalid value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to delete values in, e.g. `"system"` to modify `/etc/config/system`. |
| section | `string` | The section name to remove the specified option in or, when the subsequent argument is omitted, the section to remove entirely. |
| [option] | `string` | The option name to remove within the section. |

**Example**  
```text
const ctx = cursor(…);

// Delete 'disabled' option in first wifi-iface section
ctx.delete('wireless', '@wifi-iface[0]', 'disabled');

// Delete 'wan' interface
ctx.delete('network', 'lan');

// Delete last firewall rule
ctx.delete('firewall', '@rule[-1]');
```

#### cursor.list\_append(config, section, option, value) ⇒ `boolean`
Add an item to a list option in given configuration.

Adds a single value to an existing list option within the specified section
of the given configuration. The configuration is implicitly loaded into the
cursor if not already present.

The new value is appended to the end of the list, maintaining the existing order.
No attempt is made to check for or remove duplicate values.

Returns `true` if the item was successfully added to the list.

Returns `null` on error, e.g. if the targeted option was not found or
if an invalid value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to modify, e.g. `"firewall"` to modify `/etc/config/firewall`. |
| section | `string` | The section name containing the list option to modify. |
| option | `string` | The list option name to add a value to. |
| value | `string` \| `boolean` \| `number` | The value to add to the list option. |

**Example**  
```text
const ctx = cursor(…);

// Add '192.168.1.1' to the 'dns' list in the 'lan' interface
ctx.add_list('network', 'lan', 'dns', '192.168.1.1');

// Add a port to the first redirect section
ctx.add_list('firewall', '@redirect[0]', 'src_dport', '8080');
```

#### cursor.list\_remove(config, section, option, value) ⇒ `boolean`
Remove an item from a list option in given configuration.

Removes a single value from an existing list option within the specified section
of the given configuration. The configuration is implicitly loaded into the
cursor if not already present.

If the specified value appears multiple times in the list, all matching occurrences
will be removed.

Returns `true` if the item was successfully removed from the list.

Returns `null` on error, e.g. if the targeted option was not foundor if an
invalid value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to modify, e.g. `"firewall"` to modify `/etc/config/firewall`. |
| section | `string` | The section name containing the list option to modify. |
| option | `string` | The list option name to remove a value from. |
| value | `string` \| `boolean` \| `number` | The value to remove from the list option. |

**Example**  
```text
const ctx = cursor(…);

// Remove '8.8.8.8' from the 'dns' list in the 'lan' interface
ctx.delete_list('network', 'lan', 'dns', '8.8.8.8');

// Remove a port from the first redirect section
ctx.delete_list('firewall', '@redirect[0]', 'src_dport', '8080');
```

#### cursor.rename(config, section, option_or_name, [name]) ⇒ `boolean`
Rename an option or section in given configuration.

When invoked with four arguments, the function renames the given option
within the specified section of the given configuration to the provided
value.

When invoked with three arguments, the function renames the entire specified
section to the provided value.

In either case, the given configuration is implicitly loaded into the cursor
if not already present.

Returns the `true` if specified option or section has been renamed.

Returns `null` on error, e.g. if the targeted configuration was not found or
if an invalid value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to rename values in, e.g. `"system"` to modify `/etc/config/system`. |
| section | `string` | The section name to rename or to rename an option in. |
| option_or_name | `string` | The option name to rename within the section or, when the subsequent name argument is omitted, the new name of the renamed section within the configuration. |
| [name] | `string` | The new name of the option to rename. |

**Example**  
```text
const ctx = cursor(…);

// Assign explicit name to last anonymous firewall rule section
ctx.rename('firewall', '@rule[-1]', 'my_block_rule');

// Rename 'server' to 'orig_server_list' in ntp section of system config
ctx.rename('system', 'ntp', 'server', 'orig_server_list');

// Rename 'wan' interface to 'external'
ctx.rename('network', 'wan', 'external');
```

#### cursor.reorder(config, section, index) ⇒ `boolean`
Reorder sections in given configuration.

The `reorder()` function moves a single section by repositioning it to the
given index within the configurations section list.

The given configuration is implicitly loaded into the cursor if not already
present.

Returns the `true` if specified section has been moved.

Returns `null` on error, e.g. if the targeted configuration was not found or
if an invalid value was passed.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The name of the configuration file to move the section in, e.g. `"system"` to modify `/etc/config/system`. |
| section | `string` | The section name to move. |
| index | `number` | The target index to move the section to, starting from `0`. |

**Example**  
```text
const ctx = cursor(…);

// Query whole firewall config and reorder resulting dict by type and name
const type_order = ['defaults', 'zone', 'forwarding', 'redirect', 'rule'];
const values = ctx.get_all('firewall');

sort(values, (k1, k2, s1, s2) => {
    // Get weight from type_order array
    let w1 = index(type_order, s1['.type']);
    let w2 = index(type_order, s2['.type']);

    // For unknown type orders, use type value itself as weight
    if (w1 == -1) w1 = s1['.type'];
    if (w2 == -1) w2 = s2['.type'];

    // Get name from name option, fallback to section name
    let n1 = s1.name ?? k1;
    let n2 = s2.name ?? k2;

    // Order by weight
    if (w1 < w2) return -1;
    if (w1 > w2) return 1;

    // For same weight order by name
    if (n1 < n2) return -1;
    if (n1 > n2) return 1;

    return 0;
});

// Sequentially reorder sorted sections in firewall configuration
let position = 0;

for (let sid in values)
  ctx.reorder('firewall', sid, position++);
```

#### cursor.save([config]) ⇒ `boolean`
Save accumulated cursor changes to delta directory.

The `save()` function writes consolidated changes made to in-memory copies of
loaded configuration files to the uci delta directory which effectively makes
them available to other processes using the same delta directory path as well
as the `uci changes` cli command when using the default delta directory.

Note that uci deltas are overlayed over the actual configuration file values
so they're reflected by `get()`, `foreach()` etc. even if the underlying
configuration files are not actually changed (yet). The delta records may be
either permanently merged into the configuration by invoking `commit()` or
reverted through `revert()` in order to restore the current state of the
underlying configuration file.

When the optional "config" parameter is omitted, delta records for all
currently loaded configuration files are written.

In case that neither sharing changes with other processes nor any revert
functionality is required, changes may be committed directly using `commit()`
instead, bypassing any delta record creation.

Returns the `true` if operation completed successfully.

Returns `null` on error, e.g. if the requested configuration was not loaded
or when a file system error occurred.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  
**See**

- [commit()](#module_uci.cursor+commit)
- [revert()](#module_uci.cursor+revert)

| Param | Type | Description |
| --- | --- | --- |
| [config] | `string` | The name of the configuration file to save delta records for, e.g. `"system"` to store changes for `/etc/config/system`. |

**Example**  
```text
const ctx = cursor(…);

ctx.set('wireless', '@wifi-iface[0]', 'disabled', '1');
ctx.save('wireless');
```

#### cursor.commit([config]) ⇒ `boolean`
Update configuration files with accumulated cursor changes.

The `commit()` function merges changes made to in-memory copies of loaded
configuration files as well as existing delta records in the cursors
configured delta directory and writes them back into the underlying
configuration files, persistently committing changes to the file system.

When the optional "config" parameter is omitted, all currently loaded
configuration files with either present delta records or yet unsaved
cursor changes are updated.

Returns the `true` if operation completed successfully.

Returns `null` on error, e.g. if the requested configuration was not loaded
or when a file system error occurred.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| [config] | `string` | The name of the configuration file to commit, e.g. `"system"` to update the `/etc/config/system` file. |

**Example**  
```text
const ctx = cursor(…);

ctx.set('system', '@system[0]', 'hostname', 'example.org');
ctx.commit('system');
```

#### cursor.revert([config]) ⇒ `boolean`
Revert accumulated cursor changes and associated delta records.

The `revert()` function discards any changes made to in-memory copies of
loaded configuration files and discards any related existing delta records in
the  cursors configured delta directory.

When the optional "config" parameter is omitted, all currently loaded
configuration files with either present delta records or yet unsaved
cursor changes are reverted.

Returns the `true` if operation completed successfully.

Returns `null` on error, e.g. if the requested configuration was not loaded
or when a file system error occurred.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  
**See**: [save()](#module_uci.cursor+save)  

| Param | Type | Description |
| --- | --- | --- |
| [config] | `string` | The name of the configuration file to revert, e.g. `"system"` to discard any changes for the `/etc/config/system` file. |

**Example**  
```text
const ctx = cursor(…);

ctx.set('system', '@system[0]', 'hostname', 'example.org');
ctx.revert('system');
```

#### cursor.changes([config]) ⇒ `Object.<string, Array.<module:uci.cursor.ChangeRecord>>`
Enumerate pending changes.

The `changes()` function returns a list of change records for currently
loaded configuration files, originating both from the cursors associated
delta directory and yet unsaved cursor changes.

When the optional "config" parameter is specified, the requested
configuration is implicitly loaded if it is not already loaded into the
cursor.

Returns a dictionary of change record arrays, keyed by configuration name.

Returns `null` on error, e.g. if the requested configuration could not be
loaded.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| [config] | `string` | The name of the configuration file to enumerate changes for, e.g. `"system"` to query pending changes for the `/etc/config/system` file. |

**Example**  
```text
const ctx = cursor(…);

// Enumerate changes for all currently loaded configurations
const deltas = ctx.changes();

// Explicitly load and enumerate changes for the "system" configuration
const deltas = ctx.changes('system');
```

#### cursor.foreach(config, type, callback) ⇒ `boolean`
Iterate configuration sections.

The `foreach()` function iterates all sections of the given configuration,
optionally filtered by type, and invokes the given callback function for
each encountered section.

When the optional "type" parameter is specified, the callback is only invoked
for sections of the given type, otherwise it is invoked for all sections.

The requested configuration is implicitly loaded into the cursor.

Returns `true` if the callback was executed successfully at least once.

Returns `false` if the callback was never invoked, e.g. when the
configuration is empty or contains no sections of the given type.

Returns `null` on error, e.g. when an invalid callback was passed or the
requested configuration not found.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| config | `string` | The configuration to iterate sections for, e.g. `"system"` to read the `/etc/config/system` file. |
| type | `string` | Invoke the callback only for sections of the specified type. |
| callback | [`SectionCallback`](#module_uci.cursor.SectionCallback) | The callback to invoke for each section, will receive a section dictionary as sole argument. |

**Example**  
```text
const ctx = cursor(…);

// Iterate all network interfaces
ctx.foreach('network', 'interface',
	   section => print(`Have interface ${section[".name"]}\n`));
```

#### cursor.configs() ⇒ `Array.<string>`
Enumerate existing configurations.

The `configs()` function yields an array of configuration files present in
the cursors associated configuration directory, `/etc/config/` by default.

Returns an array of configuration names on success.

Returns `null` on error, e.g. due to filesystem errors.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  
**Example**  
```text
const ctx = cursor(…);

// Enumerate all present configuration file names
const configurations = ctx.configs();
```

#### cursor.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`cursor`](#module_uci.cursor)  
**Example**  
```ucode
// Trigger error
const ctx = cursor();
ctx.set("not_existing_config", "test", "1");

// Print error (should yield "Entry not found")
print(ctx.error(), "\n");
```

#### cursor.ParserFlags : `Object`
**Kind**: static typedef of [`cursor`](#module_uci.cursor)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| strict | `boolean` | Strict parsing mode (enabled by default). Aborts parsing when encountering a parser error. |
| print_errors | `boolean` | Print parser errors to stderr. |

#### cursor.ChangeRecord : `Array.<string>`
A uci change record is a plain array containing the change operation name as
first element, the affected section ID as second argument and an optional
third and fourth argument whose meanings depend on the operation.

**Kind**: static typedef of [`cursor`](#module_uci.cursor)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| 0 | `string` | The operation name - may be one of `add`, `set`, `remove`, `order`, `list-add`, `list-del` or `rename`. |
| 1 | `string` | The section ID targeted by the operation. |
| 2 | `string` | The meaning of the third element depends on the operation. - For `add` it is type of the section that has been added - For `set` it either is the option name if a fourth element exists, or the   type of a named section which has been added when the change entry only   contains three elements. - For `remove` it contains the name of the option that has been removed. - For `order` it specifies the new sort index of the section. - For `list-add` it contains the name of the list option a new value has been   added to. - For `list-del` it contains the name of the list option a value has been   removed from. - For `rename` it contains the name of the option that has been renamed if a   fourth element exists, else it contains the new name a section has been   renamed to if the change entry only contains three elements. |
| 4 | `string` | The meaning of the fourth element depends on the operation. - For `set` it is the value an option has been set to. - For `list-add` it is the new value that has been added to a list option. - For `rename` it is the new name of an option that has been renamed. |

#### cursor.SectionObject : `Object.<string, (boolean\|number\|string\|Array.<string>)>`
A section object represents the options and their corresponding values
enclosed within a configuration section, as well as some additional meta data
such as sort indexes and internal ID.

Any internal metadata fields are prefixed with a dot which isn't an allowed
character for normal option names.

**Kind**: static typedef of [`cursor`](#module_uci.cursor)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| .anonymous | `boolean` | The `.anonymous` property specifies whether the configuration is anonymous (`true`) or named (`false`). |
| .index | `number` | The `.index` property specifies the sort order of the section. |
| .name | `string` | The `.name` property holds the name of the section object. It may be either an anonymous ID in the form `cfgXXXXXX` with `X` being a hexadecimal digit or a string holding the name of the section. |
| .type | `string` | The `.type` property contains the type of the corresponding uci section. |
| * | `string` \| `Array.<string>` | A section object may contain an arbitrary number of further properties representing the uci option enclosed in the section. All option property names will be in the form `[A-Za-z0-9_]+` and either contain a string value or an array of strings, in case the underlying option is an UCI list. |

#### cursor.SectionCallback : `function`
The sections callback is invoked for each section found within the given
configuration and receives the section object and its associated name as
arguments.

**Kind**: static typedef of [`cursor`](#module_uci.cursor)  

| Param | Type | Description |
| --- | --- | --- |
| section | [`SectionObject`](#module_uci.cursor.SectionObject) | The section object. |

---

# ucode module: uloop

> **Live docs:** https://ucode.mein.io/module-uloop.html

---

## OpenWrt uloop event loop

The `uloop` binding provides functions for integrating with the OpenWrt
[uloop library](https://github.com/openwrt/libubox/blob/master/uloop.h).

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```text
  import { init, handle, timer, interval, process, signal, task, run } from 'uloop';

  init();

  handle(…);
  timer(…);
  interval(…);
  process(…);
  signal(…);
  task(…);

  run();
  ```

Alternatively, the module namespace can be imported using a wildcard import
statement:

  ```text
  import * as uloop from 'uloop';

  uloop.init();

  uloop.handle(…);
  uloop.timer(…);
  uloop.interval(…);
  uloop.process(…);
  uloop.signal(…);
  uloop.task(…);

  uloop.run();
  ```

Additionally, the uloop binding namespace may also be imported by invoking
the `ucode` interpreter with the `-luloop` switch.

### uloop.error() ⇒ `string`
Retrieves the last error message.

This function retrieves the last error message generated by the uloop event loop.
If no error occurred, it returns `null`.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `string` - Returns the last error message as a string, or `null` if no error occurred.  
**Example**  
```ucode
// Retrieve the last error message
const errorMessage = uloop.error();

if (errorMessage)
    printf(`Error message: ${errorMessage}\n`);
else
    printf("No error occurred\n");
```

### uloop.init() ⇒ `boolean`
Initializes the uloop event loop.

This function initializes the uloop event loop, allowing subsequent
usage of uloop functionalities. It takes no arguments.

Returns `true` on success.
Returns `null` if an error occurred during initialization.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `boolean` - Returns `true` on success, `null` on error.  
**Example**  
```ucode
// Initialize the uloop event loop
const success = uloop.init();

if (success)
    printf("uloop event loop initialized successfully\n");
else
    die(`Initialization failure: ${uloop.error()}\n`);
```

### uloop.run([timeout]) ⇒ `number`
Runs the uloop event loop.

This function starts running the uloop event loop, allowing it to handle
scheduled events and callbacks. If a timeout value is provided and is
non-negative, the event loop will run for that amount of milliseconds
before returning. If the timeout is omitted or negative, the event loop
runs indefinitely until explicitly stopped.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `number` - Returns a signal number or 0 on success, `null` on error.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [timeout] | `number` | `-1` | Optional. The timeout value in milliseconds for running the event loop. Defaults to -1, indicating an indefinite run. |

**Example**  
```ucode
// Run the uloop event loop indefinitely
const success = uloop.run();
if (rc == null)
    die(`Error occurred during uloop execution: ${uloop.error()}\n`);
else if (rc != 0)
    printf("uloop event loop was interrupted by a signal: %d\n", rc);

// Run the uloop event loop for 1000 milliseconds
const success = uloop.run(1000);
if (rc == null)
    die(`Error occurred during uloop execution: ${uloop.error()}\n`);
else if (rc != 0)
    printf("uloop event loop was interrupted by a signal: %d\n", rc);
```

### uloop.cancelling() ⇒ `boolean`
Checks if the uloop event loop is currently shutting down.

This function checks whether the uloop event loop is currently in the process
of shutting down.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `boolean` - Returns `true` if uloop is currently shutting down, `false` otherwise.  
**Example**  
```ucode
// Check if the uloop event loop is shutting down
const shuttingDown = uloop.cancelling();
if (shuttingDown)
    printf("uloop event loop is currently shutting down\n");
else
    printf("uloop event loop is not shutting down\n");
```

### uloop.running() ⇒ `boolean`
Checks if the uloop event loop is currently running.

This function checks whether the uloop event loop is currently started
and running.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `boolean` - Returns `true` if the event loop is currently running, `false` otherwise.  
**Example**  
```ucode
// Check if the uloop event loop is running
const isRunning = uloop.running();
if (isRunning)
    printf("uloop event loop is currently running\n");
else
    printf("uloop event loop is not running\n");
```

### uloop.end() ⇒ `void`
Halts the uloop event loop.

This function halts the uloop event loop, stopping its execution and
preventing further processing of scheduled events and callbacks.

Expired timeouts and already queued event callbacks are still run to
completion.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `void` - This function does not return any value.  
**Example**  
```ucode
// Halt the uloop event loop
uloop.end();
```

### uloop.done() ⇒ `void`
Stops the uloop event loop and cancels pending timeouts and events.

This function immediately stops the uloop event loop, cancels all pending
timeouts and events, unregisters all handles, and deallocates associated
resources.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: `void` - This function does not return any value.  
**Example**  
```ucode
// Stop the uloop event loop and clean up resources
uloop.done();
```

### uloop.timer([timeout], callback) ⇒ [`timer`](#module_uloop.timer)
Creates a timer instance for scheduling callbacks.

This function creates a timer instance for scheduling callbacks to be
executed after a specified timeout duration. It takes an optional timeout
parameter, which defaults to -1, indicating that the timer is initially not
armed and can be enabled later by invoking the `.set(timeout)` method on the
instance.

A callback function must be provided to be executed when the timer expires.

While the timer is armed, the event loop keeps it alive. Once it expired
and the callback did not rearm it, the timer is freed as soon as the script
no longer refers to it; a retained instance can be rearmed with
`.set(timeout)`.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: [`timer`](#module_uloop.timer) - Returns a timer instance for scheduling callbacks.
Returns `null` when the timeout or callback arguments are invalid.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [timeout] | `number` | `-1` | Optional. The timeout duration in milliseconds. Defaults to -1, indicating the timer is not initially armed. |
| callback | `function` |  | The callback function to be executed when the timer expires. |

**Example**  
```ucode
// Create a timer with a callback to be executed after 1000 milliseconds
const myTimer = uloop.timer(1000, () => {
    printf("Timer expired!\n");
});

// Later enable the timer with a timeout of 500 milliseconds
myTimer.set(500);
```

### uloop.handle(handle, callback, events) ⇒ [`handle`](#module_uloop.handle)
Creates a handle instance for monitoring file descriptor events.

This function creates a handle instance for monitoring events on a file
descriptor, file, or socket. It takes the file or socket handle, a callback
function to be invoked when the specified IO events occur, and bitwise OR-ed
flags of IO events (`ULOOP_READ`, `ULOOP_WRITE`, `ULOOP_PRIORITY`) that the
callback should be invoked for.

Unless `ULOOP_ERROR_CB` is given, the event loop removes the descriptor on
an error or hangup and invokes the callback a last time. The handle is
then freed as soon as the script no longer refers to it.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: [`handle`](#module_uloop.handle) - Returns a handle instance for monitoring file descriptor events.
Returns `null` when the handle, callback or signal arguments are invalid.  

| Param | Type | Description |
| --- | --- | --- |
| handle | `number` \| `module:fs.file` \| `module:fs.proc` \| `module:socket.socket` \| `module:io.handle` | The file handle (descriptor number, file or socket instance). |
| callback | `function` | The callback function to be invoked when the specified IO events occur. |
| events | `number` | Bitwise OR-ed flags of IO events (`ULOOP_READ`, `ULOOP_WRITE`, `ULOOP_PRIORITY`) that the callback should be invoked for. At least one IO event is required; mode flags such as `ULOOP_ERROR_CB` alone are rejected. |

**Example**  
```ucode
// Create a handle for monitoring read events on file descriptor 3
const myHandle = uloop.handle(3, (events) => {
    if (events & ULOOP_READ)
        printf("Read event occurred!\n");
}, uloop.ULOOP_READ);

// Check socket for writability
const sock = socket.connect("example.org", 80);
uloop.handle(sock, (events) => {
    sock.send("GET / HTTP/1.0\r\n\r\n");
}, uloop.ULOOP_WRITE)
```

### uloop.process(executable, [args], [env], callback) ⇒ [`process`](#module_uloop.process)
Creates a process instance for executing external programs.

This function creates a process instance for executing external programs.
It takes the executable path string, an optional string array as the argument
vector, an optional dictionary describing environment variables, and a
callback function to be invoked when the invoked process ends.

When a function is given instead of the executable path, it is invoked in
the child process after fork(), receiving the argument vector and the
environment dictionary as parameters. It may perform any preparatory work,
such as setting up file descriptors, and must return the complete argument
vector to execute, with the executable path as first element. Changes made
to the environment dictionary by the function apply to the environment of
the executed program; the executable is searched in the `PATH` of the
calling process. If the function calls `exit()`, the child process exits
with the given code. If it throws an exception or does not return a
non-empty array, the child process exits with code 255.

The function runs outside of the event loop: signals received by the child
process do not invoke the signal callbacks of the event loop.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: [`process`](#module_uloop.process) - Returns a process instance for executing external programs.
Returns `null` on invalid arguments or `fork()` failure. If the program
cannot be executed, the callback receives the exit code 255.  

| Param | Type | Description |
| --- | --- | --- |
| executable | `string` \| `function` | The path to the executable program, or a function returning the argument vector to execute. |
| [args] | `Array.<string>` | Optional. An array of strings representing the arguments passed to the executable, or to the function. |
| [env] | `Object.<string, \*>` | Optional. A dictionary describing environment variables for the process. |
| callback | `function` | The callback function to be invoked when the invoked process ends. Receives the exit code for a normally exited process, or the negative signal number if the process was terminated by a signal. |

**Example**  
```ucode
// Create a process instance for executing 'ls' command
const myProcess = uloop.process("/bin/ls", ["-l", "/tmp"], null, (code) => {
    printf(`Process exited with code ${code}\n`);
});

// Redirect stderr in the child process before executing 'ls'
const myProcess = uloop.process((args, env) => {
    const fs = require('fs');
    const errlog = fs.open('/tmp/error.log', 'w');
    fs.dup2(errlog.fileno(), 2);
    errlog.close();

    return ["/bin/ls", ...args];
}, ["-l", "/tmp"], null, (code) => {
    printf(`Process exited with code ${code}\n`);
});
```

### uloop.task(taskFunction, [outputCallback], [inputCallback]) ⇒ [`task`](#module_uloop.task)
Creates a task instance for executing background tasks.

This function creates a task instance for executing background tasks.
It takes the task function to be invoked as a background process,
an optional output callback function to be invoked when output is received
from the task, and an optional input callback function to be invoked
when input is required by the task.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: [`task`](#module_uloop.task) - Returns a task instance for executing background tasks.
Returns `null` on error, e.g. due to fork failure or invalid arguments.  

| Param | Type | Description |
| --- | --- | --- |
| taskFunction | `function` | The task function to be invoked as a background process. |
| [outputCallback] | `function` | Optional. The output callback function to be invoked when output is received from the task. It is invoked with the output data as the argument. |
| [inputCallback] | `function` | Optional. The input callback function to be invoked when input is required by the task. It is invoked with a function to send input to the task as the argument. |

**Example**  
```ucode
// Create a task instance for executing a background task
const myTask = uloop.task(
    (pipe) => {
        // Task logic
        pipe.send("Hello from the task\n");
        const input = pipe.receive();
        printf(`Received input from main thread: ${input}\n`);
    },
    (output) => {
        // Output callback, invoked when task function calls pipe.send()
        printf(`Received output from task: ${output}\n`);
    },
    () => {
        // Input callback, invoked when task function calls pipe.receive()
        return "Input from main thread\n";
    }
);
```

### uloop.interval([timeout], callback) ⇒ [`interval`](#module_uloop.interval)
Creates an interval instance for scheduling repeated callbacks.

This function creates an interval instance for scheduling repeated callbacks
to be executed at regular intervals. It takes an optional timeout parameter,
which defaults to -1, indicating that the interval is initially not armed
and can be armed later with the `.set(timeout)` method. A callback function
must be provided to be executed when the interval expires.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: [`interval`](#module_uloop.interval) - Returns an interval instance for scheduling repeated callbacks.
Returns `null` when the timeout or callback arguments are invalid.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [timeout] | `number` | `-1` | Optional. The interval duration in milliseconds. Defaults to -1, indicating the interval is not initially armed. A zero or negative value also leaves the interval unarmed. |
| callback | `function` |  | The callback function to be executed when the interval expires. |

**Example**  
```ucode
// Create an interval with a callback to be executed every 1000 milliseconds
const myInterval = uloop.interval(1000, () => {
    printf("Interval callback executed!\n");
});

// Later arm the interval to start executing the callback every 500 milliseconds
myInterval.set(500);
```

### uloop.signal(signal, callback) ⇒ [`signal`](#module_uloop.signal)
Creates a signal instance for handling Unix signals.

This function creates a signal instance for handling Unix signals.
It takes the signal name string (with or without "SIG" prefix) or signal
number, and a callback function to be invoked when the specified Unix signal
is caught.

**Kind**: instance method of [`uloop`](#module_uloop)  
**Returns**: [`signal`](#module_uloop.signal) - Returns a signal instance representing the installed signal handler.
Returns `null` when the signal or callback arguments are invalid.  

| Param | Type | Description |
| --- | --- | --- |
| signal | `string` \| `number` | The signal name string (with or without "SIG" prefix) or signal number. |
| callback | `function` | The callback function to be invoked when the specified Unix signal is caught. |

**Example**  
```ucode
// Create a signal instance for handling SIGINT
const mySignal = uloop.signal("SIGINT", () => {
    printf("SIGINT caught!\n");
});
```

### uloop.timer
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [timer()](#module_uloop+timer)  

* [.timer](#module_uloop.timer)
    * [.set([timeout])](#module_uloop.timer+set) ⇒ `boolean`
    * [.remaining()](#module_uloop.timer+remaining) ⇒ `number`
    * [.cancel()](#module_uloop.timer+cancel) ⇒ `boolean`

#### timer.set([timeout]) ⇒ `boolean`
Rearms the uloop timer with the specified timeout.

This method rearms the uloop timer with the specified timeout value,
allowing it to trigger after the specified amount of time. A zero or
negative timeout expires the timer on the next event loop iteration. If no
timeout value or `null` is provided, the timer is disarmed and keeps its
callback, so that a later call can rearm it.

**Kind**: instance method of [`timer`](#module_uloop.timer)  
**Returns**: `boolean` - Returns `true` on success, `null` on error, such as an invalid timeout argument.  

| Param | Type | Description |
| --- | --- | --- |
| [timeout] | `number` | Optional. The timeout value in milliseconds until the timer expires. Without a value, the timer is disarmed. |

**Example**  
```text
const timeout = uloop.timer(…);

// Rearm the uloop timer with a timeout of 1000 milliseconds
timeout.set(1000);

// Disable the uloop timer
timeout.set();
```

#### timer.remaining() ⇒ `number`
Returns the number of milliseconds until the uloop timer expires.

This method returns the remaining time until the uloop timer expires. If
the timer is not armed (i.e., disabled), it returns -1.

**Kind**: instance method of [`timer`](#module_uloop.timer)  
**Returns**: `number` - The number of milliseconds until the timer expires, or -1 if the timer is not armed.  
**Example**  
```ucode
// Get the remaining time until the uloop timer expires (~500ms)
const remainingTime = timer.remaining();
if (remainingTime !== -1)
    printf("Time remaining until timer expires: %d ms\n", remainingTime);
else
    printf("Timer is not armed\n");
```

#### timer.cancel() ⇒ `boolean`
Cancels the uloop timer, disarming it and removing it from the event loop.

This method destroys the uloop timer and releases its associated resources.
Calling it on a timer that already fired is not required; the timer then
only drops its callback and returns `false`.

**Kind**: instance method of [`timer`](#module_uloop.timer)  
**Returns**: `boolean` - Returns `true` on success.  
**Example**  
```ucode
// Cancel the uloop timer
timer.cancel();
```

### uloop.handle
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [handle()](#module_uloop+handle)  

* [.handle](#module_uloop.handle)
    * [.fileno()](#module_uloop.handle+fileno) ⇒ `number`
    * [.handle()](#module_uloop.handle+handle) ⇒ `module:fs.file` \| `module:fs.proc` \| `module:socket.socket`
    * [.delete()](#module_uloop.handle+delete) ⇒ `void`

#### handle.fileno() ⇒ `number`
Returns the file descriptor number.

This method returns the file descriptor number associated with the underlying
handle, which might refer to a socket or file instance.

**Kind**: instance method of [`handle`](#module_uloop.handle)  
**Returns**: `number` - The file descriptor number associated with the handle.  
**Example**  
```ucode
// Get the file descriptor number associated with the uloop handle
const fd = handle.fileno();
printf("File descriptor number: %d\n", fd);
```

#### handle.handle() ⇒ `module:fs.file` \| `module:fs.proc` \| `module:socket.socket`
Returns the underlying file or socket instance.

This method returns the underlying file or socket instance associated with
the uloop handle.

**Kind**: instance method of [`handle`](#module_uloop.handle)  
**Returns**: `module:fs.file` \| `module:fs.proc` \| `module:socket.socket` - The underlying file or socket instance associated with the handle.  
**Example**  
```ucode
// Get the associated file or socket instance
const fileOrSocket = handle.handle();
printf("Handle: %s\n", fileOrSocket); // e.g. <socket 0x5> or <fs.proc …>
```

#### handle.delete() ⇒ `void`
Unregisters the uloop handle.

This method unregisters the uloop handle from the uloop event loop and frees
any associated resources. After calling this method, the handle instance
should no longer be used.

Call this method before closing the underlying descriptor. The event loop
does not notice a closed descriptor and keeps the handle alive until it
is deleted.

A handle knows its descriptor only by number, device and inode, and checks
them when it is deleted. A handle whose descriptor was closed is disabled
for good once the check fails, once uloop rejects the removal, or once
another handle is created on the same number. It then stays allocated and
ignores events. If the number was reused for the same file opened anew, for
example the same path or device node, and a watcher outside of this module,
such as the application that embeds ucode, watches it, the check cannot
tell the two files apart, and deleting the old handle removes the other
watcher's entry.

**Kind**: instance method of [`handle`](#module_uloop.handle)  
**Returns**: `void` - This function does not return a value.  
**Example**  
```ucode
// Unregister the uloop handle and free associated resources
handle.delete();
printf("Handle deleted successfully\n");
```

### uloop.process
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [process()](#module_uloop+process)  

* [.process](#module_uloop.process)
    * [.pid()](#module_uloop.process+pid) ⇒ `number`
    * [.delete()](#module_uloop.process+delete) ⇒ `boolean`

#### process.pid() ⇒ `number`
Returns the process ID.

This method returns the process ID (PID) of the operating system process
launched by {@link module:uloop#process|process().

**Kind**: instance method of [`process`](#module_uloop.process)  
**Returns**: `number` - The process ID (PID) of the associated launched process.  
**Example**  
```text
const proc = uloop.process(…);

printf("Process ID: %d\n", proc.pid());
```

#### process.delete() ⇒ `boolean`
Unregisters the process from uloop.

This method unregisters the process from the uloop event loop and releases
any associated resources. However, note that the operating system process
itself is not terminated by this method.

**Kind**: instance method of [`process`](#module_uloop.process)  
**Returns**: `boolean` - Returns `true` on success.  
**Example**  
```text
const proc = uloop.process(…);

proc.delete();
```

### uloop.pipe
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [task()](#module_uloop+task)  

* [.pipe](#module_uloop.pipe)
    * [.send(msg)](#module_uloop.pipe+send) ⇒ `boolean`
    * [.receive()](#module_uloop.pipe+receive) ⇒ `\*`
    * [.sending()](#module_uloop.pipe+sending) ⇒ `boolean`
    * [.receiving()](#module_uloop.pipe+receiving) ⇒ `boolean`

#### pipe.send(msg) ⇒ `boolean`
Sends a serialized message to the task handle.

This method serializes the provided message and sends it over the task
communication pipe. In the main thread, the message is deserialized and
passed as an argument to the output callback function registered with the
task handle.

**Kind**: instance method of [`pipe`](#module_uloop.pipe)  
**Returns**: `boolean` - Returns `true` on success, indicating that the message was successfully sent
over the pipe. Returns `null` on error, such as when there's no output
callback registered with the task handle.  

| Param | Type | Description |
| --- | --- | --- |
| msg | `\*` | The message to be serialized and sent over the pipe. It can be of arbitrary type. |

**Example**  
```ucode
// Send a message over the uloop pipe
const success = pipe.send(message);

if (success)
    printf("Message sent successfully\n");
else
    die(`Error sending message: ${uloop.error()}\n`);
```

#### pipe.receive() ⇒ `\*`
Reads input from the task handle.

This method reads input from the task communication pipe. The input callback
function registered with the task handle is invoked to return the input data,
which is then serialized, sent over the pipe, and deserialized by the receive
method.

**Kind**: instance method of [`pipe`](#module_uloop.pipe)  
**Returns**: `\*` - Returns the deserialized message read from the task communication pipe.
Returns `null` on error, such as when there's no input callback registered
on the task handle.  
**Example**  
```ucode
// Read input from the task communication pipe
const message = pipe.receive();

if (message !== null)
    printf("Received message: %s\n", message);
else
    die(`Error receiving message: ${uloop.error()}\n`);
```

#### pipe.sending() ⇒ `boolean`
Checks if the task handle provides input.

This method checks if the task handle has an input callback  registered.
It returns a boolean value indicating whether an input callback is present.

**Kind**: instance method of [`pipe`](#module_uloop.pipe)  
**Returns**: `boolean` - Returns `true` if the remote task handle has an input callback
registered, otherwise returns `false`.  
**Example**  
```ucode
// Check if the remote task handle has an input callback
const hasInputCallback = pipe.sending();

if (hasInputCallback)
    printf("Input callback is registered on task handle\n");
else
    printf("No input callback on the task handle\n");
```

#### pipe.receiving() ⇒ `boolean`
Checks if the task handle reads output.

This method checks if the task handle has an output callback registered.
It returns a boolean value indicating whether an output callback is present.

**Kind**: instance method of [`pipe`](#module_uloop.pipe)  
**Returns**: `boolean` - Returns `true` if the task handle has an output callback registered,
otherwise returns `false`.  
**Example**  
```ucode
// Check if the task handle has an output callback
const hasOutputCallback = pipe.receiving();

if (hasOutputCallback)
    printf("Output callback is registered on task handle\n");
else
    printf("No output callback on the task handle\n");
```

### uloop.task
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [task()](#module_uloop+task)  

* [.task](#module_uloop.task)
    * [.pid()](#module_uloop.task+pid) ⇒ `number`
    * [.kill()](#module_uloop.task+kill) ⇒ `boolean`
    * [.finished()](#module_uloop.task+finished) ⇒ `boolean`

#### task.pid() ⇒ `number`
Returns the process ID.

This method returns the process ID (PID) of the underlying forked process
launched by {@link module:uloop#task|task().

**Kind**: instance method of [`task`](#module_uloop.task)  
**Returns**: `number` - The process ID (PID) of the forked task process.  
**Example**  
```text
const task = uloop.task(…);

printf("Process ID: %d\n", task.pid());
```

#### task.kill() ⇒ `boolean`
Terminates the task process.

This method terminates the task process. It sends a termination signal to
the task process, causing it to exit. Returns `true` on success, indicating
that the task process was successfully terminated. Returns `null` on error,
such as when the task process has already terminated.

**Kind**: instance method of [`task`](#module_uloop.task)  
**Returns**: `boolean` - Returns `true` when the task process was successfully terminated.
Returns `null` on error, such as when the process has already terminated.  
**Example**  
```ucode
// Terminate the task process
const success = task.kill();

if (success)
    printf("Task process terminated successfully\n");
else
    die(`Error terminating task process: ${uloop.error()}\n`);
```

#### task.finished() ⇒ `boolean`
Checks if the task ran to completion.

This method checks if the task function has already run to completion.
It returns a boolean value indicating whether the task function has finished
executing.

**Kind**: instance method of [`task`](#module_uloop.task)  
**Returns**: `boolean` - Returns `true` if the task function has already run to completion, otherwise
returns `false`.  
**Example**  
```ucode
// Check if the task function has finished executing
const isFinished = task.finished();

if (isFinished)
    printf("Task function has finished executing\n");
else
    printf("Task function is still running\n");
```

### uloop.interval
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [interval()](#module_uloop+interval)  

* [.interval](#module_uloop.interval)
    * [.set([interval])](#module_uloop.interval+set) ⇒ `boolean`
    * [.remaining()](#module_uloop.interval+remaining) ⇒ `number`
    * [.expirations()](#module_uloop.interval+expirations) ⇒ `number`
    * [.cancel()](#module_uloop.interval+cancel) ⇒ `boolean`

#### interval.set([interval]) ⇒ `boolean`
Rearms the uloop interval timer with the specified interval.

This method rearms the interval timer with the specified interval value,
allowing it to trigger repeatedly after the specified amount of time. If no
interval value or `null` is provided, the interval is disarmed and keeps
its callback, so that a later call can rearm it.

**Kind**: instance method of [`interval`](#module_uloop.interval)  
**Returns**: `boolean` - Returns `true` on success, `null` on error, such as a zero or negative
interval.  

| Param | Type | Description |
| --- | --- | --- |
| [interval] | `number` | Optional. The interval value in milliseconds specifying when the interval triggers again. Without a value, the interval is disarmed. |

**Example**  
```ucode
// Rearm the uloop interval with a interval of 1000 milliseconds
const success = interval.set(1000);

if (success)
    printf("Interval rearmed successfully\n");
else
    printf("Error occurred while rearming interval: ${uloop.error()}\n");

// Disable the uloop interval
const success = interval.set();

if (success)
    printf("Interval disabled successfully\n");
else
    printf("Error occurred while disabling interval: ${uloop.error()}\n");
```

#### interval.remaining() ⇒ `number`
Returns the milliseconds until the next expiration.

This method returns the remaining time until the uloop interval expires
and triggers again. If the interval is not armed (i.e., disabled),
it returns -1.

**Kind**: instance method of [`interval`](#module_uloop.interval)  
**Returns**: `number` - The milliseconds until the next expiration of the uloop interval, or -1 if
the interval is not armed.  
**Example**  
```ucode
// Get the milliseconds until the next expiration of the uloop interval
const remainingTime = interval.remaining();

if (remainingTime !== -1)
    printf("Milliseconds until next expiration: %d\n", remainingTime);
else
    printf("Interval is not armed\n");
```

#### interval.expirations() ⇒ `number`
Returns number of times the interval timer fired.

This method returns the number of times the uloop interval timer has expired
(fired) since it was instantiated.

**Kind**: instance method of [`interval`](#module_uloop.interval)  
**Returns**: `number` - The number of times the uloop interval timer has expired (fired).  
**Example**  
```ucode
// Get the number of times the uloop interval timer has expired
const expirations = interval.expirations();
printf("Number of expirations: %d\n", expirations);
```

#### interval.cancel() ⇒ `boolean`
Cancels the uloop interval.

This method cancels the uloop interval, disarming it and removing it from the
event loop. Associated resources are released.

**Kind**: instance method of [`interval`](#module_uloop.interval)  
**Returns**: `boolean` - Returns `true` on success.  
**Example**  
```ucode
// Cancel the uloop interval
interval.cancel();
```

### uloop.signal
**Kind**: static class of [`uloop`](#module_uloop)  
**See**: [signal()](#module_uloop+signal)  

* [.signal](#module_uloop.signal)
    * [.signo()](#module_uloop.signal+signo) ⇒ `number`
    * [.delete()](#module_uloop.signal+delete) ⇒ `boolean`

#### signal.signo() ⇒ `number`
Returns the associated signal number.

This method returns the signal number that this uloop signal handler is
configured to respond to.

**Kind**: instance method of [`signal`](#module_uloop.signal)  
**Returns**: `number` - The signal number that this handler is responding to.  
**Example**  
```ucode
// Get the signal number that the uloop signal handler is responding to
const sighandler = uloop.signal("SIGINT", () => printf("Cought INT\n"));
printf("Signal number: %d\n", sighandler.signo());
```

#### signal.delete() ⇒ `boolean`
Uninstalls the signal handler.

This method uninstalls the signal handler, restoring the previous or default
handler for the signal, and releasing any associated resources.

**Kind**: instance method of [`signal`](#module_uloop.signal)  
**Returns**: `boolean` - Returns `true` on success.  
**Example**  
```text
// Uninstall the signal handler and restore the previous/default handler
const sighandler = uloop.signal(…);
sighandler.delete();
```

### uloop~Event Mode Constants
The `ULOOP_*` constants are passed as bitwise OR-ed number to the
[handle()](#module_uloop.handle+handle) function to specify the IO
events that should be monitored on the given handle.

**Kind**: inner typedef of [`uloop`](#module_uloop)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| ULOOP_READ | `number` | File or socket is readable. |
| ULOOP_WRITE | `number` | File or socket is writable. |
| ULOOP_EDGE_TRIGGER | `number` | Enable edge-triggered event mode. |
| ULOOP_BLOCKING | `number` | Do not make descriptor non-blocking. |
| ULOOP_ERROR_CB | `number` | Deliver the error state to the callback instead of removing the descriptor from the event loop. |
| ULOOP_PRIORITY | `number` | Priority data is readable, e.g. TCP urgent data (epoll only, requires a libubox with `ULOOP_PRIORITY` support). |

---

# ucode module: zlib

> **Live docs:** https://ucode.mein.io/module-zlib.html

---

## Zlib bindings

The `zlib` module provides single-call and stream-oriented functions for interacting with zlib data.

### zlib.deflate(str_or_resource, [gzip], [level]) ⇒ `string`
Compresses data in Zlib or gzip format.

If the input argument is a plain string, it is directly compressed.

If an array, object or resource value is given, this function will attempt to
invoke a `read()` method on it to read chunks of input text to incrementally
compress. Reading will stop if the object's `read()` method returns
either `null` or an empty string.

Throws an exception on errors.

Returns the compressed data.

**Kind**: instance method of [`zlib`](#module_zlib)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| str_or_resource | `string` |  | The string or resource object to be compressed. |
| [gzip] | `boolean` | `false` | Add a gzip header if true (creates a gzip-compliant output, otherwise defaults to Zlib) |
| [level] | `number` | `Z_DEFAULT_COMPRESSION` | The compression level (0-9). |

**Example**  
```ucode
// deflate content using default compression
const deflated = deflate(content);

// deflate content using fastest compression
const deflated = deflate(content, Z_BEST_SPEED);
```

### zlib.inflate(str_or_resource) ⇒ `string`
Decompresses data in Zlib or gzip format.

If the input argument is a plain string, it is directly decompressed.

If an array, object or resource value is given, this function will attempt to
invoke a `read()` method on it to read chunks of input text to incrementally
decompress. Reading will stop if the object's `read()` method returns
either `null` or an empty string.

Throws an exception on errors.

Returns the decompressed data.

**Kind**: instance method of [`zlib`](#module_zlib)  

| Param | Type | Description |
| --- | --- | --- |
| str_or_resource | `string` | The string or resource object to be parsed as JSON. |

### zlib.deflater([gzip], [level]) ⇒ [`deflate`](#module_zlib.deflate)
Initializes a deflate stream.

Returns a stream handle on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`zlib`](#module_zlib)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [gzip] | `boolean` | `false` | Add a gzip header if true (creates a gzip-compliant output, otherwise defaults to Zlib) |
| [level] | `number` | `Z_DEFAULT_COMPRESSION` | The compression level (0-9). |

**Example**  
```ucode
// initialize a Zlib deflate stream using default compression
const zstrmd = deflater();

// initialize a gzip deflate stream using fastest compression
const zstrmd = deflater(true, Z_BEST_SPEED);
```

### zlib.inflater() ⇒ [`inflate`](#module_zlib.inflate)
Initializes an inflate stream. Can process either Zlib or gzip data.

Returns a stream handle on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`zlib`](#module_zlib)  
**Example**  
```ucode
// initialize an inflate stream
const zstrmi = inflater();
```

### zlib.deflate
**Kind**: static class of [`zlib`](#module_zlib)  
**See**: [module:zlib#deflater()](module:zlib#deflater())  

* [.deflate](#module_zlib.deflate)
    * [.write(src, [flush])](#module_zlib.deflate+write) ⇒ `boolean`
    * [.read()](#module_zlib.deflate+read) ⇒ `string`
    * [.error()](#module_zlib.deflate+error) ⇒ `string`

#### deflate.write(src, [flush]) ⇒ `boolean`
Writes a chunk of data to the deflate stream.

Input data must be a string, it is internally compressed by the zlib `deflate()` routine,
the end result is buffered according to the requested `flush` mode until read via
[module:zlib.zstrmd#read](module:zlib.zstrmd#read).
Valid `flush`values are `Z_NO_FLUSH` (the default),
`Z_SYNC_FLUSH, Z_PARTIAL_FLUSH, Z_FULL_FLUSH, Z_FINISH`.
If `flush` is `Z_FINISH` then no more data can be written to the stream.
Refer to the [Zlib manual](https://zlib.net/manual.html) for details
on each flush mode.

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`deflate`](#module_zlib.deflate)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| src | `string` |  | The string of data to deflate. |
| [flush] | `number` | `Z_NO_FLUSH` | The zlib flush mode. |

#### deflate.read() ⇒ `string`
Reads a chunk of compressed data from the deflate stream.

Returns the current content of the deflate buffer, fed through
[write](#module_zlib.deflate+write).

Returns compressed chunk on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`deflate`](#module_zlib.deflate)  

#### deflate.error() ⇒ `string`
Queries error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`deflate`](#module_zlib.deflate)  

### zlib.inflate
**Kind**: static class of [`zlib`](#module_zlib)  
**See**: [module:zlib#inflater()](module:zlib#inflater())  

* [.inflate](#module_zlib.inflate)
    * [.write(src, [flush])](#module_zlib.inflate+write) ⇒ `boolean`
    * [.read()](#module_zlib.inflate+read) ⇒ `string`
    * [.error()](#module_zlib.inflate+error) ⇒ `string`

#### inflate.write(src, [flush]) ⇒ `boolean`
Writes a chunk of data to the inflate stream.

Input data must be a string, it is internally decompressed by the zlib `inflate()` routine,
the end result is buffered according to the requested `flush` mode until read via
[read](#module_zlib.inflate+read).
Valid `flush` values are `Z_NO_FLUSH` (the default), `Z_SYNC_FLUSH, Z_FINISH`.
If `flush` is `Z_FINISH` then no more data can be written to the stream.
Refer to the [Zlib manual](https://zlib.net/manual.html) for details
on each flush mode.

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`inflate`](#module_zlib.inflate)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| src | `string` |  | The string of data to inflate. |
| [flush] | `number` | `Z_NO_FLUSH` | The zlib flush mode. |

#### inflate.read() ⇒ `string`
Reads a chunk of decompressed data from the inflate stream.

Returns the current content of the inflate buffer, fed through
[write](#module_zlib.inflate+write).

Returns decompressed chunk on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`inflate`](#module_zlib.inflate)  

#### inflate.error() ⇒ `string`
Queries error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`inflate`](#module_zlib.inflate)  

### zlib~Compression levels
Constants representing predefined compression levels.

**Kind**: inner typedef of [`zlib`](#module_zlib)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| Z_NO_COMPRESSION. | `number` |  |
| Z_BEST_SPEED. | `number` |  |
| Z_BEST_COMPRESSION. | `number` |  |
| Z_DEFAULT_COMPRESSION | `number` | default compromise between speed and compression (currently equivalent to level 6). |

### zlib~flush options
Constants representing flush options.

**Kind**: inner typedef of [`zlib`](#module_zlib)  
**Properties**

| Name | Type |
| --- | --- |
| Z_NO_FLUSH. | `number` | 
| Z_PARTIAL_FLUSH. | `number` | 
| Z_SYNC_FLUSH. | `number` | 
| Z_FULL_FLUSH. | `number` | 
| Z_FINISH. | `number` |
