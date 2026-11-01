---
module: ucode
total_token_count: 97566
section_count: 14
is_monolithic: false
is_sharded_part: true
part_number: 1
part_count: 2
generated: '2026-11-01T18:18:06.554594+00:00'
---

# ucode Bundled Reference (Part 1 of 2)

> **Contains:** 14 documents
> **Tokens:** ~97566 (cl100k_base)
> **Index:** [./bundled-reference.md](./bundled-reference.md)

---

# ucode module: debug

> **Live docs:** https://ucode.mein.io/module-debug.html

---

## Debugger Module

This module provides runtime debug functionality for ucode scripts.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { memdump, traceback } from 'debug';

  let stacktrace = traceback(1);

  memdump("/tmp/dump.txt");
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as debug from 'debug';

  let stacktrace = debug.traceback(1);

  debug.memdump("/tmp/dump.txt");
  ```

Additionally, the debug module namespace may also be imported by invoking the
`ucode` interpreter with the `-ldebug` switch.

Upon loading, the `debug` module will register a `SIGUSR2` signal handler
which, upon receipt of the signal, will write a memory dump of the currently
running program to `/tmp/ucode.$timestamp.$pid.memdump`. This default
behavior can be inhibited by setting the `UCODE_DEBUG_MEMDUMP_ENABLED`
environment variable to `0` when starting the process. The memory dump signal
and output directory can be overridden with the `UCODE_DEBUG_MEMDUMP_SIGNAL`
and `UCODE_DEBUG_MEMDUMP_PATH` environment variables respectively.

### debug.memdump(file) ⇒ `boolean`
Write a memory dump report to the given file.

This function generates a human readable memory dump of ucode values
currently managed by the running VM which is useful to track down logical
memory leaks in scripts.

The file parameter can be either a string value containing a file path, in
which case this function tries to create and write the report file at the
given location, a numeric file descriptor, or a resource implementing a
`fileno()` method which returns a numeric file descriptor.

Returns `true` if the report has been written.

Returns `null` if the file could not be opened or if the handle was invalid.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Description |
| --- | --- | --- |
| file | `string` \| `number` \| `module:fs.file` \| `module:fs.proc` \| `module:uloop.handle` \| `module:socket.socket` | The file path, file descriptor number, or open file handle to write report to. |

### debug.traceback([level]) ⇒ [`Array.<StackTraceEntry>`](#module_debug.StackTraceEntry)
Capture call stack trace.

This function captures the current call stack and returns it. The optional
level parameter controls how many calls up the trace should start. It
defaults to `1`, that is the function calling this `traceback()` function.

Returns an array of stack trace entries describing the function invocations
up to the point where `traceback()` is called.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [level] | `number` | `1` | The number of callframes up the call trace should start, `0` is this function itself, `1` the function calling it and so on. |

### debug.sourcepos() ⇒ [`SourcePosition`](#module_debug.SourcePosition)
Obtain information about the current source position.

The `sourcepos()` function determines the source code position of the
current instruction invoking this function.

Returns a dictionary containing the filename, line number and line byte
offset of the call site.

Returns `null` if this function was invoked from C code.

**Kind**: instance method of [`debug`](#module_debug)  

### debug.getinfo(value) ⇒ [`ValueInformation`](#module_debug.ValueInformation)
Obtain information about the given value.

The `getinfo()` function allows querying internal information about the
given ucode value, such as the current reference count, the mark bit state
etc.

Returns a dictionary with value type specific details.

Returns `null` if a `null` value was provided.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Description |
| --- | --- | --- |
| value | `\*` | The value to query information for. |

### debug.getlocal([level], variable) ⇒ [`LocalInfo`](#module_debug.LocalInfo)
Obtain local variable.

The `getlocal()` function retrieves information about the specified local
variable at the given call stack depth.

The call stack depth specifies the amount of levels up local variables should
be queried. A value of `0` refers to this `getlocal()` function call itself,
`1` to the function calling `getlocal()` and so on.

The variable to query might be either specified by name or by its index with
index numbers following the source code declaration order.

Returns a dictionary holding information about the given variable.

Returns `null` if the stack depth exceeds the size of the current call stack.

Returns `null` if the invocation at the given stack depth is a C call.

Returns `null` if the given variable name is not found or the given variable
index is invalid.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [level] | `number` | `1` | The amount of call stack levels up local variables should be queried. |
| variable | `string` \| `number` |  | The variable index or variable name to obtain information for. |

### debug.setlocal([level], variable, [value]) ⇒ [`LocalInfo`](#module_debug.LocalInfo)
Set local variable.

The `setlocal()` function manipulates the value of the specified local
variable at the given call stack depth.

The call stack depth specifies the amount of levels up local variables should
be updated. A value of `0` refers to this `setlocal()` function call itself,
`1` to the function calling `setlocal()` and so on.

The variable to update might be either specified by name or by its index with
index numbers following the source code declaration order.

Returns a dictionary holding information about the updated variable.

Returns `null` if the stack depth exceeds the size of the current call stack.

Returns `null` if the invocation at the given stack depth is a C call.

Returns `null` if the given variable name is not found or the given variable
index is invalid.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [level] | `number` | `1` | The amount of call stack levels up local variables should be updated. |
| variable | `string` \| `number` |  | The variable index or variable name to update. |
| [value] | `\*` | `` | The value to set the local variable to. |

### debug.getupval(target, variable) ⇒ [`UpvalInfo`](#module_debug.UpvalInfo)
Obtain captured variable (upvalue).

The `getupval()` function retrieves information about the specified captured
variable associated with the given function value or the invoked function at
the given call stack depth.

The call stack depth specifies the amount of levels up the function should be
selected to query associated captured variables for. A value of `0` refers to
this `getupval()` function call itself, `1` to the function calling
`getupval()` and so on.

The variable to query might be either specified by name or by its index with
index numbers following the source code declaration order.

Returns a dictionary holding information about the given variable.

Returns `null` if the given function value is not a closure.

Returns `null` if the stack depth exceeds the size of the current call stack.

Returns `null` if the invocation at the given stack depth is not a closure.

Returns `null` if the given variable name is not found or the given variable
index is invalid.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Description |
| --- | --- | --- |
| target | `function` \| `number` | Either a function value referring to a closure to query upvalues for or a stack depth number selecting a closure that many levels up. |
| variable | `string` \| `number` | The variable index or variable name to obtain information for. |

### debug.setupval(target, variable, value) ⇒ [`UpvalInfo`](#module_debug.UpvalInfo)
Set upvalue.

The `setupval()` function manipulates the value of the specified captured
variable associated with the given function value or the invoked function at
the given call stack depth.

The call stack depth specifies the amount of levels up the function should be
selected to update associated captured variables for. A value of `0` refers
to this `setupval()` function call itself, `1` to the function calling
`setupval()` and so on.

The variable to update might be either specified by name or by its index with
index numbers following the source code declaration order.

Returns a dictionary holding information about the updated variable.

Returns `null` if the given function value is not a closure.

Returns `null` if the stack depth exceeds the size of the current call stack.

Returns `null` if the invocation at the given stack depth is not a closure.

Returns `null` if the given variable name is not found or the given variable
index is invalid.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Description |
| --- | --- | --- |
| target | `function` \| `number` | Either a function value referring to a closure to update upvalues for or a stack depth number selecting a closure that many levels up. |
| variable | `string` \| `number` | The variable index or variable name to update. |
| value | `\*` | The value to set the variable to. |

### debug.breakpoint(spec, [mainfn]) ⇒ `number` \| `boolean`
Install a user breakpoint from a location specification, using the exact
same grammar as the interactive `break` CLI command (`path[:line[:offset]]`,
a bare function name, or a ucode expression evaluating to a function).

Unlike the `break` CLI command, this may be called before the program has
started running and thus without any active script call frame - e.g. by
the `-x <expr>`/`-X <expr>` command line options, which use this function
to resolve their argument early, before `uc_vm_execute()` is even called.
In that case, `mainfn` is used to resolve bare function names instead of
the (nonexistent) current frame; a `:line` spec without an explicit path,
or an arbitrary expression, cannot be resolved without a frame and are
reported as an error.

**Kind**: instance method of [`debug`](#module_debug)  
**Returns**: `number` \| `boolean` - The installed breakpoint id, or `false` on failure.  

| Param | Type | Description |
| --- | --- | --- |
| spec | `string` | The breakpoint location specification. |
| [mainfn] | `function` | The program entry function, used to resolve bare function names when there is no active call frame yet. |

### debug.notifyExit(status, exitCode, [exception])
Notify an attached remote debugger client, if any, that the target is
about to exit, with the final VM status (successful completion,
`exit()`/`quit`, or an uncaught error). A no-op when nobody is attached,
or for the local interactive debugger, where the exit is immediately
visible on the same terminal.

Called by [main.c](../wiki/chunked-reference/wiki_page-guide-developer-creating-a-meson-based-package.md) right after `uc_vm_execute()` returns, passing its raw
`uc_vm_status_t` return value plus the corresponding detail (exit code, or
an exception object), so a remote client learns the final outcome as an
explicit event instead of only noticing sometime later that the
connection dropped, with no indication of why.

The detail arguments must be passed in explicitly by the caller rather
than read off the vm here: by the time this C function body runs,
uc_vm_call() has already cleared vm->exception as its own first action
(a normal safety reset for ordinary calls), so [main.c](../wiki/chunked-reference/wiki_page-guide-developer-creating-a-meson-based-package.md) has to snapshot
vm->arg.s32 / call uc_vm_exception_object() into locals before making
this call.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Description |
| --- | --- | --- |
| status | `number` | The `uc_vm_status_t` value `uc_vm_execute()` returned. |
| exitCode | `number` | `vm->arg.s32` at the time `status` was returned, meaningful only for `STATUS_EXIT`. |
| [exception] | `object` | `uc_vm_exception_object(vm)` at the time `status` was returned - the same `{type, message, stacktrace}` shape script code sees via try/catch. Meaningful only for `ERROR_COMPILE`/`ERROR_RUNTIME`. |

### debug.debugger([target])
Initialize interactive debugger.

The `debugger()` function sets up the interactive command line debugger and
immediately starts it, or - when a function argument is provided - defers the
debugger invocation until the given function is called.

This function does not return any value.

**Kind**: instance method of [`debug`](#module_debug)  

| Param | Type | Description |
| --- | --- | --- |
| [target] | `function` | An optional function to attach the debugger to. When provided, a debug breakpoint is installed at the first instruction of the given function, causing the debug cli to get launched as soon as this function is entered. |

**Example**  
```ucode
// Launch debugger immediately
debug.debugger();

// Attach debugger to function
function test(a, b) {
  print(`Result is ${a * b}\n`);
}

debug.debugger(test); // Install debug breakpoint in `test()` function
test();               // Starts debugger, breaking before `print(…)`
```

### debug.StackTraceEntry : `Object`
**Kind**: static typedef of [`debug`](#module_debug)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| callee | `function` | The function that was called. |
| this | `\*` | The `this` context the function was called with. |
| mcall | `boolean` | Indicates whether the function was invoked as a method. |
| [strict] | `boolean` | Indicates whether the VM was running in strict mode when the function was called (only applicable to non-C, pure ucode calls). |
| [filename] | `string` | The name of the source file that called the function (only applicable to non-C, pure ucode calls). |
| [line] | `number` | The source line of the function call (only applicable to non-C, pure ucode calls). |
| [byte] | `number` | The source line offset of the function call (only applicable to non-C, pure ucode calls). |
| [context] | `string` | The surrounding source code context formatted as human-readable string, useful for generating debug messages (only applicable to non-C, pure ucode calls). |

### debug.SourcePosition : `Object`
**Kind**: static typedef of [`debug`](#module_debug)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| filename | `string` | The name of the source file that called this function. |
| line | `number` | The source line of the function call. |
| byte | `number` | The source line offset of the function call. |

### debug.UpvalRef : `Object`
**Kind**: static typedef of [`debug`](#module_debug)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| name | `string` | The name of the captured variable. |
| closed | `boolean` | Indicates whether the captured variable (upvalue) is closed or not. A closed upvalue means that the function value outlived the declaration scope of the captured variable. |
| value | `\*` | The current value of the captured variable. |
| [slot] | `number` | The stack slot of the captured variable. Only applicable to open (non-closed) captured variables. |

### debug.ValueInformation : `Object`
**Kind**: static typedef of [`debug`](#module_debug)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| type | `string` | The name of the value type, one of `integer`, `boolean`, `string`, `double`, `array`, `object`, `regexp`, `cfunction`, `closure`, `upvalue` or `resource`. |
| value | `\*` | The value itself. |
| tagged | `boolean` | Indicates whether the given value is internally stored as tagged pointer without an additional heap allocation. |
| [mark] | `boolean` | Indicates whether the value has it's mark bit set, which is used for loop detection during recursive object traversal on garbage collection cycles or complex value stringification. Only applicable to non-tagged values. |
| [refcount] | `number` | The current reference count of the value. Note that the `getinfo()` function places a reference to the value into the `value` field of the resulting information dictionary, so the ref count will always be at least 2 - one reference for the function call argument and one for the value property in the result dictionary. Only applicable to non-tagged values. |
| [unsigned] | `boolean` | Whether the number value is internally stored as unsigned integer. Only applicable to non-tagged integer values. |
| [address] | `number` | The address of the underlying C heap memory. Only applicable to non-tagged `string`, `array`, `object`, `cfunction` or `resource` values. |
| [length] | `number` | The length of the underlying string memory. Only applicable to non-tagged `string` values. |
| [count] | `number` | The amount of elements in the underlying memory structure. Only applicable to `array` and `object` values. |
| [constant] | `boolean` | Indicates whether the value is constant (immutable). Only applicable to `array` and `object` values. |
| [prototype] | `\*` | The associated prototype value, if any. Only applicable to `array`, `object` and `prototype` values. |
| [source] | `string` | The original regex source pattern. Only applicable to `regexp` values. |
| [icase] | `boolean` | Whether the compiled regex has the `i` (ignore case) flag set. Only applicable to `regexp` values. |
| [global] | `boolean` | Whether the compiled regex has the `g` (global) flag set. Only applicable to `regexp` values. |
| [newline] | `boolean` | Whether the compiled regex has the `s` (single line) flag set. Only applicable to `regexp` values. |
| [nsub] | `number` | The amount of capture groups within the regular expression. Only applicable to `regexp` values. |
| [name] | `string` | The name of the non-anonymous function. Only applicable to `cfunction` and `closure` values. Set to `null` for anonymous function values. |
| [arrow] | `boolean` | Indicates whether the ucode function value is an arrow function. Only applicable to `closure` values. |
| [module] | `boolean` | Indicates whether the ucode function value is a module entry point. Only applicable to `closure` values. |
| [strict] | `boolean` | Indicates whether the function body will be executed in strict mode. Only applicable to `closure` values. |
| [vararg] | `boolean` | Indicates whether the ucode function takes a variable number of arguments. Only applicable to `closure` values. |
| [nargs] | `number` | The number of arguments expected by the ucode function, excluding a potential final variable argument ellipsis. Only applicable to `closure` values. |
| [argnames] | `Array.<string>` | The names of the function arguments in their declaration order. Only applicable to `closure` values. |
| [nupvals] | `number` | The number of upvalues associated with the ucode function. Only applicable to `closure` values. |
| [upvals] | [`Array.<UpvalRef>`](#module_debug.UpvalRef) | An array of upvalue information objects. Only applicable to `closure` values. |
| [filename] | `string` | The path of the source file the function was declared in. Only applicable to `closure` values. |
| [line] | `number` | The source line number the function was declared at. Only applicable to `closure` values. |
| [byte] | `number` | The source line offset the function was declared at. Only applicable to `closure` values. |
| [type] | `string` | The resource type name. Only applicable to `resource` values. |

### debug.LocalInfo : `Object`
**Kind**: static typedef of [`debug`](#module_debug)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| index | `number` | The index of the local variable. |
| name | `string` | The name of the local variable. |
| value | `\*` | The current value of the local variable. |
| linefrom | `number` | The source line number of the local variable declaration. |
| bytefrom | `number` | The source line offset of the local variable declaration. |
| lineto | `number` | The source line number where the local variable goes out of scope. |
| byteto | `number` | The source line offset where the local variable goes out of scope. |

### debug.UpvalInfo : `Object`
**Kind**: static typedef of [`debug`](#module_debug)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| index | `number` | The index of the captured variable (upvalue). |
| name | `string` | The name of the captured variable. |
| closed | `boolean` | Indicates whether the captured variable is closed or not. A closed upvalue means that the function outlived the declaration scope of the captured variable. |
| value | `\*` | The current value of the captured variable. |

---

# ucode module: digest

> **Live docs:** https://ucode.mein.io/module-digest.html

---

## Digest Functions

The `digest` module bundles various digest functions.

### digest.md5(str) ⇒ `string`
Calculates the MD5 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
md5("This is a test");  // Returns "ce114e4501d2f4e2dcea3e17b546f339"
md5(123);               // Returns null
```

### digest.sha1(str) ⇒ `string`
Calculates the SHA1 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
sha1("This is a test");  // Returns "a54d88e06612d820bc3be72877c74f257b561b19"
sha1(123);               // Returns null
```

### digest.sha256(str) ⇒ `string`
Calculates the SHA256 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
sha256("This is a test");  // Returns "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e"
sha256(123);               // Returns null
```

### digest.fnv1a64(str) ⇒ `string`
Calculates the 64-bit FNV-1a non-cryptographic hash of string and returns
that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
fnv1a64("This is a test");  // Returns "25f0b040ca8b4ce0"
fnv1a64(123);               // Returns null
```

### digest.fnv1a64\_file(path) ⇒ `string`
Calculates the 64-bit FNV-1a non-cryptographic hash of a given file and
returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.md2(str) ⇒ `string`
Calculates the MD2 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
md2("This is a test");  // Returns "dc378580fd0722e56b82666a6994c718"
md2(123);               // Returns null
```

### digest.md4(str) ⇒ `string`
Calculates the MD4 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
md4("This is a test");  // Returns "3b487cf6856af7e330bc4b1b7d977ef8"
md4(123);               // Returns null
```

### digest.sha384(str) ⇒ `string`
Calculates the SHA384 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
sha384("This is a test");  // Returns "a27c7667e58200d4c0688ea136968404a0da366b1a9fc19bb38a0c7a609a1eef2bcc82837f4f4d92031a66051494b38c"
sha384(123);               // Returns null
```

### digest.sha512(str) ⇒ `string`
Calculates the SHA512 hash of string and returns that hash.

Returns `null` if a non-string argument is given.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| str | `string` | The string to hash. |

**Example**  
```ucode
sha512("This is a test");  // Returns "a028d4f74b602ba45eb0a93c9a4677240dcf281a1a9322f183bd32f0bed82ec72de9c3957b2f4c9a1ccf7ed14f85d73498df38017e703d47ebb9f0b3bf116f69"
sha512(123);               // Returns null
```

### digest.md5\_file(path) ⇒ `string`
Calculates the MD5 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.sha1\_file(path) ⇒ `string`
Calculates the SHA1 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.sha256\_file(path) ⇒ `string`
Calculates the SHA256 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.md2\_file(path) ⇒ `string`
Calculates the MD2 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.md4\_file(path) ⇒ `string`
Calculates the MD4 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.sha384\_file(path) ⇒ `string`
Calculates the SHA384 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

### digest.sha512\_file(path) ⇒ `string`
Calculates the SHA512 hash of a given file and returns that hash.

Returns `null` if an error occurred.

**Kind**: instance method of [`digest`](#module_digest)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |

---

# ucode module: fs

> **Live docs:** https://ucode.mein.io/module-fs.html

---

## Filesystem Access

The `fs` module provides functions for interacting with the file system.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { readlink, popen } from 'fs';

  let dest = readlink('/sys/class/net/eth0');
  let proc = popen('ps ww');
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as fs from 'fs';

  let dest = fs.readlink('/sys/class/net/eth0');
  let proc = fs.popen('ps ww');
  ```

Additionally, the filesystem module namespace may also be imported by invoking
the `ucode` interpreter with the `-lfs` switch.

### fs.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`fs`](#module_fs)  
**Example**  
```ucode
// Trigger file system error
unlink('/path/does/not/exist');

// Print error (should yield "No such file or directory")
print(error(), "\n");
```

### fs.popen(command, [mode]) ⇒ [`proc`](#module_fs.proc)
Starts a process and returns a handle representing the executed process.

The handle will be connected to the process stdin or stdout, depending on the
value of the mode argument.

The mode argument may be either "r" to open the process for reading (connect
to its stdout) or "w" to open the process for writing (connect to its stdin).

The mode character "r" or "w" may be optionally followed by "e" to apply the
FD_CLOEXEC flag onto the open descriptor.

Returns a process handle referring to the executed process.

Returns `null` if an error occurred.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| command | `string` \| `Array.<\*>` |  | The command to be executed, either as a plain shell command string or as an array of arguments. When an array is provided the process is started directly via execvp() without involving a shell, so argument values are never interpreted as shell syntax. Non-string array elements are converted to their string representation. A string command is passed to /bin/sh -c as usual. |
| [mode] | `string` | `"\"r\""` | The open mode of the process handle. |

**Example**  
```ucode
// Open a process with a command string (interpreted by the shell)
const process = popen('ls -la /tmp', 'r');
```
**Example**  
```ucode
// Open a process with an argument array (no shell involved)
const process = popen(['ls', '-la', '/tmp'], 'r');
```

### fs.open(path, [mode], [perm]) ⇒ [`file`](#module_fs.file)
Opens a file.

The mode argument specifies the way the file is opened, it may
start with one of the following values:

| Mode    | Description                                                                                                   |
|---------|---------------------------------------------------------------------------------------------------------------|
| "r"     | Opens a file for reading. The file must exist.                                                                 |
| "w"     | Opens a file for writing. If the file exists, it is truncated. If the file does not exist, it is created.     |
| "a"     | Opens a file for appending. Data is written at the end of the file. If the file does not exist, it is created. |
| "r+"    | Opens a file for both reading and writing. The file must exist.                                              |
| "w+"    | Opens a file for both reading and writing. If the file exists, it is truncated. If the file does not exist, it is created. |
| "a+"    | Opens a file for both reading and appending. Data can be read and written at the end of the file. If the file does not exist, it is created. |

Additionally, the following flag characters may be appended to
the mode value:

| Flag    | Description                                                                                                   |
|---------|---------------------------------------------------------------------------------------------------------------|
| "x"     | Opens a file for exclusive creation. If the file exists, the `open` call fails.                             |
| "e"     | Opens a file with the `O_CLOEXEC` flag set, ensuring that the file descriptor is closed on `exec` calls.      |

If the mode is one of `"w…"` or `"a…"`, the permission argument
controls the filesystem permissions bits used when creating
the file.

Returns a file handle object associated with the opened file.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| path | `string` |  | The path to the file. |
| [mode] | `string` | `"\"r\""` | The file opening mode. |
| [perm] | `number` | `0o666` | The file creation permissions (for modes `w…` and `a…`) |

**Example**  
```ucode
// Open a file in read-only mode
const fileHandle = open('file.txt', 'r');
```

### fs.fdopen(fd, [mode]) ⇒ `Object`
Associates a file descriptor number with a file handle object.

The mode argument controls how the file handle object is opened
and must match the open mode of the underlying descriptor.

It may be set to one of the following values:

| Mode    | Description                                                                                                  |
|---------|--------------------------------------------------------------------------------------------------------------|
| "r"     | Opens a file stream for reading. The file descriptor must be valid and opened in read mode.                  |
| "w"     | Opens a file stream for writing. The file descriptor must be valid and opened in write mode.                 |
| "a"     | Opens a file stream for appending. The file descriptor must be valid and opened in write mode.               |
| "r+"    | Opens a file stream for both reading and writing. The file descriptor must be valid and opened in read/write mode. |
| "w+"    | Opens a file stream for both reading and writing. The file descriptor must be valid and opened in read/write mode. |
| "a+"    | Opens a file stream for both reading and appending. The file descriptor must be valid and opened in read/write mode. |

Returns the file handle object associated with the file descriptor.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` |  | The file descriptor. |
| [mode] | `string` | `"\"r\""` | The open mode. |

**Example**  
```ucode
// Associate file descriptors of stdin and stdout with handles
const stdinHandle = fdopen(0, 'r');
const stdoutHandle = fdopen(1, 'w');
```

### fs.dup2(oldfd, newfd) ⇒ `boolean`
Duplicates a file descriptor.

This function duplicates the file descriptor `oldfd` to `newfd`. If `newfd`
was previously open, it is silently closed before being reused.

Returns `true` on success.
Returns `null` on error.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| oldfd | `number` | The file descriptor to duplicate. |
| newfd | `number` | The file descriptor number to duplicate to. |

**Example**  
```ucode
// Redirect stderr to a log file
const logfile = open('/tmp/error.log', 'w');
dup2(logfile.fileno(), 2);
logfile.close();
```

### fs.opendir(path) ⇒ [`dir`](#module_fs.dir)
Opens a directory and returns a directory handle associated with the open
directory descriptor.

Returns a director handle referring to the open directory.

Returns `null` if an error occurred.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the directory. |

**Example**  
```ucode
// Open a directory
const directory = opendir('path/to/directory');
```

### fs.readlink(path) ⇒ `string`
Reads the target path of a symbolic link.

Returns a string containing the target path.

Returns `null` if an error occurred.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the symbolic link. |

**Example**  
```ucode
// Read the value of a symbolic link
const targetPath = readlink('symbolicLink');
```

### fs.stat(path) ⇒ [`FileStatResult`](#module_fs.FileStatResult)
Retrieves information about a file or directory.

Returns an object containing information about the file or directory.

Returns `null` if an error occurred, e.g. due to insufficient permissions.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file or directory. |

**Example**  
```ucode
// Get information about a file
const fileInfo = stat('path/to/file');
```

### fs.lstat(path) ⇒ [`FileStatResult`](#module_fs.FileStatResult)
Retrieves information about a file or directory, without following symbolic
links.

Returns an object containing information about the file or directory.

Returns `null` if an error occurred, e.g. due to insufficient permissions.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file or directory. |

**Example**  
```ucode
// Get information about a directory
const dirInfo = lstat('path/to/directory');
```

### fs.statvfs(path) ⇒ [`StatVFSResult`](#module_fs.StatVFSResult)
Query filesystem statistics for a given pathname.

The returned object mirrors the members of `struct statvfs`.
Convenience properties `freesize` and `totalsize` are added,
which are calculated as:
- `frsize * bfree` to provide the free space in bytes and
- `frsize * blocks` to provide the total size of the filesystem.

On Linux an additional `type` field (magic number from `statfs`) is
provided if the call succeeds.

Returns `null` on failure (and sets `fs.last_error`).

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the directory or file with which to query the filesystem. |

**Example**  
```ucode
// Get filesystem statistics for a path
const stats = statvfs('path/to/directory');
print(stats.bsize); // file system block size
```

### fs.mkdir(path) ⇒ `boolean`
Creates a new directory.

Returns `true` if the directory was successfully created.

Returns `null` if an error occurred, e.g. due to non-existent path.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the new directory. |

**Example**  
```ucode
// Create a directory
mkdir('path/to/new-directory');
```

### fs.rmdir(path) ⇒ `boolean`
Removes the specified directory.

Returns `true` if the directory was successfully removed.

Returns `null` if an error occurred, e.g. due to non-existent path.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the directory to be removed. |

**Example**  
```ucode
// Remove a directory
rmdir('path/to/directory');
```

### fs.symlink(target, path) ⇒ `boolean`
Creates a new symbolic link.

Returns `true` if the symlink was successfully created.

Returns `null` if an error occurred, e.g. due to non-existent path.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| target | `string` | The target of the symbolic link. |
| path | `string` | The path of the symbolic link. |

**Example**  
```ucode
// Create a symbolic link
symlink('target', 'path/to/symlink');
```

### fs.unlink(path) ⇒ `boolean`
Removes the specified file or symbolic link.

Returns `true` if the unlink operation was successful.

Returns `null` if an error occurred, e.g. due to non-existent path.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file or symbolic link. |

**Example**  
```ucode
// Remove a file
unlink('path/to/file');
```

### fs.getcwd() ⇒ `string`
Retrieves the current working directory.

Returns a string containing the current working directory path.

Returns `null` if an error occurred.

**Kind**: instance method of [`fs`](#module_fs)  
**Example**  
```ucode
// Get the current working directory
const cwd = getcwd();
```

### fs.chdir(path) ⇒ `boolean`
Changes the current working directory to the specified path.

Returns `true` if the permission change was successful.

Returns `null` if an error occurred, e.g. due to insufficient permissions or
invalid arguments.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the new working directory. |

**Example**  
```ucode
// Change the current working directory
chdir('new-directory');
```

### fs.chmod(path, mode) ⇒ `boolean`
Changes the permission mode bits of a file or directory.

Returns `true` if the permission change was successful.

Returns `null` if an error occurred, e.g. due to insufficient permissions or
invalid arguments.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file or directory. |
| mode | `number` | The new mode (permissions). |

**Example**  
```ucode
// Change the mode of a file
chmod('path/to/file', 0o644);
```

### fs.chown(path, [uid], [gid]) ⇒ `boolean`
Changes the owner and group of a file or directory.

The user and group may be specified either as uid or gid number respectively,
or as a string containing the user or group name, in which case it is
resolved to the proper uid/gid first.

If either the user or group parameter is omitted or given as `-1`,
it is not changed.

Returns `true` if the ownership change was successful.

Returns `null` if an error occurred or if a user/group name cannot be
resolved to a uid/gid value.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| path | `string` |  | The path to the file or directory. |
| [uid] | `number` \| `string` | `-1` | The new owner's user ID. When given as number, it is used as-is, when given as string, the user name is resolved to the corresponding uid first. |
| [gid] | `number` \| `string` | `-1` | The new group's ID. When given as number, it is used as-is, when given as string, the group name is resolved to the corresponding gid first. |

**Example**  
```ucode
// Change the owner of a file
chown('path/to/file', 1000);

// Change the group of a directory
chown('/htdocs/', null, 'www-data');
```

### fs.rename(oldPath, newPath) ⇒ `boolean`
Renames or moves a file or directory.

Returns `true` if the rename operation was successful.

Returns `null` if an error occurred.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| oldPath | `string` | The current path of the file or directory. |
| newPath | `string` | The new path of the file or directory. |

**Example**  
```ucode
// Rename a file
rename('old-name.txt', 'new-name.txt');
```

### fs.glob(...pattern) ⇒ `Array.<string>`
Takes an arbitrary number of glob patterns and
resolves matching files for each one. In case of multiple patterns,
no efforts are made to remove duplicates or to globally sort the combined
match list. The list of matches for each individual pattern is sorted.
Returns an array containing all matched file paths.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type |
| --- | --- |
| ...pattern | `Arguments` | 

**Example**  
```ucode
import { chdir, glob } from 'fs';
chdir('/etc/ssl/certs/');
for (let cert in glob('*.crt', '*.pem')) {
	if (cert != null)
		print(cert, '\n');
}
// ACCVRAIZ1.crt
// AC_RAIZ_FNMT-RCM.crt
// AC_RAIZ_FNMT-RCM_SERVIDORES_SEGUROS.crt
// ...
```

### fs.dirname(path) ⇒ `string`
Retrieves the directory name of a path.

Returns the directory name component of the specified path.

Returns `null` if the path argument is not a string.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to extract the directory name from. |

**Example**  
```ucode
// Get the directory name of a path
const directoryName = dirname('/path/to/file.txt');
```

### fs.basename(path) ⇒ `string`
Retrieves the base name of a path.

Returns the base name component of the specified path.

Returns `null` if the path argument is not a string.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to extract the base name from. |

**Example**  
```ucode
// Get the base name of a path
const baseName = basename('/path/to/file.txt');
```

### fs.lsdir(path) ⇒ `Array.<string>`
Lists the content of a directory.

Returns a sorted array of the names of files and directories in the specified
directory.

Returns `null` if an error occurred, e.g. if the specified directory cannot
be opened.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the directory. |

**Example**  
```ucode
// List the content of a directory
const fileList = lsdir('/path/to/directory');
```

### fs.mkstemp([template]) ⇒ [`file`](#module_fs.file)
Creates a unique, ephemeral temporary file.

Creates a new temporary file, opens it in read and write mode, unlinks it and
returns a file handle object referring to the yet open but deleted file.

Upon closing the handle, the associated file will automatically vanish from
the system.

The optional path template argument may be used to override the path and name
chosen for the temporary file. If the path template contains no path element,
`/tmp/` is prepended, if it does not end with `XXXXXX`, then  * `.XXXXXX` is
appended to it. The `XXXXXX` sequence is replaced with a random value
ensuring uniqueness of the temporary file name.

Returns a file handle object referring to the ephemeral file on success.

Returns `null` if an error occurred, e.g. on insufficient permissions or
inaccessible directory.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [template] | `string` | `"\"/tmp/XXXXXX\""` | The path template to use when forming the temporary file name. |

**Example**  
```ucode
// Create a unique temporary file in the current working directory
const tempFile = mkstemp('./data-XXXXXX');
```

### fs.mkdtemp([template]) ⇒ `string`
Creates a unique temporary directory based on the given template.

If the template argument is given and contains a relative path, the created
directory will be placed relative to the current working directory.

If the template argument is given and contains an absolute path, the created
directory will be placed relative to the given directory.

If the template argument is given but does not contain a directory separator,
the directory will be placed in `/tmp/`.

If no template argument is given, the default `/tmp/XXXXXX` is used.

The template argument must end with six consecutive X characters (`XXXXXX`),
which will be replaced with a random string to create the unique directory name.
If the template does not end with `XXXXXX`, it will be automatically appended.

Returns a string containing the path of the created directory on success.

Returns `null` if an error occurred, e.g. on insufficient permissions or
inaccessible directory.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [template] | `string` | `"\"/tmp/XXXXXX\""` | The path template to use when forming the temporary directory name. |

**Example**  
```ucode
// Create a unique temporary directory in the current working directory
const tempDir = mkdtemp('./data-XXXXXX');
```

### fs.access(path, [mode]) ⇒ `boolean`
Checks the accessibility of a file or directory.

The optional modes argument specifies the access modes which should be
checked. A file is only considered accessible if all access modes specified
in the modes argument are possible.

The following modes are recognized:

| Mode | Description                           |
|------|---------------------------------------|
| "r"  | Tests whether the file is readable.   |
| "w"  | Tests whether the file is writable.   |
| "x"  | Tests whether the file is executable. |
| "f"  | Tests whether the file exists.        |

Returns `true` if the given path is accessible or `false` when it is not.

Returns `null` if an error occurred, e.g. due to inaccessible intermediate
path components, invalid path arguments etc.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| path | `string` |  | The path to the file or directory. |
| [mode] | `number` | `"f"` | Optional access mode. |

**Example**  
```ucode
// Check file read and write accessibility
const isAccessible = access('path/to/file', 'rw');

// Check execute permissions
const mayExecute = access('/usr/bin/example', 'x');
```

### fs.readfile(path, [limit]) ⇒ `string`
Reads the content of a file, optionally limited to the given amount of bytes.

Returns a string containing the file contents.

Returns `null` if an error occurred, e.g. due to insufficient permissions.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |
| [limit] | `number` | Number of bytes to limit the result to. When omitted, the entire content is returned. |

**Example**  
```ucode
// Read first 100 bytes of content
const content = readfile('path/to/file', 100);

// Read entire file content
const content = readfile('path/to/file');
```

### fs.writefile(path, data, [limit]) ⇒ `number`
Writes the given data to a file, optionally truncated to the given amount
of bytes.

In case the given data is not a string, it is converted to a string before
being written into the file. String values are written as-is, integer and
double values are written in decimal notation, boolean values are written as
`true` or `false` while arrays and objects are converted to their JSON
representation before being written into the file. The `null` value is
represented by an empty string so `writefile(…, null)` would write an empty
file. Resource values are written in the form `<type address>`, e.g.
`<fs.file 0x7f60f0981760>`.

If resource, array or object values contain a `tostring()` function in their
prototypes, then this function is invoked to obtain an alternative string
representation of the value.

If a file already exists at the given path, it is truncated. If no file
exists, it is created with default permissions 0o666 masked by the currently
effective umask.

Returns the number of bytes written.

Returns `null` if an error occurred, e.g. due to insufficient permissions.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file. |
| data | `\*` | The data to be written. |
| [limit] | `number` | Truncates the amount of data to be written to the specified amount of bytes. When omitted, the entire content is written. |

**Example**  
```ucode
// Write string to a file
const bytesWritten = writefile('path/to/file', 'Hello, World!');

// Write object as JSON to a file and limit to 1024 bytes at most
const obj = { foo: "Hello world", bar: true, baz: 123 };
const bytesWritten = writefile('debug.txt', obj, 1024);
```

### fs.realpath(path) ⇒ `string`
Resolves the absolute path of a file or directory.

Returns a string containing the resolved path.

Returns `null` if an error occurred, e.g. due to insufficient permissions.

**Kind**: instance method of [`fs`](#module_fs)  

| Param | Type | Description |
| --- | --- | --- |
| path | `string` | The path to the file or directory. |

**Example**  
```ucode
// Resolve the absolute path of a file
const absolutePath = realpath('path/to/file', 'utf8');
```

### fs.pipe() ⇒ [`Array.<file>`](#module_fs.file)
Creates a pipe and returns file handle objects associated with the read- and
write end of the pipe respectively.

Returns a two element array containing both a file handle object open in read
mode referring to the read end of the pipe and a file handle object open in
write mode referring to the write end of the pipe.

Returns `null` if an error occurred.

**Kind**: instance method of [`fs`](#module_fs)  
**Example**  
```ucode
// Create a pipe
const pipeHandles = pipe();
pipeHandles[1].write("Hello world\n");
print(pipeHandles[0].read("line"));
```

### fs.proc
**Kind**: static class of [`fs`](#module_fs)  
**See**: [popen()](#module_fs+popen)  

* [.proc](#module_fs.proc)
    * [.close()](#module_fs.proc+close) ⇒ `number`
    * [.read(length)](#module_fs.proc+read) ⇒ `string`
    * [.write(data)](#module_fs.proc+write) ⇒ `number`
    * [.flush()](#module_fs.proc+flush) ⇒ `boolean`
    * [.fileno()](#module_fs.proc+fileno) ⇒ `number`
    * [.error()](#module_fs.proc+error) ⇒ `string`

#### proc.close() ⇒ `number`
Closes the program handle and awaits program termination.

Upon calling `close()` on the handle, the program's input or output stream
(depending on the open mode) is closed. Afterwards, the function awaits the
termination of the underlying program and returns its exit code.

- When the program was terminated by a signal, the return value will be the
  negative signal number, e.g. `-9` for SIGKILL.

- When the program terminated normally, the return value will be the positive
  exit code of the program.

Returns a negative signal number if the program was terminated by a signal.

Returns a positive exit code if the program terminated normally.

Returns `null` if an error occurred.

**Kind**: instance method of [`proc`](#module_fs.proc)  

#### proc.read(length) ⇒ `string`
Reads a chunk of data from the program handle.

The length argument may be either a positive number of bytes to read, in
which case the read call returns up to that many bytes, or a string to
specify a dynamic read size.

 - If length is a number, the method will read the specified number of bytes
   from the handle. Reading stops after the given amount of bytes or after
   encountering EOF, whatever comes first.

 - If length is the string "line", the method will read an entire line,
   terminated by "\n" (a newline), from the handle. Reading stops at the next
   newline or when encountering EOF. The returned data will contain the
   terminating newline character if one was read.

 - If length is the string "all", the method will read from the handle until
   encountering EOF and return the complete contents.

 - If length is a single character string, the method will read from the
   handle until encountering the specified character or upon encountering
   EOF. The returned data will contain the terminating character if one was
   read.

Returns a string containing the read data.

Returns an empty string on EOF.

Returns `null` if a read error occurred.

**Kind**: instance method of [`proc`](#module_fs.proc)  

| Param | Type | Description |
| --- | --- | --- |
| length | `number` \| `string` | The length of data to read. Can be a number, the string "line", the string "all", or a single character string. |

**Example**  
```ucode
const fp = popen("command", "r");

// Example 1: Read 10 bytes from the handle
const chunk = fp.read(10);

// Example 2: Read the handle line by line
for (let line = fp.read("line"); length(line); line = fp.read("line"))
  print(line);

// Example 3: Read the complete contents from the handle
const content = fp.read("all");

// Example 4: Read until encountering the character ':'
const field = fp.read(":");
```

#### proc.write(data) ⇒ `number`
Writes a chunk of data to the program handle.

In case the given data is not a string, it is converted to a string before
being written to the program's stdin. String values are written as-is,
integer and double values are written in decimal notation, boolean values are
written as `true` or `false` while arrays and objects are converted to their
JSON representation before being written. The `null` value is represented by
an empty string so `proc.write(null)` would be a no-op. Resource values are
written in the form `<type address>`, e.g. `<fs.file 0x7f60f0981760>`.

If resource, array or object values contain a `tostring()` function in their
prototypes, then this function is invoked to obtain an alternative string
representation of the value.

Returns the number of bytes written.

Returns `null` if a write error occurred.

**Kind**: instance method of [`proc`](#module_fs.proc)  

| Param | Type | Description |
| --- | --- | --- |
| data | `\*` | The data to be written. |

**Example**  
```ucode
const fp = popen("command", "w");

fp.write("Hello world!\n");
```

#### proc.flush() ⇒ `boolean`
Forces a write of all buffered data to the underlying handle.

Returns `true` if the data was successfully flushed.

Returns `null` on error.

**Kind**: instance method of [`proc`](#module_fs.proc)  

#### proc.fileno() ⇒ `number`
Obtains the number of the handle's underlying file descriptor.

Returns the descriptor number.

Returns `null` on error.

**Kind**: instance method of [`proc`](#module_fs.proc)  

#### proc.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`proc`](#module_fs.proc)  
**Example**  
```ucode
// Trigger file system error
unlink('/path/does/not/exist');

// Print error (should yield "No such file or directory")
print(error(), "\n");
```

### fs.file
**Kind**: static class of [`fs`](#module_fs)  
**See**

- [open()](#module_fs+open)
- [fdopen()](#module_fs+fdopen)
- [mkstemp()](#module_fs+mkstemp)
- [pipe()](#module_fs+pipe)

* [.file](#module_fs.file)
    * [.close()](#module_fs.file+close) ⇒ `boolean`
    * [.read(length)](#module_fs.file+read) ⇒ `string`
    * [.write(data)](#module_fs.file+write) ⇒ `number`
    * [.seek([offset], [position])](#module_fs.file+seek) ⇒ `boolean`
    * [.truncate([offset])](#module_fs.file+truncate) ⇒ `boolean`
    * [.lock([op])](#module_fs.file+lock) ⇒ `boolean`
    * [.tell()](#module_fs.file+tell) ⇒ `number`
    * [.isatty()](#module_fs.file+isatty) ⇒ `boolean`
    * [.flush()](#module_fs.file+flush) ⇒ `boolean`
    * [.fileno()](#module_fs.file+fileno) ⇒ `number`
    * [.ioctl(direction, type, num, [value])](#module_fs.file+ioctl) ⇒ `number` \| `string`
    * [.error()](#module_fs.file+error) ⇒ `string`

#### file.close() ⇒ `boolean`
Closes the file handle.

Upon calling `close()` on the handle, buffered data is flushed and the
underlying file descriptor is closed.

Returns `true` if the handle was properly closed.

Returns `null` if an error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

#### file.read(length) ⇒ `string`
Reads a chunk of data from the file handle.

The length argument may be either a positive number of bytes to read, in
which case the read call returns up to that many bytes, or a string to
specify a dynamic read size.

 - If length is a number, the method will read the specified number of bytes
   from the handle. Reading stops after the given amount of bytes or after
   encountering EOF, whatever comes first.

 - If length is the string "line", the method will read an entire line,
   terminated by "\n" (a newline), from the handle. Reading stops at the next
   newline or when encountering EOF. The returned data will contain the
   terminating newline character if one was read.

 - If length is the string "all", the method will read from the handle until
   encountering EOF and return the complete contents.

 - If length is a single character string, the method will read from the
   handle until encountering the specified character or upon encountering
   EOF. The returned data will contain the terminating character if one was
   read.

Returns a string containing the read data.

Returns an empty string on EOF.

Returns `null` if a read error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

| Param | Type | Description |
| --- | --- | --- |
| length | `number` \| `string` | The length of data to read. Can be a number, the string "line", the string "all", or a single character string. |

**Example**  
```ucode
const fp = open("file.txt", "r");

// Example 1: Read 10 bytes from the handle
const chunk = fp.read(10);

// Example 2: Read the handle line by line
for (let line = fp.read("line"); length(line); line = fp.read("line"))
  print(line);

// Example 3: Read the complete contents from the handle
const content = fp.read("all");

// Example 4: Read until encountering the character ':'
const field = fp.read(":");
```

#### file.write(data) ⇒ `number`
Writes a chunk of data to the file handle.

In case the given data is not a string, it is converted to a string before
being written into the file. String values are written as-is, integer and
double values are written in decimal notation, boolean values are written as
`true` or `false` while arrays and objects are converted to their JSON
representation before being written. The `null` value is represented by an
empty string so `file.write(null)` would be a no-op. Resource values are
written in the form `<type address>`, e.g. `<fs.file 0x7f60f0981760>`.

If resource, array or object values contain a `tostring()` function in their
prototypes, then this function is invoked to obtain an alternative string
representation of the value.

Returns the number of bytes written.

Returns `null` if a write error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

| Param | Type | Description |
| --- | --- | --- |
| data | `\*` | The data to be written. |

**Example**  
```ucode
const fp = open("file.txt", "w");

fp.write("Hello world!\n");
```

#### file.seek([offset], [position]) ⇒ `boolean`
Set file read position.

Set the read position of the open file handle to the given offset and
position.

Returns `true` if the read position was set.

Returns `null` if an error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [offset] | `number` | `0` | The offset in bytes. |
| [position] | `number` | `0` | The position of the offset. | Position | Description                                                                                  | |----------|----------------------------------------------------------------------------------------------| | `0`      | The given offset is relative to the start of the file. This is the default value if omitted. | | `1`      | The given offset is relative to the current read position.                                   | | `2`      | The given offset is relative to the end of the file.                                         | |

**Example**  
```ucode
const fp = open("file.txt", "r");

print(fp.read(100), "\n");  // read 100 bytes...
fp.seek(0, 0);              // ... and reset position to start of file
print(fp.read(100), "\n");  // ... read same 100 bytes again

fp.seek(10, 1);  // skip 10 bytes forward, relative to current offset ...
fp.tell();       // ... position is at 110 now

fp.seek(-10, 2);            // set position to ten bytes before EOF ...
print(fp.read(100), "\n");  // ... reads 10 bytes at most
```

#### file.truncate([offset]) ⇒ `boolean`
Truncate file to a given size

Returns `true` if the file was successfully truncated.

Returns `null` if an error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [offset] | `number` | `0` | The offset in bytes. |

#### file.lock([op]) ⇒ `boolean`
Locks or unlocks a file.

The mode argument specifies lock/unlock operation flags.

| Flag    | Description                  |
|---------|------------------------------|
| "s"     | shared lock                  |
| "x"     | exclusive lock               |
| "n"     | don't block when locking     |
| "u"     | unlock                       |

Returns `true` if the file was successfully locked/unlocked.

Returns `null` if an error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

| Param | Type | Description |
| --- | --- | --- |
| [op] | `string` | The lock operation flags |

#### file.tell() ⇒ `number`
Obtain current read position.

Obtains the current, absolute read position of the open file.

Returns an integer containing the current read offset in bytes.

Returns `null` if an error occurred.

**Kind**: instance method of [`file`](#module_fs.file)  

#### file.isatty() ⇒ `boolean`
Check for TTY.

Checks whether the open file handle refers to a TTY (terminal) device.

Returns `true` if the handle refers to a terminal.

Returns `false` if the handle refers to another kind of file.

Returns `null` on error.

**Kind**: instance method of [`file`](#module_fs.file)  

#### file.flush() ⇒ `boolean`
Forces a write of all buffered data to the underlying handle.

Returns `true` if the data was successfully flushed.

Returns `null` on error.

**Kind**: instance method of [`file`](#module_fs.file)  

#### file.fileno() ⇒ `number`
Obtains the number of the handle's underlying file descriptor.

Returns the descriptor number.

Returns `null` on error.

**Kind**: instance method of [`file`](#module_fs.file)  

#### file.ioctl(direction, type, num, [value]) ⇒ `number` \| `string`
Performs an ioctl operation on the file.

The direction parameter specifies who is reading and writing,
from the user's point of view. It can be one of the following values:

| Direction      | Description                                                                       |
|----------------|-----------------------------------------------------------------------------------|
| IOC_DIR_NONE   | neither userspace nor kernel is writing, ioctl is executed without passing data.  |
| IOC_DIR_WRITE  | userspace is writing and kernel is reading.                                       |
| IOC_DIR_READ   | kernel is writing and userspace is reading.                                       |
| IOC_DIR_RW     | userspace is writing and kernel is writing back into the data structure.          |

Returns the result of the ioctl operation; for `IOC_DIR_READ` and
`IOC_DIR_RW` this is a string containing the data, otherwise a number as
return code.

In case of an error, null is returned and error details are available via
[error()](#module_fs+error).

**Kind**: instance method of [`file`](#module_fs.file)  

| Param | Type | Description |
| --- | --- | --- |
| direction | `number` | The direction of the ioctl operation. Use constants IOC_DIR_*. |
| type | `number` \| `null` | The ioctl type (see https://www.kernel.org/doc/html/latest/userspace-api/ioctl/ioctl-number.html) |
| num | `number` | The ioctl sequence number. |
| [value] | `number` \| `string` | The value to pass to the ioctl system call. For `IOC_DIR_NONE`, this argument is ignored. With `IOC_DIR_READ`, the value should be a positive integer specifying the number of bytes to expect from the kernel. For the other directions, `IOC_DIR_WRITE` and `IOC_DIR_RW`, that value parameter must be a string, serving as buffer for the data to send. |

#### file.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`file`](#module_fs.file)  
**Example**  
```ucode
// Trigger file system error
unlink('/path/does/not/exist');

// Print error (should yield "No such file or directory")
print(error(), "\n");
```

### fs.dir
**Kind**: static class of [`fs`](#module_fs)  
**See**: [opendir()](#module_fs+opendir)  

* [.dir](#module_fs.dir)
    * [.fileno()](#module_fs.dir+fileno) ⇒ `number`
    * [.read()](#module_fs.dir+read) ⇒ `string`
    * [.tell()](#module_fs.dir+tell) ⇒ `number`
    * [.seek(offset)](#module_fs.dir+seek) ⇒ `boolean`
    * [.close()](#module_fs.dir+close) ⇒ `boolean`
    * [.error()](#module_fs.dir+error) ⇒ `string`

#### dir.fileno() ⇒ `number`
Obtains the number of the handle's underlying file descriptor.

Returns the descriptor number.

Returns `null` on error.

**Kind**: instance method of [`dir`](#module_fs.dir)  

#### dir.read() ⇒ `string`
Read the next entry from the open directory.

Returns a string containing the entry name.

Returns `null` if there are no more entries to read.

Returns `null` if an error occurred.

**Kind**: instance method of [`dir`](#module_fs.dir)  

#### dir.tell() ⇒ `number`
Obtain current read position.

Returns the current read position in the open directory handle which can be
passed back to the `seek()` function to return to this position. This is
mainly useful to read an open directory handle (or specific items) multiple
times.

Returns an integer referring to the current position.

Returns `null` if an error occurred.

**Kind**: instance method of [`dir`](#module_fs.dir)  

#### dir.seek(offset) ⇒ `boolean`
Set read position.

Sets the read position within the open directory handle to the given offset
value. The offset value should be obtained by a previous call to `tell()` as
the specific integer values are implementation defined.

Returns `true` if the read position was set.

Returns `null` if an error occurred.

**Kind**: instance method of [`dir`](#module_fs.dir)  

| Param | Type | Description |
| --- | --- | --- |
| offset | `number` | Position value obtained by `tell()`. |

**Example**  
```ucode
const handle = opendir("/tmp");
const begin = handle.tell();

print(handle.read(), "\n");

handle.seek(begin);

print(handle.read(), "\n");  // prints the first entry again
```

#### dir.close() ⇒ `boolean`
Closes the directory handle.

Closes the underlying file descriptor referring to the opened directory.

Returns `true` if the handle was properly closed.

Returns `null` if an error occurred.

**Kind**: instance method of [`dir`](#module_fs.dir)  

#### dir.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`dir`](#module_fs.dir)  
**Example**  
```ucode
// Trigger file system error
unlink('/path/does/not/exist');

// Print error (should yield "No such file or directory")
print(error(), "\n");
```

### fs.FileStatResult : `Object`
**Kind**: static typedef of [`fs`](#module_fs)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| dev | `Object` | The device information. |
| dev.major | `number` | The major device number. |
| dev.minor | `number` | The minor device number. |
| perm | `Object` | The file permissions. |
| perm.setuid | `boolean` | Whether the setuid bit is set. |
| perm.setgid | `boolean` | Whether the setgid bit is set. |
| perm.sticky | `boolean` | Whether the sticky bit is set. |
| perm.user_read | `boolean` | Whether the file is readable by the owner. |
| perm.user_write | `boolean` | Whether the file is writable by the owner. |
| perm.user_exec | `boolean` | Whether the file is executable by the owner. |
| perm.group_read | `boolean` | Whether the file is readable by the group. |
| perm.group_write | `boolean` | Whether the file is writable by the group. |
| perm.group_exec | `boolean` | Whether the file is executable by the group. |
| perm.other_read | `boolean` | Whether the file is readable by others. |
| perm.other_write | `boolean` | Whether the file is writable by others. |
| perm.other_exec | `boolean` | Whether the file is executable by others. |
| inode | `number` | The inode number. |
| mode | `number` | The file mode. |
| nlink | `number` | The number of hard links. |
| uid | `number` | The user ID of the owner. |
| gid | `number` | The group ID of the owner. |
| size | `number` | The file size in bytes. |
| blksize | `number` | The block size for file system I/O. |
| blocks | `number` | The number of 512-byte blocks allocated for the file. |
| atime | `number` | The timestamp when the file was last accessed. |
| mtime | `number` | The timestamp when the file was last modified. |
| ctime | `number` | The timestamp when the file status was last changed. |
| type | `string` | The type of the file ("directory", "file", etc.). |

### fs.StatVFSResult : `Object`
**Kind**: static typedef of [`fs`](#module_fs)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| bsize | `number` | file system block size |
| frsize | `number` | fragment size |
| blocks | `number` | total blocks |
| bfree | `number` | free blocks |
| bavail | `number` | free blocks available to unprivileged users |
| files | `number` | total file nodes (inodes) |
| ffree | `number` | free file nodes |
| favail | `number` | free nodes available to unprivileged users |
| fsid | `number` | file system id |
| flag | [`ST\_FLAGS`](#module_fs.ST_FLAGS) | mount flags |
| namemax | `number` | maximum filename length |
| freesize | `number` | free space in bytes (calculated as `frsize * bfree`) |
| totalsize | `number` | total size of the filesystem (calculated as `frsize * blocks`) |
| type | `number` | (Linux only) magic number of the filesystem, obtained from `statfs` |

### fs.ST\_FLAGS
Bitmask flags used at volume mount time (¹ - Linux only).

**Kind**: static typedef of [`fs`](#module_fs)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| ST_MANDLOCK | `number` | Mandatory locking.¹ |
| ST_NOATIME | `number` | Do not update access times.¹ |
| ST_NODEV | `number` | Do not allow device files.¹ |
| ST_NODIRATIME | `number` | Do not update directory access times.¹ |
| ST_NOEXEC | `number` | Do not allow execution of binaries.¹ |
| ST_NOSUID | `number` | Do not allow set-user-identifier or set-group-identifier bits. |
| ST_RDONLY | `number` | Read-only filesystem. |
| ST_RELATIME | `number` | Update access times relative to modification time.¹ |
| ST_SYNCHRONOUS | `number` | Synchronous writes.¹ |
| ST_NOSYMFOLLOW | `number` | Do not follow symbolic links.¹ |

---

# ucode module: io

> **Live docs:** https://ucode.mein.io/module-io.html

---

## I/O Operations

The `io` module provides object-oriented access to UNIX file descriptors.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { open, O_RDWR } from 'io';

  let handle = open('/tmp/test.txt', O_RDWR);
  handle.write('Hello World\n');
  handle.close();
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as io from 'io';

  let handle = io.open('/tmp/test.txt', io.O_RDWR);
  handle.write('Hello World\n');
  handle.close();
  ```

Additionally, the io module namespace may also be imported by invoking
the `ucode` interpreter with the `-lio` switch.

### io.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`io`](#module_io)  
**Example**  
```ucode
// Trigger an error
io.open('/path/does/not/exist');

// Print error (should yield "No such file or directory")
print(io.error(), "\n");
```

### io.new(fd) ⇒ [`handle`](#module_io.handle)
Creates an io.handle from a file descriptor number.

Wraps the given file descriptor number in an io.handle object.

Returns an io.handle object.

Returns `null` if an error occurred.

**Kind**: instance method of [`io`](#module_io)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` | The file descriptor number. |

**Example**  
```ucode
// Wrap stdin
const stdin = io.new(0);
const data = stdin.read(100);
```

### io.open(path, [flags], [mode]) ⇒ [`handle`](#module_io.handle)
Opens a file and returns an io.handle.

Opens the specified file with the given flags and mode, returning an
io.handle wrapping the resulting file descriptor.

Returns an io.handle object.

Returns `null` if an error occurred.

**Kind**: instance method of [`io`](#module_io)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| path | `string` |  | The path to the file. |
| [flags] | `number` | `O_RDONLY` | The open flags (O_RDONLY, O_WRONLY, O_RDWR, etc.). |
| [mode] | `number` | `0o666` | The file creation mode (used with O_CREAT). |

**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDWR | O_CREAT, 0o644);
handle.write('Hello World\n');
handle.close();
```

### io.pipe() ⇒ [`Array.<handle>`](#module_io.handle)
Creates a pipe.

Creates a unidirectional data channel (pipe) that can be used for
inter-process communication. Returns an array containing two io.handle
objects: the first is the read end of the pipe, the second is the write end.

Data written to the write end can be read from the read end.

Returns an array `[read_handle, write_handle]` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`io`](#module_io)  
**Example**  
```ucode
const pair = io.pipe();
const reader = pair[0], writer = pair[1];

writer.write('Hello from pipe!');
writer.close();

const data = reader.read(100);
print(data, "\n");  // Prints: Hello from pipe!
```

### io.from(value) ⇒ [`handle`](#module_io.handle)
Creates an io.handle from various value types.

Creates an io.handle by extracting the file descriptor from the given value.
The value can be:
- An integer file descriptor number
- An [fs.file](../ucode/chunked-reference/c_source-api-module-fs.md), [fs.proc](../ucode/chunked-reference/c_source-api-module-fs.md), or socket resource
- Any object/array/resource with a fileno() method

Returns an io.handle object.

Returns `null` if an error occurred or the value cannot be converted.

**Kind**: instance method of [`io`](#module_io)  

| Param | Type | Description |
| --- | --- | --- |
| value | `\*` | The value to convert. |

**Example**  
```ucode
import { open as fsopen } from 'fs';
const fp = fsopen('/tmp/test.txt', 'r');
const handle = io.from(fp);
const data = handle.read(100);
```

### io.handle
**Kind**: static class of [`io`](#module_io)  
**See**

- [new()](#module_io+new)
- [open()](#module_io+open)
- [from()](#module_io+from)

* [.handle](#module_io.handle)
    * [.ptsname()](#module_io.handle+ptsname) ⇒ `string`
    * [.tcgetattr()](#module_io.handle+tcgetattr) ⇒ `object`
    * [.tcsetattr(attrs, [when])](#module_io.handle+tcsetattr) ⇒ `boolean`
    * [.grantpt()](#module_io.handle+grantpt) ⇒ `boolean`
    * [.unlockpt()](#module_io.handle+unlockpt) ⇒ `boolean`
    * [.read(length)](#module_io.handle+read) ⇒ `string`
    * [.write(data)](#module_io.handle+write) ⇒ `number`
    * [.seek([offset], [whence])](#module_io.handle+seek) ⇒ `boolean`
    * [.tell()](#module_io.handle+tell) ⇒ `number`
    * [.dup()](#module_io.handle+dup) ⇒ [`handle`](#module_io.handle)
    * [.dup2(newfd)](#module_io.handle+dup2) ⇒ `boolean`
    * [.fileno()](#module_io.handle+fileno) ⇒ `number`
    * [.fcntl(cmd, [arg])](#module_io.handle+fcntl) ⇒ `number` \| [`handle`](#module_io.handle)
    * [.ioctl(direction, type, num, [value])](#module_io.handle+ioctl) ⇒ `number` \| `string`
    * [.isatty()](#module_io.handle+isatty) ⇒ `boolean`
    * [.close()](#module_io.handle+close) ⇒ `boolean`
    * [.error()](#module_io.handle+error) ⇒ `string`

#### handle.ptsname() ⇒ `string`
Gets the name of the pseudo-terminal slave.

Returns the name of the pseudo-terminal slave device associated with
the master file descriptor.

Returns a string containing the slave device name.

Returns `null` if an error occurred or if the descriptor is not a
pseudo-terminal master.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const master = io.open('/dev/ptmx', O_RDWR);
const slave_name = master.ptsname();
print(slave_name, "\n");
```

#### handle.tcgetattr() ⇒ `object`
Gets terminal attributes.

Retrieves the terminal attributes for the file descriptor.

Returns an object containing terminal attributes (iflag, oflag, cflag, lflag,
ispeed, ospeed, and cc array).

Returns `null` if an error occurred or if the descriptor is not a terminal.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const handle = io.open('/dev/tty', O_RDWR);
const attrs = handle.tcgetattr();
if (attrs)
    print("Input flags: ", attrs.iflag, "\n");
```

#### handle.tcsetattr(attrs, [when]) ⇒ `boolean`
Sets terminal attributes.

Sets the terminal attributes for the file descriptor.

The attrs parameter should be an object with properties:
- iflag: input flags
- oflag: output flags
- cflag: control flags
- lflag: local flags
- ispeed: input speed
- ospeed: output speed
- cc: array of control characters (optional)

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| attrs | `object` |  | The terminal attributes to set. |
| [when] | `number` | `0` | When to apply the changes (TCSANOW, TCSADRAIN, TCSAFLUSH). |

**Example**  
```ucode
const handle = io.open('/dev/tty', O_RDWR);
const attrs = handle.tcgetattr();
attrs.lflag &= ~0x0000008; // Disable ECHO
handle.tcsetattr(attrs, TCSANOW);
```

#### handle.grantpt() ⇒ `boolean`
Grants access to a pseudo-terminal slave device.

Allows the owner of the pseudo-terminal master device to grant the
appropriate permissions on the corresponding slave device so that it
may be opened.

This function is typically called before opening the slave device.

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const master = io.open('/dev/ptmx', O_RDWR);
if (master.grantpt()) {
    print("Granted access to slave device\n");
}
```

#### handle.unlockpt() ⇒ `boolean`
Unlocks a pseudo-terminal slave device.

Unlocks the pseudo-terminal slave device associated with the master device
referred to by the file descriptor. This function is typically called after
grantpt() and before opening the slave device.

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const master = io.open('/dev/ptmx', O_RDWR);
master.grantpt();
if (master.unlockpt()) {
    print("Unlocked slave device\n");
}
```

#### handle.read(length) ⇒ `string`
Reads data from the file descriptor.

Reads up to the specified number of bytes from the file descriptor.

Returns a string containing the read data.

Returns an empty string on EOF.

Returns `null` if a read error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Description |
| --- | --- | --- |
| length | `number` | The maximum number of bytes to read. |

**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
const data = handle.read(1024);
```

#### handle.write(data) ⇒ `number`
Writes data to the file descriptor.

Writes the given data to the file descriptor. Non-string values are
converted to strings before being written.

Returns the number of bytes written.

Returns `null` if a write error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Description |
| --- | --- | --- |
| data | `\*` | The data to write. |

**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_WRONLY | O_CREAT);
handle.write('Hello World\n');
```

#### handle.seek([offset], [whence]) ⇒ `boolean`
Sets the file descriptor position.

Sets the file position of the descriptor to the given offset and whence.

Returns `true` if the position was successfully set.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [offset] | `number` | `0` | The offset in bytes. |
| [whence] | `number` | `0` | The position reference. | Whence | Description                                                        | |--------|--------------------------------------------------------------------| | `0`    | The offset is relative to the start of the file (SEEK_SET).       | | `1`    | The offset is relative to the current position (SEEK_CUR).        | | `2`    | The offset is relative to the end of the file (SEEK_END).         | |

**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
handle.seek(100, 0);  // Seek to byte 100 from start
```

#### handle.tell() ⇒ `number`
Gets the current file descriptor position.

Returns the current file position as an integer.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
const pos = handle.tell();
```

#### handle.dup() ⇒ [`handle`](#module_io.handle)
Duplicates the file descriptor.

Creates a duplicate of the file descriptor using dup(2).

Returns a new io.handle for the duplicated descriptor.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
const dup_handle = handle.dup();
```

#### handle.dup2(newfd) ⇒ `boolean`
Duplicates the file descriptor to a specific descriptor number.

Creates a duplicate of the file descriptor to the specified descriptor
number using dup2(2). If newfd was previously open, it is silently closed.

Returns `true` on success.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Description |
| --- | --- | --- |
| newfd | `number` | The target file descriptor number. |

**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_WRONLY);
handle.dup2(2);  // Redirect stderr to the file
```

#### handle.fileno() ⇒ `number`
Gets the file descriptor number.

Returns the underlying file descriptor number.

Returns `null` if the handle is closed.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
print(handle.fileno(), "\n");
```

#### handle.fcntl(cmd, [arg]) ⇒ `number` \| [`handle`](#module_io.handle)
Performs fcntl() operations on the file descriptor.

Performs the specified fcntl() command on the file descriptor with an
optional argument.

Returns the result of the fcntl() call. For F_DUPFD and F_DUPFD_CLOEXEC,
returns a new io.handle wrapping the duplicated descriptor. For other
commands, returns a number (interpretation depends on cmd).

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Description |
| --- | --- | --- |
| cmd | `number` | The fcntl command (e.g., F_GETFL, F_SETFL, F_GETFD, F_SETFD, F_DUPFD). |
| [arg] | `number` | Optional argument for the command. |

**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
const flags = handle.fcntl(F_GETFL);
handle.fcntl(F_SETFL, flags | O_NONBLOCK);
const dup_handle = handle.fcntl(F_DUPFD, 10);  // Returns io.handle
```

#### handle.ioctl(direction, type, num, [value]) ⇒ `number` \| `string`
Performs an ioctl operation on the file descriptor.

The direction parameter specifies who is reading and writing,
from the user's point of view. It can be one of the following values:

| Direction      | Description                                                                       |
|----------------|-----------------------------------------------------------------------------------|
| IOC_DIR_NONE   | neither userspace nor kernel is writing, ioctl is executed without passing data.  |
| IOC_DIR_WRITE  | userspace is writing and kernel is reading.                                       |
| IOC_DIR_READ   | kernel is writing and userspace is reading.                                       |
| IOC_DIR_RW     | userspace is writing and kernel is writing back into the data structure.          |

Returns the result of the ioctl operation; for `IOC_DIR_READ` and
`IOC_DIR_RW` this is a string containing the data, otherwise a number as
return code.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  

| Param | Type | Description |
| --- | --- | --- |
| direction | `number` | The direction of the ioctl operation. Use constants IOC_DIR_*. |
| type | `number` | The ioctl type (see https://www.kernel.org/doc/html/latest/userspace-api/ioctl/ioctl-number.html) |
| num | `number` \| `null` | The ioctl sequence number. |
| [value] | `number` \| `string` | The value to pass to the ioctl system call. For `IOC_DIR_NONE`, this argument is ignored. With `IOC_DIR_READ`, the value should be a positive integer specifying the number of bytes to expect from the kernel. For the other directions, `IOC_DIR_WRITE` and `IOC_DIR_RW`, that value parameter must be a string, serving as buffer for the data to send. |

**Example**  
```ucode
const handle = io.open('/dev/tty', O_RDWR);
const size = handle.ioctl(IOC_DIR_READ, 0x54, 0x13, 8);  // TIOCGWINSZ
```

#### handle.isatty() ⇒ `boolean`
Checks if the file descriptor refers to a terminal.

Returns `true` if the descriptor refers to a terminal device.

Returns `false` otherwise.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const handle = io.new(0);  // stdin
if (handle.isatty())
    print("Running in a terminal\n");
```

#### handle.close() ⇒ `boolean`
Closes the file descriptor.

Closes the underlying file descriptor. Further operations on this handle
will fail.

Returns `true` if the descriptor was successfully closed.

Returns `null` if an error occurred.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
const handle = io.open('/tmp/test.txt', O_RDONLY);
handle.close();
```

#### handle.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`handle`](#module_io.handle)  
**Example**  
```ucode
// Trigger an error
io.open('/path/does/not/exist');

// Print error (should yield "No such file or directory")
print(io.error(), "\n");
```

---

# ucode module: log

> **Live docs:** https://ucode.mein.io/module-log.html

---

## System logging functions

The `log` module provides bindings to the POSIX syslog functions `openlog()`,
`syslog()` and `closelog()` as well as - when available - the OpenWrt
specific ulog library functions.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { openlog, syslog, LOG_PID, LOG_USER, LOG_ERR } from 'log';

  openlog("my-log-ident", LOG_PID, LOG_USER);
  syslog(LOG_ERR, "An error occurred!");

  // OpenWrt specific ulog functions
  import { ulog_open, ulog, ULOG_SYSLOG, LOG_DAEMON, LOG_INFO } from 'log';

  ulog_open(ULOG_SYSLOG, LOG_DAEMON, "my-log-ident");
  ulog(LOG_INFO, "The current epoch is %d", time());
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as log from 'log';

  log.openlog("my-log-ident", log.LOG_PID, log.LOG_USER);
  log.syslog(log.LOG_ERR, "An error occurred!");

  // OpenWrt specific ulog functions
  log.ulog_open(log.ULOG_SYSLOG, log.LOG_DAEMON, "my-log-ident");
  log.ulog(log.LOG_INFO, "The current epoch is %d", time());
  ```

Additionally, the log module namespace may also be imported by invoking the
`ucode` interpreter with the `-llog` switch.

## Constants

The `log` module declares a number of numeric constants to specify logging
facility, priority and option values, as well as ulog specific channels.

### Syslog Options

| Constant Name | Description                                             |
|---------------|---------------------------------------------------------|
| `LOG_PID`     | Include PID with each message.                          |
| `LOG_CONS`    | Log to console if error occurs while sending to syslog. |
| `LOG_NDELAY`  | Open the connection to the logger immediately.          |
| `LOG_ODELAY`  | Delay open until the first message is logged.           |
| `LOG_NOWAIT`  | Do not wait for child processes created during logging. |

### Syslog Facilities

| Constant Name  | Description                                      |
|----------------|--------------------------------------------------|
| `LOG_AUTH`     | Authentication/authorization messages.           |
| `LOG_AUTHPRIV` | Private authentication messages.                 |
| `LOG_CRON`     | Clock daemon (cron and at commands).             |
| `LOG_DAEMON`   | System daemons without separate facility values. |
| `LOG_FTP`      | FTP server daemon.                               |
| `LOG_KERN`     | Kernel messages.                                 |
| `LOG_LPR`      | Line printer subsystem.                          |
| `LOG_MAIL`     | Mail system.                                     |
| `LOG_NEWS`     | Network news subsystem.                          |
| `LOG_SYSLOG`   | Messages generated internally by syslogd.        |
| `LOG_USER`     | Generic user-level messages.                     |
| `LOG_UUCP`     | UUCP subsystem.                                  |
| `LOG_LOCAL0`   | Local use 0 (custom facility).                   |
| `LOG_LOCAL1`   | Local use 1 (custom facility).                   |
| `LOG_LOCAL2`   | Local use 2 (custom facility).                   |
| `LOG_LOCAL3`   | Local use 3 (custom facility).                   |
| `LOG_LOCAL4`   | Local use 4 (custom facility).                   |
| `LOG_LOCAL5`   | Local use 5 (custom facility).                   |
| `LOG_LOCAL6`   | Local use 6 (custom facility).                   |
| `LOG_LOCAL7`   | Local use 7 (custom facility).                   |

### Syslog Priorities

| Constant Name | Description                         |
|---------------|-------------------------------------|
| `LOG_EMERG`   | System is unusable.                 |
| `LOG_ALERT`   | Action must be taken immediately.   |
| `LOG_CRIT`    | Critical conditions.                |
| `LOG_ERR`     | Error conditions.                   |
| `LOG_WARNING` | Warning conditions.                 |
| `LOG_NOTICE`  | Normal, but significant, condition. |
| `LOG_INFO`    | Informational message.              |
| `LOG_DEBUG`   | Debug-level message.                |

### Ulog channels

| Constant Name | Description                          |
|---------------|--------------------------------------|
| `ULOG_KMSG`   | Log messages to `/dev/kmsg` (dmesg). |
| `ULOG_STDIO`  | Log messages to stdout.              |
| `ULOG_SYSLOG` | Log messages to syslog.              |

### log.openlog([ident], [options], [facility]) ⇒ `boolean`
Open connection to system logger.

The `openlog()` function instructs the program to establish a connection to
the system log service and configures the default facility and identification
for use in subsequent log operations. It may be omitted, in which case the
first call to `syslog()` will implicitly call `openlog()` with a default
ident value representing the program name and a default `LOG_USER` facility.

The log option argument may be either a single string value containing an
option name, an array of option name strings or a numeric value representing
a bitmask of `LOG_*` option constants.

The facility argument may be either a single string value containing a
facility name or one of the numeric `LOG_*` facility constants in the module
namespace.

Returns `true` if the system `openlog()` function was invoked.

Returns `false` if an invalid argument, such as an unrecognized option or
facility name, was provided.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [ident] | `string` |  | A string identifying the program name. If omitted, the name of the calling process is used by default. |
| [options] | `number` \| [`LogOption`](#module_log.LogOption) \| [`Array.<LogOption>`](#module_log.LogOption) |  | Logging options to use. See [LogOption](#module_log.LogOption) for recognized option names. |
| [facility] | `number` \| [`LogFacility`](#module_log.LogFacility) | `"user"` | The facility to use for log messages generated by subsequent syslog calls. See [LogFacility](#module_log.LogFacility) for recognized facility names. |

**Example**  
```ucode
// Example usage of openlog function
openlog("myapp", LOG_PID | LOG_NDELAY, LOG_LOCAL0);

// Using option names instead of bitmask and LOG_USER facility
openlog("myapp", [ "pid", "ndelay" ], "user");
```

### log.syslog(priority, format, [...args]) ⇒ `boolean`
Log a message to the system logger.

This function logs a message to the system logger. The function behaves in a
sprintf-like manner, allowing the use of format strings and associated
arguments to construct log messages.

If the `openlog` function has not been called explicitly before, `syslog()`
implicitly calls `openlog()`, using a default ident and `LOG_USER` facility
value before logging the message.

If the `format` argument is not a string and not `null`, it will be
implicitly converted to a string and logged as-is, without further format
string processing.

Returns `true` if a message was passed to the system `syslog()` function.

Returns `false` if an invalid priority value or an empty message was given.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| priority | `number` \| [`LogPriority`](#module_log.LogPriority) | Log message priority. May be either a number value (potentially bitwise OR-ed with a log facility constant) which is passed as-is to the system `syslog()` function or a priority name string. See [LogPriority](#module_log.LogPriority) for recognized priority names. |
| format | `\*` | The sprintf-like format string for the log message, or any other, non-null, non-string value type which will be implicitly stringified and logged as-is. |
| [...args] | `\*` | In case a format string value was provided in the previous argument, then all subsequent arguments are used to replace the placeholders in the format string. |

**Example**  
```ucode
// Example usage of syslog function with format string and arguments
const username = "user123";
const errorCode = 404;
syslog(LOG_ERR, "User %s encountered error: %d", username, errorCode);

// If openlog has not been called explicitly, it is implicitly called with defaults:
syslog(LOG_INFO, "This message will be logged with default settings.");

// Selectively override used facility by OR-ing numeric constant
const password =" secret";
syslog(LOG_DEBUG|LOG_AUTHPRIV, "The password %s has been wrong", secret);

// Using priority names for logging
syslog("emerg", "System shutdown imminent!");

// Implicit stringification
syslog("debug", { foo: 1, bar: true, baz: [1, 2, 3] });
```

### log.closelog()
Close connection to system logger.

The usage of this function is optional, and usually an explicit log
connection tear down is not required.

**Kind**: instance method of [`log`](#module_log)  

### log.ulog\_open([channel], [facility], [ident]) ⇒ `boolean`
Configure ulog logger.

This functions configures the ulog mechanism and is analogous to using the
`openlog()` function in conjunction with `syslog()`.

The `ulog_open()` function is OpenWrt specific and may not be present on
other systems. Use `openlog()` and `syslog()` instead for portability to
non-OpenWrt environments.

A program may use multiple channels to simultaneously output messages using
different means. The channel argument may either be a single string value
containing a channel name, an array of channel names or a numeric value
representing a bitmask of `ULOG_*` channel constants.

The facility argument may be either a single string value containing a
facility name or one of the numeric `LOG_*` facility constants in the module
namespace.

The default facility value varies, depending on the execution context of the
program. In OpenWrt's preinit boot phase, or when stdout is not connected to
an interactive terminal, the facility defaults to `"daemon"` (`LOG_DAEMON`),
otherwise to `"user"` (`LOG_USER`).

Likewise, the default channel is selected depending on the context. During
OpenWrt's preinit boot phase, the `"kmsg"` channel is used, for interactive
terminals the `"stdio"` one and for all other cases the `"syslog"` channel
is selected.

Returns `true` if ulog was configured.

Returns `false` if an invalid argument, such as an unrecognized channel or
facility name, was provided.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| [channel] | `number` \| [`UlogChannel`](#module_log.UlogChannel) \| [`Array.<UlogChannel>`](#module_log.UlogChannel) | Specifies the log channels to use. See [UlogChannel](#module_log.UlogChannel) for recognized channel names. |
| [facility] | `number` \| [`LogFacility`](#module_log.LogFacility) | The facility to use for log messages generated by subsequent `ulog()` calls. See [LogFacility](#module_log.LogFacility) for recognized facility names. |
| [ident] | `string` | A string identifying the program name. If omitted, the name of the calling process is used by default. |

**Example**  
```ucode
// Log to dmesg and stderr
ulog_open(["stdio", "kmsg"], "daemon", "my-program");

// Use numeric constants and use implicit default ident
ulog_open(ULOG_SYSLOG, LOG_LOCAL0);
```

### log.ulog(priority, format, [...args]) ⇒ `boolean`
Log a message via the ulog mechanism.

The `ulog()` function outputs the given log message to all configured ulog
channels unless the given priority level exceeds the globally configured ulog
priority threshold. See [ulog_threshold()](#module_log+ulog_threshold)
for details.

The `ulog()` function is OpenWrt specific and may not be present on other
systems. Use `syslog()` instead for portability to non-OpenWrt environments.

Like `syslog()`, the function behaves in a sprintf-like manner, allowing the
use of format strings and associated arguments to construct log messages.

If the `ulog_open()` function has not been called explicitly before, `ulog()`
implicitly configures certain defaults, see
[ulog_open()](#module_log+ulog_open) for a detailed description.

If the `format` argument is not a string and not `null`, it will be
implicitly converted to a string and logged as-is, without further format
string processing.

Returns `true` if a message was passed to the underlying `ulog()` function.

Returns `false` if an invalid priority value or an empty message was given.

**Kind**: instance method of [`log`](#module_log)  
**See**

- module:log#ulog_open
- module:log#ulog_threshold
- module:log#syslog

| Param | Type | Description |
| --- | --- | --- |
| priority | `number` \| [`LogPriority`](#module_log.LogPriority) | Log message priority. May be either a number value or a priority name string. See [LogPriority](#module_log.LogPriority) for recognized priority names. |
| format | `\*` | The sprintf-like format string for the log message, or any other, non-null, non-string value type which will be implicitly stringified and logged as-is. |
| [...args] | `\*` | In case a format string value was provided in the previous argument, then all subsequent arguments are used to replace the placeholders in the format string. |

**Example**  
```ucode
// Example usage of ulog function with format string and arguments
const username = "user123";
const errorCode = 404;
ulog(LOG_ERR, "User %s encountered error: %d", username, errorCode);

// Using priority names for logging
ulog("err", "General error encountered");

// Implicit stringification
ulog("debug", { foo: 1, bar: true, baz: [1, 2, 3] });
```

### log.ulog\_close()
Close ulog logger.

Resets the ulog channels, the default facility and the log ident value to
defaults.

In case the `"syslog"` channel has been configured, the underlying
`closelog()` function will be invoked.

The usage of this function is optional, and usually an explicit ulog teardown
is not required.

The `ulog_close()` function is OpenWrt specific and may not be present on
other systems. Use `closelog()` in conjunction with `syslog()` instead for
portability to non-OpenWrt environments.

**Kind**: instance method of [`log`](#module_log)  
**See**: module:log#closelog  

### log.ulog\_threshold([priority]) ⇒ `boolean`
Set ulog priority threshold.

This function configures the application wide log message threshold for log
messages emitted with `ulog()`. Any message with a priority higher (= less
severe) than the threshold priority will be discarded. This is useful to
implement application wide verbosity settings without having to wrap `ulog()`
invocations into a helper function or guarding code.

When no explicit threshold has been set, `LOG_DEBUG` is used by default,
allowing log messages with all known priorities.

The `ulog_threshold()` function is OpenWrt specific and may not be present on
other systems. There is no syslog equivalent to this ulog specific threshold
mechanism.

The priority argument may be either a string value containing a priority name
or one of the numeric `LOG_*` priority constants in the module namespace.

Returns `true` if a threshold was set.

Returns `false` if an invalid priority value was given.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| [priority] | `number` \| [`LogPriority`](#module_log.LogPriority) | The priority threshold to configure. See [LogPriority](#module_log.LogPriority) for recognized priority names. |

**Example**  
```ucode
// Set threshold to "warning" or more severe
ulog_threshold(LOG_WARNING);

// This message will be suppressed
ulog(LOG_DEBUG, "Testing thresholds");

// Using priority name
ulog_threshold("debug");
```

### log.INFO(format, [...args]) ⇒ `boolean`
Invoke ulog with LOG_INFO.

This function is convenience wrapper for `ulog(LOG_INFO, ...)`.

See [ulog()](#module_log+ulog) for details.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| format | `\*` | The sprintf-like format string for the log message, or any other, non-null, non-string value type which will be implicitly stringified and logged as-is. |
| [...args] | `\*` | In case a format string value was provided in the previous argument, then all subsequent arguments are used to replace the placeholders in the format string. |

**Example**  
```ucode
INFO("This is an info log message");
```

### log.NOTE(format, [...args]) ⇒ `boolean`
Invoke ulog with LOG_NOTICE.

This function is convenience wrapper for `ulog(LOG_NOTICE, ...)`.

See [ulog()](#module_log+ulog) for details.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| format | `\*` | The sprintf-like format string for the log message, or any other, non-null, non-string value type which will be implicitly stringified and logged as-is. |
| [...args] | `\*` | In case a format string value was provided in the previous argument, then all subsequent arguments are used to replace the placeholders in the format string. |

**Example**  
```ucode
NOTE("This is a notification log message");
```

### log.WARN(format, [...args]) ⇒ `boolean`
Invoke ulog with LOG_WARNING.

This function is convenience wrapper for `ulog(LOG_WARNING, ...)`.

See [ulog()](#module_log+ulog) for details.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| format | `\*` | The sprintf-like format string for the log message, or any other, non-null, non-string value type which will be implicitly stringified and logged as-is. |
| [...args] | `\*` | In case a format string value was provided in the previous argument, then all subsequent arguments are used to replace the placeholders in the format string. |

**Example**  
```ucode
WARN("This is a warning");
```

### log.ERR(format, [...args]) ⇒ `boolean`
Invoke ulog with LOG_ERR.

This function is convenience wrapper for `ulog(LOG_ERR, ...)`.

See [ulog()](#module_log+ulog) for details.

**Kind**: instance method of [`log`](#module_log)  

| Param | Type | Description |
| --- | --- | --- |
| format | `\*` | The sprintf-like format string for the log message, or any other, non-null, non-string value type which will be implicitly stringified and logged as-is. |
| [...args] | `\*` | In case a format string value was provided in the previous argument, then all subsequent arguments are used to replace the placeholders in the format string. |

**Example**  
```ucode
ERR("This is an error!");
```

### log.LogOption : `enum`
The following log option strings are recognized:

| Log Option | Description                                                |
|------------|------------------------------------------------------------|
| `"pid"`    | Include PID with each message.                             |
| `"cons"`   | Log to console if an error occurs while sending to syslog. |
| `"ndelay"` | Open the connection to the logger immediately.             |
| `"odelay"` | Delay open until the first message is logged.              |
| `"nowait"` | Do not wait for child processes created during logging.    |

**Kind**: static enum of [`log`](#module_log)  

### log.LogFacility : `enum`
The following log facility strings are recognized:

| Facility     | Description                                      |
|--------------|--------------------------------------------------|
| `"auth"`     | Authentication/authorization messages.           |
| `"authpriv"` | Private authentication messages.                 |
| `"cron"`     | Clock daemon (cron and at commands).             |
| `"daemon"`   | System daemons without separate facility values. |
| `"ftp"`      | FTP server daemon.                               |
| `"kern"`     | Kernel messages.                                 |
| `"lpr"`      | Line printer subsystem.                          |
| `"mail"`     | Mail system.                                     |
| `"news"`     | Network news subsystem.                          |
| `"syslog"`   | Messages generated internally by syslogd.        |
| `"user"`     | Generic user-level messages.                     |
| `"uucp"`     | UUCP subsystem.                                  |
| `"local0"`   | Local use 0 (custom facility).                   |
| `"local1"`   | Local use 1 (custom facility).                   |
| `"local2"`   | Local use 2 (custom facility).                   |
| `"local3"`   | Local use 3 (custom facility).                   |
| `"local4"`   | Local use 4 (custom facility).                   |
| `"local5"`   | Local use 5 (custom facility).                   |
| `"local6"`   | Local use 6 (custom facility).                   |
| `"local7"`   | Local use 7 (custom facility).                   |

**Kind**: static enum of [`log`](#module_log)  

### log.LogPriority : `enum`
The following log priority strings are recognized:

| Priority    | Description                         |
|-------------|-------------------------------------|
| `"emerg"`   | System is unusable.                 |
| `"alert"`   | Action must be taken immediately.   |
| `"crit"`    | Critical conditions.                |
| `"err"`     | Error conditions.                   |
| `"warning"` | Warning conditions.                 |
| `"notice"`  | Normal, but significant, condition. |
| `"info"`    | Informational message.              |
| `"debug"`   | Debug-level message.                |

**Kind**: static enum of [`log`](#module_log)  

### log.UlogChannel : `enum`
The following ulog channel strings are recognized:

| Channel    | Description                                       |
|------------|---------------------------------------------------|
| `"kmsg"`   | Log to `/dev/kmsg`, log messages appear in dmesg. |
| `"syslog"` | Use standard `syslog()` mechanism.                |
| `"stdio"`  | Use stderr for log output.                        |

**Kind**: static enum of [`log`](#module_log)

---

# ucode module: math

> **Live docs:** https://ucode.mein.io/module-math.html

---

## Mathematical Functions

The `math` module bundles various mathematical and trigonometrical functions.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { pow, rand } from 'math';

  let x = pow(2, 5);
  let y = rand();
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as math from 'math';

  let x = math.pow(2, 5);
  let y = math.rand();
  ```

Additionally, the math module namespace may also be imported by invoking the
`ucode` interpreter with the `-lmath` switch.

It should be noted that when the ucode interpreter is run as `-p "..."`,
values involving Infinity are returned as the max double precision value
+/-1e309 (JSON), whereas when run as `-e "print(...)"` Infinity is
represented by the string `Infinity`. The boolean check `isinf()` is
available to determine Infinity values.

### math.abs(number) ⇒ `number`
Returns the absolute value of the given numeric value.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - Returns the absolute value or `NaN` if the given argument could
not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| number | `\*` | The number to return the absolute value for. |

### math.acos(x) ⇒ `double`
Calculates the arc cosine of `x`.

On success, this function returns the principal value of the arc
cosine of `x` in radians; the return value is in the range [pi, 0].

 - If `x` is -1, pi is returned.
 - If `x` is  0, pi/2 is returned.
 - If `x` is +1, 0 is returned.

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

**Example**  
```ucode
acos(-1); // 3.1415926535898 i.e. pi
acos(0);  // 1.5707963267949 i.e. pi/2
acos(1);  // 0.0 i.e. 0 pi
```

### math.asin(x) ⇒ `double`
Calculates the arc sine of `x`.

On success, this function returns the principal value of the arc
sine of `x` in radians; the return value is in the range [-pi/2, pi/2].

 - If `x` is +0 (-0), 0 is returned.
 - If `x` is +1 (-1), pi/2 (-pi/2) is returned.

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

**Example**  
```ucode
asin(-1); // -1.5707963267949 i.e. -pi/2
asin(0);  // 0.0 i.e. 0 pi
asin(1);  // 1.5707963267949 i.e. pi/2
```

### math.atan(x) ⇒ `double`
Calculates the arc tangent of `x`.

On success, this function returns the principal value of the arc
tangent of `x` in radians; the return value is in the range [-pi/2, pi/2].

 - If `x` is +0 (-0), 0 is returned.
 - As `x` tends toward +Infinity (-Infinity), the return value asymptotically
converges toward pi/2 (-pi/2).

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

**Example**  
```ucode
atan(-100000); // -1.5707863267949 i.e. ~ -pi/2
atan(0);       // 0.0 i.e. 0 pi
atan(100000);  // 1.5707863267949 i.e. ~ pi/2
```

### math.cosh(x) ⇒ `double`
Calculates the hyperbolic cosine of `x`.

On success, this function returns the principal value of the hyperbolic
cosine of `x`; the return value is in the range [Infinity, 1].

The relationship is: cosh = `((e^x) + (e^-x)) / 2`.

 - As `x` decreases below -1, the return value exponentiates toward Infinity.
 - If `x` is  0, 1 is returned.
 - As `x` increases above +1, the return value exponentiates toward Infinity.

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

**Example**  
```ucode
cosh(-10); // 11013.232920103
cosh(-1);  // 1.5430806348152
cosh(0);   // 1.0
cosh(1);   // 1.5430806348152
cosh(10);  // 11013.232920103
```

### math.sinh(x) ⇒ `double`
Calculates the hyperbolic sine of `x`.

On success, this function returns the principal value of the hyperbolic
sine of `x`; the return value is in the range [-Infinity, Infinity].
 
The relationship is: sinh = `((e^x) - (e^-x)) / 2`.

 - As `x` decreases below -1, the return value exponentiates toward -Infinity.
 - If `x` is  0, 0 is returned.
 - As `x` increases above +1, the return value exponentiates toward Infinity.

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

**Example**  
```ucode
sinh(-10); // -11013.232920103
sinh(-1);  // -1.1752011936438
sinh(0);   // 0.0
sinh(1);   // 1.1752011936438
sinh(10);  // 11013.232920103
```

### math.tanh(x) ⇒ `double`
Calculates the hyperbolic tangent of `x`.

On success, this function returns the principal value of the hyperbolic
tangent of `x`; the return value is in the range [-1, 1].

The relationship is: tanh = `((e^x) - (e^-x)) / ((e^x) + (e^-x))`, or
tanh = `sinh(x) / cosh(x)`.

 - As `x` decreases below -1, the return value asymptotically expands
toward -1.
 - If `x` is  0, 0 is returned.
 - As `x` increases above +1, the return value asymptotically expands
toward 1.

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

**Example**  
```ucode
atan(-100); // -1.0
atan(-10);  // -0.99999999587769
atan(0);    // 0.0
atan(10);   // 0.99999999587769
atan(100);  // 1.0
```

### math.atan2(y, x) ⇒ `number`
Calculates the principal value of the arc tangent of `y`/`x`,
using the signs of the two arguments to determine the quadrant
of the result.

On success, this function returns the principal value of the arc
tangent of `y`/`x` in radians; the return value is in the range [-pi, pi].

 - If `y` is +0 (-0) and `x` is less than 0, +pi (-pi) is returned.
 - If `y` is +0 (-0) and `x` is greater than 0, +0 (-0) is returned.
 - If `y` is less than 0 and `x` is +0 or -0, -pi/2 is returned.
 - If `y` is greater than 0 and `x` is +0 or -0, pi/2 is returned.
 - If either `x` or `y` is NaN, a NaN is returned.
 - If `y` is +0 (-0) and `x` is -0, +pi (-pi) is returned.
 - If `y` is +0 (-0) and `x` is +0, +0 (-0) is returned.
 - If `y` is a finite value greater (less) than 0, and `x` is negative
   infinity, +pi (-pi) is returned.
 - If `y` is a finite value greater (less) than 0, and `x` is positive
   infinity, +0 (-0) is returned.
 - If `y` is positive infinity (negative infinity), and `x` is finite,
   pi/2 (-pi/2) is returned.
 - If `y` is positive infinity (negative infinity) and `x` is negative
   infinity, +3 * pi/4 (-3 * pi/4) is returned.
 - If `y` is positive infinity (negative infinity) and `x` is positive
   infinity, +pi/4 (-pi/4) is returned.

When either `x` or `y` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| y | `\*` | The `y` value. |
| x | `\*` | The `x` value. |

### math.tan(x) ⇒ `double`
Calculates the tangent of `x`, the floating-point value representing the
angle in radians.

On success, this function returns the tangent of `x`.

The relationship is `tan(x) = sin(x) / cos (x)`. A graph of the tangent has
periodic patterns directly related to ratios of pi, where radian values of
whole multiples of (1, 2, 3, ...) pi are 0, and radian values of half
multiples of pi (1/2, 3/2, 5/2, ...) are +/-Infinity.

When `x` can't be converted to a numeric value, `NaN` is
returned.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | The `x` value. |

### math.cos(x) ⇒ `number`
Calculates the cosine of `x`, where `x` is given in radians.

Returns the resulting cosine value.

Returns `NaN` if the `x` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | Radians value to calculate cosine for. |

### math.exp(x) ⇒ `number`
Calculates the value of `e` (the base of natural logarithms)
raised to the power of `x`.

On success, returns the exponential value of `x`.

 - If `x` is positive infinity, positive infinity is returned.
 - If `x` is negative infinity, `+0` is returned.
 - If the result underflows, a range error occurs, and zero is returned.
 - If the result overflows, a range error occurs, and `Infinity` is returned.

Returns `NaN` if the `x` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | Power to raise `e` to. |

### math.log(x) ⇒ `number`
Calculates the natural logarithm of `x`.

On success, returns the natural logarithm of `x`.

 - If `x` is `1`, the result is `+0`.
 - If `x` is positive infinity, positive infinity is returned.
 - If `x` is zero, then a pole error occurs, and the function
   returns negative infinity.
 - If `x` is negative (including negative infinity), then a domain
   error occurs, and `NaN` is returned.

Returns `NaN` if the `x` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | Value to calculate natural logarithm of. |

### math.log10(x) ⇒ `double`
Calculate base-10 log of x.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - The common (base-10) logarithm of x, or
`NaN` if the given argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
log10(100);   // 2.0
log10(10);    // 1.0
log10(5);     // 0.69897000433602
log10(1);     // 0.0
log10(0);     // -1e309
```

### math.log2(x) ⇒ `double`
Calculate base-2 log of x.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - The common (base-2) logarithm of x, or
`NaN` if the given argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
log2(1024);  // 10.0
log2(512);   // 9.0
log2(16);    // 4.0
log2(4);     // 2.0
log2(2);     // 1.0
log2(1);     // 0.0
log2(0);     // -1e309
```

### math.log1p(x) ⇒ `double`
Computes the natural (base e) logarithm of 1 + x. This function is more
precise than the expression [`log`](#module_math+log)(1 + x) if x is
close to zero.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - The natural (base e) logarithm of 1 + x, or
`NaN` if the given argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
log1p(10);    // 2.3978952727984
log1p(1);     // 0.69314718055995
log1p(0.1);   // 0.095310179804325
log1p(0.001); // 0.00099950033308353
log1p(0);     // 0.0
```

### math.expm1(x) ⇒ `double`
Computes the e (Euler's number, 2.7182818) raised to the given power x,
minus 1.0. This function is more accurate than the expression 
[`exp(x)`](#module_math+exp)-1.0
if x is close to zero.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - The e (Euler's number, 2.7182818) raised to the given power x, minus 1.0, or
`NaN` if the given argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
expm1(10);       // 22025.465794807
expm1(1);        // 1.718281828459
expm1(0.1);      // 0.10517091807565
expm1(0.001);    // 0.0010005001667083
exp(0.001)-1;    // 0.0010005001667084
expm1(0.0001);   // 0.00010000500016667
exp(0.0001)-1;   // 0.00010000500016671
expm1(0.000001); // 1.0000005000002e-06
exp(0.000001)-1; // 1.0000004999622e-06
expm1(0);        // 0.0
```

### math.sin(x) ⇒ `number`
Calculates the sine of `x`, where `x` is given in radians.

Returns the resulting sine value.

 - When `x` is positive or negative infinity, a domain error occurs
   and `NaN` is returned.

Returns `NaN` if the `x` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | Radians value to calculate sine for. |

### math.sqrt(x) ⇒ `number`
Calculates the non-negative square root of `x`.

Returns the resulting square root value.

 - If `x` is `+0` (`-0`) then `+0` (`-0`) is returned.
 - If `x` is positive infinity, positive infinity is returned.
 - If `x` is less than `-0`, a domain error occurs, and `NaN` is returned.

Returns `NaN` if the `x` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | Value to calculate square root for. |

### math.cbrt(x) ⇒ `double`
Calculates the cube root of `x`.

Returns the resulting cube root value.

 - If `x` is `+0` (`-0`) then `+0` (`-0`) is returned.
 - If `x` is (+/-) infinity, (+/-) infinity is returned.

Returns `NaN` if the `x` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | Value to calculate cube root for. |

**Example**  
```ucode
cbrt(27);  // 3.0
cbrt(0);   // 0.0
cbrt(-27); // -3.0
```

### math.hypot(x, y) ⇒ `double`
Computes the square root of the sum of the squares of `x` and `y`, i.e.
the hypotenuse without undue overflow or underflow at intermediate stages of
the computation.

Returns the result of `sqrt(x^2 + y^2)`.

 - If `x` and `y` are `+0` (`-0`) then `+0` (`-0`) is returned.
 - If `x` or `y` is `+0` (`-0`) then `+y` or `+x` is returned.
 - If `x` or `y` is (+/-) infinity, (+/-) infinity is returned.

Returns `NaN` if the `x` or `y` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | base |
| y | `double` | height |

**Example**  
```ucode
hypot(3, 3);   // 4.2426406871193
hypot(2, 2);   // 2.8284271247462
hypot(1, 1);   // 1.4142135623731
hypot(0, 0);   // 0.0
hypot(-1, -1); // -1.4142135623731
```

### math.pow(x, y) ⇒ `number`
Calculates the value of `x` raised to the power of `y`.

On success, returns the value of `x` raised to the power of `y`.

 - If the result overflows, a range error occurs, and the function
   returns `Infinity`.
 - If result underflows, and is not representable, a range error
   occurs, and `0.0` with the appropriate sign is returned.
 - If `x` is `+0` or `-0`, and `y` is an odd integer less than `0`,
   a pole error occurs `Infinity` is returned, with the same sign
   as `x`.
 - If `x` is `+0` or `-0`, and `y` is less than `0` and not an odd
   integer, a pole error occurs and `Infinity` is returned.
 - If `x` is `+0` (`-0`), and `y` is an odd integer greater than `0`,
   the result is `+0` (`-0`).
 - If `x` is `0`, and `y` greater than `0` and not an odd integer,
   the result is `+0`.
 - If `x` is `-1`, and `y` is positive infinity or negative infinity,
   the result is `1.0`.
 - If `x` is `+1`, the result is `1.0` (even if `y` is `NaN`).
 - If `y` is `0`, the result is `1.0` (even if `x` is `NaN`).
 - If `x` is a finite value less than `0`, and `y` is a finite
   non-integer, a domain error occurs, and `NaN` is returned.
 - If the absolute value of `x` is less than `1`, and `y` is negative
   infinity, the result is positive infinity.
 - If the absolute value of `x` is greater than `1`, and `y` is
   negative infinity, the result is `+0`.
 - If the absolute value of `x` is less than `1`, and `y` is positive
   infinity, the result is `+0`.
 - If the absolute value of `x` is greater than `1`, and `y` is positive
   infinity, the result is positive infinity.
 - If `x` is negative infinity, and `y` is an odd integer less than `0`,
   the result is `-0`.
 - If `x` is negative infinity, and `y` less than `0` and not an odd
   integer, the result is `+0`.
 - If `x` is negative infinity, and `y` is an odd integer greater than
   `0`, the result is negative infinity.
 - If `x` is negative infinity, and `y` greater than `0` and not an odd
   integer, the result is positive infinity.
 - If `x` is positive infinity, and `y` less than `0`, the result is `+0`.
 - If `x` is positive infinity, and `y` greater than `0`, the result is
   positive infinity.

Returns `NaN` if either the `x` or `y` value can't be converted to a number.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | The base value. |
| y | `number` | The power value. |

### math.rand([a], [b]) ⇒ `number`
Depending on the arguments, it produces a pseudo-random positive integer, 
or a pseudo-random number in a supplied range.

Without arguments it returns the calculated pseuo-random value. The value 
is within the range `0` to `RAND_MAX` inclusive where `RAND_MAX` is a platform 
specific value guaranteed to be at least `32767`.

With 2 arguments `a, b` it returns a number in the range `a` to `b` inclusive.
With a single argument `a` it returns a number in the range `0` to `a` inclusive.

The [`srand()`](#module_math+srand) function sets its argument as the
seed for a new sequence of pseudo-random integers to be returned by `rand()`.
These sequences are repeatable by calling [`srand()`](#module_math+srand)
with the same seed value.

If no seed value is explicitly set by calling
[`srand()`](#module_math+srand) prior to the first call to `rand()`,
the math module will automatically seed the PRNG once, using the current
time of day in milliseconds as seed value.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| [a] | `number` | End of the desired range. |
| [b] | `number` | The other end of the desired range. |

### math.srand(seed)
Seeds the pseudo-random number generator.

This functions seeds the PRNG with the given value and thus affects the
pseudo-random integer sequence produced by subsequent calls to
[`rand()`](#module_math+rand).

Setting the same seed value will result in the same pseudo-random numbers
produced by [`rand()`](#module_math+rand).

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| seed | `number` | The seed value. |

### math.isnan(x) ⇒ `boolean`
Tests whether `x` is a `NaN` double.

This functions checks whether the given argument is of type `double` with
a `NaN` (not a number) value.

Returns `true` if the value is `NaN`, otherwise false.

Note that a value can also be checked for `NaN` with the expression
`x !== x` which only evaluates to `true` if `x` is `NaN`.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | The value to test. |

### math.isinf(x) ⇒ `boolean`
Tests whether `x` is double precision `Infinity`.

This functions checks whether the given argument is of type `double` of
`Infinity` value. Double precision values >= 1.8e308 are considered `Infinity`.

Returns `true` if the value is `Infinity`, otherwise false.

**Kind**: instance method of [`math`](#module_math)  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | The value to test. |

### math.deg2rad(number) ⇒ `number`
Returns the radian value of the given degree value.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - Returns the absolute value or `NaN` if the given argument could
not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| number | `double` | The number to return the radian value for. |

**Example**  
```ucode
deg2rad(180);   // 3.1415926535898
deg2rad("180"); // 3.1415926535898
```

### math.rad2deg(number) ⇒ `number`
Returns the degree value of the given radian value.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - Returns the absolute value or `NaN` if the given argument could
not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| number | `double` | The number to return the degree value for. |

**Example**  
```ucode
rad2deg(3.1415926535898);   // 180.0
rad2deg("3.1415926535898"); // 180.0
```

### math.fmin(x, y) ⇒ `double`
Returns the lesser of two values x and y.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - Returns the lesser of the two values x or y or `NaN` if a given argument
could not be converted to a number. Use `(-)Infinity` or `NAN` for
comparisons involving said values.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | first parameter |
| y | `double` | second parameter |

**Example**  
```ucode
fmin("180", "-180");   // -180.0
fmin(180, -180);       // -180.0
fmin(-Infinity, 0);    // -1e309 i.e. -infinity in double type representation.
```

### math.fmax(x, y) ⇒ `double`
Returns the greater of two values x and y.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - Returns the greater of the two values x or y or `NaN` if a given argument
could not be converted to a number. Use `(-)Infinity` or `NAN` for
comparisons involving said values.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | first parameter |
| y | `double` | second parameter |

**Example**  
```ucode
fmax("180", "-180");   // 180.0
fmax(180, -180);       // 180.0
fmax(Infinity, 0);     // 1e309 i.e. infinity in double type representation.
```

### math.clamp(x, upper, lower) ⇒ `double`
Clamps `x` to within `upper` and `lower` bounds if `x` exceeds them.

The operation is effectively: `min(upper, max(x, lower))`.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - Returns `x` if within `upper` and `lower`, otherwise one of `lower` or `upper`
if `x` exceeds those bounds, or `NaN` if any given argument
could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number to clamp |
| upper | `double` | upper bound |
| lower | `double` | lower bound |

**Example**  
```ucode
clamp(1000, 200, 180);   // 200.0
clamp(-1000, 200, 180);  // 180.0
clamp(190, 200, 180);    // 190.0
```

### math.sign(x) ⇒ `integer`
Returns -1 or 1 depending on the sign of the given number, or 0 if the given
number itself is zero.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `integer` - Returns -1 or 1 for negative and positive inputs respectively, 0 if the given
number is zero, or `NaN` if the given argument could not be converted to a
number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
sign(2);   // 1
sign(-8);  // -1
sign(0);   // 0
sign(-0);  // 0
```

### math.signbit(x) ⇒ `integer`
Returns -1 or 1 depending on the sign of the given number, or 0 if the given
number itself is zero. IEEE-754 behaviour.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `integer` - Returns -1 or 1 for negative and positive inputs respectively, 0 if the given
number is zero, -1 for -0.0, or `NaN` if the given argument could not be
converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
signbit(2);    // 1
signbit(-8);   // -1
signbit(0);    // 0
signbit(-0.0); // -1
signbit(-0);   // 0
```

### math.signnz(x) ⇒ `integer`
Returns -1 or 1 depending on the sign of the given number only (no zero).
(-)Zero effectively becomes 1.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `integer` - Returns -1 or +1 for negative and positive inputs respectively, and zero is
converted to +1, or `NaN` if the given argument could not be converted to a
number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |

**Example**  
```ucode
signnz(2);   // 1
signnz(-8);  // -1
signnz(0);   // 1
signnz(-0);  // 1
```

### math.copysign(x, y) ⇒ `double`
Returns a double whose magnitude is that of `x`, but whose sign is that of
`y`.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `double` - Returns `NaN` if a given argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |
| y | `double` | number |

**Example**  
```ucode
copysign(-3, -5);  // -3.0
copysign(8, -5);   // -8.0
copysign(-0, 3);   // 0.0
```

### math.floor(x, output_type) ⇒ `number`
Floors `x` to the largest integer value not greater than `x`.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - Returns the largest integer value not greater than `x`, or `NaN` if the given
argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |
| output_type | `boolean` | false is `integer`, true is `double`. |

**Example**  
```ucode
floor(2.7);        // 2
floor(2.7, true);  // 2.0
floor(-2.7);       // -3
floor(-0.0);       // 0
floor(-0.0, true); // -0.0
floor(-Infinity);  // -1e309 i.e. -infinity in double type representation.
```

### math.ceil(x, output_type) ⇒ `number`
Computes the smallest integer value not less than `x`.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - Returns the smallest integer value not less than `x`, or `NaN` if the given
argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |
| output_type | `boolean` | false is `integer`, true is `double`. |

**Example**  
```ucode
ceil(2.7);        // 3
ceil(2.7, true);  // 3.0
ceil(-2.7);       // -2
ceil(-0.0);       // 0
ceil(-0.0, true); // -0.0
ceil(-Infinity);  // -1e309 i.e. -infinity in double type representation.
```

### math.round(x, output_type) ⇒ `number`
Returns the integral value nearest to x rounding half-way cases away
from zero, regardless of the current rounding direction.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - Returns the rounded integer value of `x`, or `NaN` if the given
argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `double` | number |
| output_type | `boolean` | false is `integer`, true is `double`. |

**Example**  
```ucode
round(2.4);        // 2
round(2.5);        // 3
round(2.7);        // 3
round(2.7, true);  // 3.0
round(-2.4);       // -2
round(-2.5);       // -3
round(-2.7);       // -3
round(-0.0);       // 0
round(-0.0, true); // -0.0
round(-Infinity);  // -1e309 i.e. -infinity in double type representation.
```

### math.trunc(x, output_type) ⇒ `number`
Truncate away the decimal portion to produce the nearest integer not greater
in magnitude than x.

**Kind**: instance method of [`math`](#module_math)  
**Returns**: `number` - The integral portion remaining after the decimal portion is truncated, or
`NaN` if the given argument could not be converted to a number.  

| Param | Type | Description |
| --- | --- | --- |
| x | `number` | number |
| output_type | `boolean` | false is `integer`, true is `double`. |

**Example**  
```ucode
trunc(2.4);        // 2
trunc(2.5);        // 2
trunc(2.7);        // 2
trunc(2.7, true);  // 2.0
trunc(-2.4);       // -2
trunc(-2.5);       // -2
trunc(-2.7);       // -2
trunc(-0.0);       // 0
trunc(-0.0, true); // -0.0
```

---

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

---

# ucode module: nl80211

> **Live docs:** https://ucode.mein.io/module-nl80211.html

---

## Wireless Netlink

The `nl80211` module provides functions for interacting with the nl80211 netlink interface
for wireless networking configuration and management.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import * as nl80211 from 'nl80211';

  // Send a nl80211 request
  let response = nl80211.request(nl80211.const.NL80211_CMD_GET_WIPHY, 0, { wiphy: 0 });

  // Create a listener for wireless events
  let wifiListener = nl80211.listener((msg) => {
      print('Received wireless event:', msg, '\n');
  }, [nl80211.const.NL80211_CMD_NEW_INTERFACE, nl80211.const.NL80211_CMD_DEL_INTERFACE]);

  // Wait for a specific nl80211 event
  let event = nl80211.waitfor([nl80211.const.NL80211_CMD_NEW_SCAN_RESULTS], 5000);
  if (event)
      print('Received scan results:', event.msg, '\n');
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as nl80211 from 'nl80211';

  // Send a nl80211 request
  let response = nl80211.request(nl80211.const.NL80211_CMD_GET_WIPHY, 0, { wiphy: 0 });

  // Create a listener for wireless events
  let listener = nl80211.listener((msg) => {
      print('Received wireless event:', msg, '\n');
  }, [nl80211.const.NL80211_CMD_NEW_INTERFACE, nl80211.const.NL80211_CMD_DEL_INTERFACE]);
  ```

Additionally, the nl80211 module namespace may also be imported by invoking
the `ucode` interpreter with the `-lnl80211` switch.

### nl80211.listener
**Kind**: static class of [`nl80211`](#module_nl80211)  
**See**: [listener()](module:nl80211#listener)  

### nl80211~Netlink message flags
**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NLM_F_ACK | `number` | Request for acknowledgment |
| NLM_F_ACK_TLVS | `number` | Request for acknowledgment with TLVs |
| NLM_F_APPEND | `number` | Append to existing list |
| NLM_F_ATOMIC | `number` | Atomic operation |
| NLM_F_CAPPED | `number` | Request capped |
| NLM_F_CREATE | `number` | Create if not exists |
| NLM_F_DUMP | `number` | Dump request |
| NLM_F_DUMP_FILTERED | `number` | Dump filtered request |
| NLM_F_DUMP_INTR | `number` | Dump interrupted |
| NLM_F_ECHO | `number` | Echo request |
| NLM_F_EXCL | `number` | Exclusive creation |
| NLM_F_MATCH | `number` | Match request |
| NLM_F_MULTI | `number` | Multi-part message |
| NLM_F_NONREC | `number` | Non-recursive operation |
| NLM_F_REPLACE | `number` | Replace existing |
| NLM_F_REQUEST | `number` | Request message |
| NLM_F_ROOT | `number` | Root operation |

### nl80211~nl80211 commands
**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_CMD_GET_WIPHY | `number` | Get wireless PHY attributes |
| NL80211_CMD_SET_WIPHY | `number` | Set wireless PHY attributes |
| NL80211_CMD_NEW_WIPHY | `number` | Create new wireless PHY |
| NL80211_CMD_DEL_WIPHY | `number` | Delete wireless PHY |
| NL80211_CMD_GET_INTERFACE | `number` | Get interface information |
| NL80211_CMD_SET_INTERFACE | `number` | Set interface attributes |
| NL80211_CMD_NEW_INTERFACE | `number` | Create new interface |
| NL80211_CMD_DEL_INTERFACE | `number` | Delete interface |
| NL80211_CMD_GET_KEY | `number` | Get key |
| NL80211_CMD_SET_KEY | `number` | Set key |
| NL80211_CMD_NEW_KEY | `number` | Add new key |
| NL80211_CMD_DEL_KEY | `number` | Delete key |
| NL80211_CMD_GET_BEACON | `number` | Get beacon |
| NL80211_CMD_SET_BEACON | `number` | Set beacon |
| NL80211_CMD_NEW_BEACON | `number` | Set beacon (alias) |
| NL80211_CMD_STOP_AP | `number` | Stop AP operation |
| NL80211_CMD_DEL_BEACON | `number` | Delete beacon |
| NL80211_CMD_GET_STATION | `number` | Get station information |
| NL80211_CMD_SET_STATION | `number` | Set station attributes |
| NL80211_CMD_NEW_STATION | `number` | Add new station |
| NL80211_CMD_DEL_STATION | `number` | Delete station |
| NL80211_CMD_GET_MPATH | `number` | Get mesh path |
| NL80211_CMD_SET_MPATH | `number` | Set mesh path |
| NL80211_CMD_NEW_MPATH | `number` | Add new mesh path |
| NL80211_CMD_DEL_MPATH | `number` | Delete mesh path |
| NL80211_CMD_SET_BSS | `number` | Set BSS attributes |
| NL80211_CMD_SET_REG | `number` | Set regulatory domain |
| NL80211_CMD_REQ_SET_REG | `number` | Request regulatory domain change |
| NL80211_CMD_GET_MESH_CONFIG | `number` | Get mesh configuration |
| NL80211_CMD_SET_MESH_CONFIG | `number` | Set mesh configuration |
| NL80211_CMD_GET_REG | `number` | Get regulatory domain |
| NL80211_CMD_GET_SCAN | `number` | Get scan results |
| NL80211_CMD_TRIGGER_SCAN | `number` | Trigger scan |
| NL80211_CMD_NEW_SCAN_RESULTS | `number` | New scan results available |
| NL80211_CMD_SCAN_ABORTED | `number` | Scan aborted |
| NL80211_CMD_REG_CHANGE | `number` | Regulatory domain change |
| NL80211_CMD_AUTHENTICATE | `number` | Authenticate |
| NL80211_CMD_ASSOCIATE | `number` | Associate |
| NL80211_CMD_DEAUTHENTICATE | `number` | Deauthenticate |
| NL80211_CMD_DISASSOCIATE | `number` | Disassociate |
| NL80211_CMD_MICHAEL_MIC_FAILURE | `number` | Michael MIC failure |
| NL80211_CMD_REG_BEACON_HINT | `number` | Beacon regulatory hint |
| NL80211_CMD_JOIN_IBSS | `number` | Join [IBSS](../wiki/chunked-reference/wiki_page-techref-wireless-modes.md) |
| NL80211_CMD_LEAVE_IBSS | `number` | Leave [IBSS](../wiki/chunked-reference/wiki_page-techref-wireless-modes.md) |
| NL80211_CMD_TESTMODE | `number` | Test mode |
| NL80211_CMD_CONNECT | `number` | Connect |
| NL80211_CMD_ROAM | `number` | Roam |
| NL80211_CMD_DISCONNECT | `number` | Disconnect |
| NL80211_CMD_SET_WIPHY_NETNS | `number` | Set wireless PHY network namespace |
| NL80211_CMD_GET_SURVEY | `number` | Get survey data |
| NL80211_CMD_NEW_SURVEY_RESULTS | `number` | New survey results |
| NL80211_CMD_SET_PMKSA | `number` | Set PMKSA |
| NL80211_CMD_DEL_PMKSA | `number` | Delete PMKSA |
| NL80211_CMD_FLUSH_PMKSA | `number` | Flush PMKSA |
| NL80211_CMD_REMAIN_ON_CHANNEL | `number` | Remain on channel |
| NL80211_CMD_CANCEL_REMAIN_ON_CHANNEL | `number` | Cancel remain on channel |
| NL80211_CMD_SET_TX_BITRATE_MASK | `number` | Set TX bitrate mask |
| NL80211_CMD_REGISTER_FRAME | `number` | Register frame |
| NL80211_CMD_REGISTER_ACTION | `number` | Register action frame |
| NL80211_CMD_FRAME | `number` | Frame |
| NL80211_CMD_ACTION | `number` | Action frame |
| NL80211_CMD_FRAME_TX_STATUS | `number` | Frame TX status |
| NL80211_CMD_ACTION_TX_STATUS | `number` | Action TX status |
| NL80211_CMD_SET_POWER_SAVE | `number` | Set power save |
| NL80211_CMD_GET_POWER_SAVE | `number` | Get power save |
| NL80211_CMD_SET_CQM | `number` | Set CQM |
| NL80211_CMD_NOTIFY_CQM | `number` | Notify CQM |
| NL80211_CMD_SET_CHANNEL | `number` | Set channel |
| NL80211_CMD_SET_WDS_PEER | `number` | Set WDS peer |
| NL80211_CMD_FRAME_WAIT_CANCEL | `number` | Cancel frame wait |
| NL80211_CMD_JOIN_MESH | `number` | Join mesh |
| NL80211_CMD_LEAVE_MESH | `number` | Leave mesh |
| NL80211_CMD_UNPROT_DEAUTHENTICATE | `number` | Unprotected deauthenticate |
| NL80211_CMD_UNPROT_DISASSOCIATE | `number` | Unprotected disassociate |
| NL80211_CMD_NEW_PEER_CANDIDATE | `number` | New peer candidate |
| NL80211_CMD_GET_WOWLAN | `number` | Get WoWLAN |
| NL80211_CMD_SET_WOWLAN | `number` | Set WoWLAN |
| NL80211_CMD_START_SCHED_SCAN | `number` | Start scheduled scan |
| NL80211_CMD_STOP_SCHED_SCAN | `number` | Stop scheduled scan |
| NL80211_CMD_SCHED_SCAN_RESULTS | `number` | Scheduled scan results |
| NL80211_CMD_SCHED_SCAN_STOPPED | `number` | Scheduled scan stopped |
| NL80211_CMD_SET_REKEY_OFFLOAD | `number` | Set rekey offload |
| NL80211_CMD_PMKSA_CANDIDATE | `number` | PMKSA candidate |
| NL80211_CMD_TDLS_OPER | `number` | TDLS operation |
| NL80211_CMD_TDLS_MGMT | `number` | TDLS management |
| NL80211_CMD_UNEXPECTED_FRAME | `number` | Unexpected frame |
| NL80211_CMD_PROBE_CLIENT | `number` | Probe client |
| NL80211_CMD_REGISTER_BEACONS | `number` | Register beacons |
| NL80211_CMD_UNEXPECTED_4ADDR_FRAME | `number` | Unexpected 4-address frame |
| NL80211_CMD_SET_NOACK_MAP | `number` | Set no-ack map |
| NL80211_CMD_CH_SWITCH_NOTIFY | `number` | Channel switch notify |
| NL80211_CMD_START_P2P_DEVICE | `number` | Start P2P device |
| NL80211_CMD_STOP_P2P_DEVICE | `number` | Stop P2P device |
| NL80211_CMD_CONN_FAILED | `number` | Connection failed |
| NL80211_CMD_SET_MCAST_RATE | `number` | Set multicast rate |
| NL80211_CMD_SET_MAC_ACL | `number` | Set MAC ACL |
| NL80211_CMD_RADAR_DETECT | `number` | Radar detect |
| NL80211_CMD_GET_PROTOCOL_FEATURES | `number` | Get protocol features |
| NL80211_CMD_UPDATE_FT_IES | `number` | Update FT IEs |
| NL80211_CMD_FT_EVENT | `number` | FT event |
| NL80211_CMD_CRIT_PROTOCOL_START | `number` | Start critical protocol |
| NL80211_CMD_CRIT_PROTOCOL_STOP | `number` | Stop critical protocol |
| NL80211_CMD_GET_COALESCE | `number` | Get coalesce |
| NL80211_CMD_SET_COALESCE | `number` | Set coalesce |
| NL80211_CMD_CHANNEL_SWITCH | `number` | Channel switch |
| NL80211_CMD_VENDOR | `number` | Vendor command |
| NL80211_CMD_SET_QOS_MAP | `number` | Set QoS map |
| NL80211_CMD_ADD_TX_TS | `number` | Add TX TS |
| NL80211_CMD_DEL_TX_TS | `number` | Delete TX TS |
| NL80211_CMD_GET_MPP | `number` | Get MPP |
| NL80211_CMD_JOIN_OCB | `number` | Join OCB |
| NL80211_CMD_LEAVE_OCB | `number` | Leave OCB |
| NL80211_CMD_CH_SWITCH_STARTED_NOTIFY | `number` | Channel switch started notify |
| NL80211_CMD_TDLS_CHANNEL_SWITCH | `number` | TDLS channel switch |
| NL80211_CMD_TDLS_CANCEL_CHANNEL_SWITCH | `number` | Cancel TDLS channel switch |
| NL80211_CMD_ABORT_SCAN | `number` | Abort scan |

### nl80211~Scan flags
Constants for NL80211_ATTR_SCAN_FLAGS bitmask.

**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_SCAN_FLAG_LOW_PRIORITY | `number` | Low priority scan |
| NL80211_SCAN_FLAG_FLUSH | `number` | Flush scan results before returning |
| NL80211_SCAN_FLAG_AP | `number` | Force AP mode scan |
| NL80211_SCAN_FLAG_RANDOM_ADDR | `number` | Randomize source MAC address |
| NL80211_SCAN_FLAG_FILS_MAX_CHANNEL_TIME | `number` | FILS max channel time |
| NL80211_SCAN_FLAG_ACCEPT_BCAST_PROBE_RESP | `number` | Accept broadcast probe responses |
| NL80211_SCAN_FLAG_OCE_PROBE_REQ_HIGH_TX_RATE | `number` | OCE high TX rate probe requests |
| NL80211_SCAN_FLAG_OCE_PROBE_REQ_DEFERRAL_SUPPRESSION | `number` | OCE probe request deferral suppression |
| NL80211_SCAN_FLAG_LOW_SPAN | `number` | Low span scan |
| NL80211_SCAN_FLAG_LOW_POWER | `number` | Low power scan |
| NL80211_SCAN_FLAG_HIGH_ACCURACY | `number` | High accuracy scan |
| NL80211_SCAN_FLAG_RANDOM_SN | `number` | Randomize sequence number |
| NL80211_SCAN_FLAG_MIN_PREQ_CONTENT | `number` | Minimize probe request content |
| NL80211_SCAN_FLAG_FREQ_KHZ | `number` | Report scan results with frequency in KHz |
| NL80211_SCAN_FLAG_COLOCATED_6GHZ | `number` | Scan colocated 6GHz BSS |

### nl80211~BSS status constants
Constants for BSS status values.

**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_BSS_STATUS_AUTHENTICATED | `number` | Authenticated with BSS |
| NL80211_BSS_STATUS_ASSOCIATED | `number` | Associated with BSS |
| NL80211_BSS_STATUS_IBSS_JOINED | `number` | Joined [IBSS](../wiki/chunked-reference/wiki_page-techref-wireless-modes.md) |

### nl80211~BSS use-for and cannot-use-reasons constants
Constants for BSS use-for and cannot-use-reasons bitmasks.

**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_BSS_USE_FOR_NORMAL | `number` | Use BSS for normal connection |
| NL80211_BSS_USE_FOR_MLD_LINK | `number` | Use BSS as MLD link |
| NL80211_BSS_CANNOT_USE_NSTR_NONPRIMARY | `number` | NSTR nonprimary link not usable |
| NL80211_BSS_CANNOT_USE_6GHZ_PWR_MISMATCH | `number` | 6GHz power mode mismatch |

### nl80211~HWSIM commands
**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| HWSIM_CMD_REGISTER | `number` | Register radio |
| HWSIM_CMD_FRAME | `number` | Send frame |
| HWSIM_CMD_TX_INFO_FRAME | `number` | Send TX info frame |
| HWSIM_CMD_NEW_RADIO | `number` | Create new radio |
| HWSIM_CMD_DEL_RADIO | `number` | Delete radio |
| HWSIM_CMD_GET_RADIO | `number` | Get radio information |
| HWSIM_CMD_ADD_MAC_ADDR | `number` | Add MAC address |
| HWSIM_CMD_DEL_MAC_ADDR | `number` | Delete MAC address |
| HWSIM_CMD_START_PMSR | `number` | Start peer measurement |
| HWSIM_CMD_ABORT_PMSR | `number` | Abort peer measurement |
| HWSIM_CMD_REPORT_PMSR | `number` | Report peer measurement |

### nl80211~Interface types
**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_IFTYPE_ADHOC | `number` | [IBSS](../wiki/chunked-reference/wiki_page-techref-wireless-modes.md)/ad-hoc interface |
| NL80211_IFTYPE_STATION | `number` | Station interface |
| NL80211_IFTYPE_AP | `number` | Access point interface |
| NL80211_IFTYPE_AP_VLAN | `number` | AP VLAN interface |
| NL80211_IFTYPE_WDS | `number` | WDS interface |
| NL80211_IFTYPE_MONITOR | `number` | Monitor interface |
| NL80211_IFTYPE_MESH_POINT | `number` | Mesh point interface |
| NL80211_IFTYPE_P2P_CLIENT | `number` | P2P client interface |
| NL80211_IFTYPE_P2P_GO | `number` | P2P group owner interface |
| NL80211_IFTYPE_P2P_DEVICE | `number` | P2P device interface |
| NL80211_IFTYPE_OCB | `number` | Outside context of BSS (OCB) interface |

### nl80211~States of a mesh peer link
**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_PLINK_LISTEN | `number` | initial state of non-existent mesh peer links |
| NL80211_PLINK_OPN_SNT | `number` | mesh plink open frame has been sent |
| NL80211_PLINK_OPN_RCVD | `number` | mesh plink open frame has been received |
| NL80211_PLINK_CNF_RCVD | `number` | mesh plink confirm frame has been received |
| NL80211_PLINK_ESTAB | `number` | mesh peer link is established |
| NL80211_PLINK_HOLDING | `number` | mesh peer link is being closed or cancelled |
| NL80211_PLINK_BLOCKED | `number` | all frames are discarded, except for authentication frames |

### nl80211~Actions on mesh peer links
**Kind**: inner typedef of [`nl80211`](#module_nl80211)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NL80211_PLINK_ACTION_NO_ACTION | `number` | perform no action |
| NL80211_PLINK_ACTION_OPEN | `number` | start mesh peer link establishment |
| NL80211_PLINK_ACTION_BLOCK | `number` | block traffic from this mesh peer |

---

# ucode module: resolv

> **Live docs:** https://ucode.mein.io/module-resolv.html

---

## DNS Resolution Module

The `resolv` module provides DNS resolution functionality for ucode, allowing
you to perform DNS queries for various record types and handle responses.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { query } from 'resolv';

  let result = query('example.com', { type: ['A'] });
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as resolv from 'resolv';

  let result = resolv.query('example.com', { type: ['A'] });
  ```

Additionally, the resolv module namespace may also be imported by invoking
the `ucode` interpreter with the `-lresolv` switch.

## Record Types

The module supports the following DNS record types:

| Type    | Description                    |
|---------|--------------------------------|
| `A`     | IPv4 address record            |
| `AAAA`  | IPv6 address record            |
| `CNAME` | Canonical name record          |
| `MX`    | Mail exchange record           |
| `NS`    | Name server record             |
| `PTR`   | Pointer record (reverse DNS)   |
| `SOA`   | Start of authority record      |
| `SRV`   | Service record                 |
| `TXT`   | Text record                    |
| `ANY`   | Any available record type      |

## Response Codes

DNS queries can return the following response codes:

| Code        | Description                               |
|-------------|-------------------------------------------|
| `NOERROR`   | No error, query successful                |
| `FORMERR`   | Format error in query                     |
| `SERVFAIL`  | Server failure                            |
| `NXDOMAIN`  | Non-existent domain                       |
| `NOTIMP`    | Not implemented                           |
| `REFUSED`   | Query refused                             |
| `TIMEOUT`   | Query timed out                           |

## Response Format

DNS query results are returned as objects where:
- Keys are the queried domain names
- Values are objects containing arrays of records grouped by type
- Special `rcode` property indicates query status for failed queries

### Record Format by Type

**A and AAAA records:**
```json
{
  "example.com": {
    "A": ["192.0.2.1", "192.0.2.2"],
    "AAAA": ["2001:db8::1", "2001:db8::2"]
  }
}
```

**MX records:**
```json
{
  "example.com": {
    "MX": [
      [10, "mail1.example.com"],
      [20, "mail2.example.com"]
    ]
  }
}
```

**SRV records:**
```json
{
  "_http._tcp.example.com": {
    "SRV": [
      [10, 5, 80, "web1.example.com"],
      [10, 10, 80, "web2.example.com"]
    ]
  }
}
```

**SOA records:**
```json
{
  "example.com": {
    "SOA": [
      [
        "ns1.example.com",      // primary nameserver
        "admin.example.com",    // responsible mailbox
        2023010101,             // serial number
        3600,                   // refresh interval
        1800,                   // retry interval
        604800,                 // expire time
        86400                   // minimum TTL
      ]
    ]
  }
}
```

**TXT, NS, CNAME, PTR records:**
```json
{
  "example.com": {
    "TXT": ["v=spf1 include:_spf.example.com ~all"],
    "NS": ["ns1.example.com", "ns2.example.com"],
    "CNAME": ["alias.example.com"]
  }
}
```

**Error responses:**
```json
{
  "nonexistent.example.com": {
    "rcode": "NXDOMAIN"
  }
}
```

## Examples

Basic A record lookup:

```ucode
import { query } from 'resolv';

const result = query(['example.com']);
print(result, "\n");
// {
//   "example.com": {
//     "A": ["192.0.2.1"],
//     "AAAA": ["2001:db8::1"]
//   }
// }
```

Specific record type query:

```ucode
const mxRecords = query(['example.com'], { type: ['MX'] });
print(mxRecords, "\n");
// {
//   "example.com": {
//     "MX": [[10, "mail.example.com"]]
//   }
// }
```

Multiple domains and types:

```ucode
const results = query(
  ['example.com', 'google.com'],
  { 
    type: ['A', 'MX'],
    timeout: 10000,
    nameserver: ['8.8.8.8', '1.1.1.1']
  }
);
```

Reverse DNS lookup:

```ucode
const ptrResult = query(['192.0.2.1'], { type: ['PTR'] });
print(ptrResult, "\n");
// {
//   "1.2.0.192.in-addr.arpa": {
//     "PTR": ["example.com"]
//   }
// }
```

### resolv.query(names, [options]) ⇒ `object`
Perform DNS queries for specified domain names.

The `query()` function performs DNS lookups for one or more domain names
according to the specified options. It returns a structured object containing
all resolved DNS records grouped by domain name and record type.

If no record types are specified in the options, the function will perform
both A and AAAA record lookups for regular domain names, or PTR record
lookups for IP addresses (reverse DNS).

Returns an object containing DNS query results organized by domain name.

Raises a runtime exception if invalid arguments are provided or if DNS
resolution encounters critical errors.

**Kind**: instance method of [`resolv`](#module_resolv)  
**Returns**: `object` - Object containing DNS query results. Keys are domain names, values are
objects containing arrays of records grouped by type, or error information
for failed queries.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| names | `string` \| `Array.<string>` |  | Domain name(s) to query. Can be a single domain name string or an array of domain name strings. IP addresses can also be provided for reverse DNS lookups. |
| [options] | `object` |  | Query options object. |
| [options.type] | `Array.<string>` |  | Array of DNS record types to query for. Valid types are: 'A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT', 'ANY'. If not specified, defaults to 'A' and 'AAAA' for domain names, or 'PTR' for IP addresses. |
| [options.nameserver] | `Array.<string>` |  | Array of DNS nameserver addresses to query. Each address can optionally include a port number using '#' separator (e.g., '8.8.8.8#53'). IPv6 addresses can include interface scope using '%' separator. If not specified, nameservers are read from /etc/resolv.conf, falling back to '127.0.0.1'. |
| [options.timeout] | `number` | `5000` | Total timeout for all queries in milliseconds. |
| [options.retries] | `number` | `2` | Number of attempts spread over the timeout; must be at least 1. Passing 0 or a negative value is rejected with an EINVAL error. |
| [options.edns_maxsize] | `number` | `4096` | Maximum UDP packet size for EDNS (Extension Mechanisms for DNS). Set to 0 to disable EDNS. |
| [options.txt_as_array] | `boolean` | `false` | Return TXT record strings as array elements instead of space-joining all record strings into one single string per record. |

**Example**  
```ucode
// Basic A and AAAA record lookup
const result = query('example.com');
print(result, "\n");
// {
//   "example.com": {
//     "A": ["192.0.2.1"],
//     "AAAA": ["2001:db8::1"]
//   }
// }
```
**Example**  
```ucode
// Specific record type queries
const mxResult = query('example.com', { type: ['MX'] });
print(mxResult, "\n");
// {
//   "example.com": {
//     "MX": [[10, "mail.example.com"]]
//   }
// }
```
**Example**  
```ucode
// Multiple domains and types with custom nameserver
const results = query(
  ['example.com', 'google.com'],
  {
    type: ['A', 'MX'],
    nameserver: ['8.8.8.8', '1.1.1.1'],
    timeout: 10000
  }
);
```
**Example**  
```ucode
// Reverse DNS lookup
const ptrResult = query(['192.0.2.1'], { type: ['PTR'] });
print(ptrResult, "\n");
// {
//   "1.2.0.192.in-addr.arpa": {
//     "PTR": ["example.com"]
//   }
// }
```
**Example**  
```ucode
// TXT record with multiple elements
const txtResult = query(['_spf.facebook.com'], { type: ['TXT'], txt_as_array: true });
printf(txtResult, "\n");
// {
//   "_spf.facebook.com": {
//     "TXT": [
//       [
//         "v=spf1 ip4:66.220.144.128/25 ip4:66.220.155.0/24 ip4:66.220.157.0/25 ip4:69.63.178.128/25 ip4:69.63.181.0/24 ip4:69.63.184.0/25",
//         " ip4:69.171.232.0/24 ip4:69.171.244.0/23 -all"
//       ]
//     ]
//   }
// }
```
**Example**  
```ucode
// Handling errors
const errorResult = query(['nonexistent.example.com']);
print(errorResult, "\n");
// {
//   "nonexistent.example.com": {
//     "rcode": "NXDOMAIN"
//   }
// }
```

### resolv.error() ⇒ `string` \| `null`
Get the last error message from DNS operations.

The `error()` function returns a descriptive error message for the last
failed DNS operation, or `null` if no error occurred. This function is
particularly useful for debugging DNS resolution issues.

After calling this function, the stored error state is cleared, so
subsequent calls will return `null` unless a new error occurs.

Returns a string describing the last error, or `null` if no error occurred.

**Kind**: instance method of [`resolv`](#module_resolv)  
**Returns**: `string` \| `null` - A descriptive error message for the last failed operation, or `null` if
no error occurred.  
**Example**  
```ucode
// Check for errors after a failed query
const result = query("example.org", { nameserver: "invalid..domain" });
const err = error();
if (err) {
  print("DNS query failed: ", err, "\n");
}
```

---

# ucode module: rtnl

> **Live docs:** https://ucode.mein.io/module-rtnl.html

---

## Routing Netlink

The `rtnl` module provides functions for interacting with the routing netlink interface.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { error, request, listener, RTM_GETROUTE, RTM_NEWROUTE, RTM_DELROUTE, AF_INET } from 'rtnl';

  // Send a netlink request
  let response = request(RTM_GETROUTE, 0, { family: AF_INET });

  // Create a listener for route changes
  let routeListener = listener((msg) => {
      print('Received route message:', msg, '\n');
  }, [RTM_NEWROUTE, RTM_DELROUTE]);
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as rtnl from 'rtnl';

  // Send a netlink request
  let response = rtnl.request(rtnl.RTM_GETROUTE, 0, { family: rtnl.AF_INET });

  // Create a listener for route changes
  let listener = rtnl.listener((msg) => {
      print('Received route message:', msg, '\n');
  }, [rtnl.RTM_NEWROUTE, rtnl.RTM_DELROUTE]);
  ```

Additionally, the rtnl module namespace may also be imported by invoking
the `ucode` interpreter with the `-lrtnl` switch.

### rtnl.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`rtnl`](#module_rtnl)  
**Example**  
```ucode
// Trigger rtnl error
request('invalid_command', {}, {});

// Print error (should yield error description)
print(error(), "\n");
```

### rtnl.request(cmd, flags, payload) ⇒ `Object` \| `Array.<Object>` \| `boolean`
Send a netlink request.

Sends a netlink request with the specified command, flags, and payload.

**Kind**: instance method of [`rtnl`](#module_rtnl)  
**Returns**: `Object` \| `Array.<Object>` \| `boolean` - - The response data, true for a
                                        successful acknowledgement without
                                        data, false when the kernel refuses
                                        the request or the reply cannot be
                                        received, or null for a dump
                                        without entries and when the
                                        request cannot be sent  

| Param | Type | Description |
| --- | --- | --- |
| cmd | `string` | The netlink command to send |
| flags | `number` | The netlink flags for the request |
| payload | `\*` | The payload data for the request |

**Example**  
```ucode
// Send a route request
let response = request('RTM_GETROUTE', 0, { family: AF_INET });
```

### rtnl.listener(callback, [commands], [groups]) ⇒ [`listener`](#module_rtnl.listener)
Create a netlink listener.

Creates a new netlink listener that will receive messages matching the specified
commands and multicast groups.

**Kind**: instance method of [`rtnl`](#module_rtnl)  
**Returns**: [`listener`](#module_rtnl.listener) - - A listener object with methods to control the listener  

| Param | Type | Description |
| --- | --- | --- |
| callback | `function` | The callback function to invoke when a message is received |
| [commands] | `Array.<string>` | Array of netlink commands to listen for (optional) |
| [groups] | `Array.<number>` | Array of multicast groups to join (optional) |

**Example**  
```ucode
// Create a listener for route changes
let routeListener = listener((msg) => {
    print('Received route message:', msg, '\n');
}, [RTM_NEWROUTE, RTM_DELROUTE]);
```

### rtnl.listener
**Kind**: static class of [`rtnl`](#module_rtnl)  
**See**: [listener()](#module_rtnl+listener)  

* [.listener](#module_rtnl.listener)
    * [.set_commands(commands)](#module_rtnl.listener+set_commands) ⇒ `boolean`
    * [.set_overrun_handler(handler)](#module_rtnl.listener+set_overrun_handler) ⇒ `boolean`
    * [.close()](#module_rtnl.listener+close) ⇒ `boolean`

#### listener.set\_commands(commands) ⇒ `boolean`
Set the commands for a netlink listener.

Updates the set of netlink commands that the listener will receive.

**Kind**: instance method of [`listener`](#module_rtnl.listener)  
**Returns**: `boolean` - - true if successful, false on error  

| Param | Type | Description |
| --- | --- | --- |
| commands | `Array.<string>` | Array of netlink commands to listen for |

**Example**  
```ucode
// Update listener to only receive route messages
listener.set_commands([RTM_NEWROUTE, RTM_DELROUTE]);
```

#### listener.set\_overrun\_handler(handler) ⇒ `boolean`
Set the overrun handler of a netlink listener.

The kernel drops event messages when the receive buffer of the event
socket is full. The module then enlarges the buffer and calls the
overrun handler of each listener without arguments.

Events of every joined group can be lost, including deletions. The
handler must dump each table that the script keeps state for. It must
treat every entry of the dump as new or changed, and every cached entry
that is missing from the dump as deleted.

**Kind**: instance method of [`listener`](#module_rtnl.listener)  
**Returns**: `boolean` - - true if successful, null if the listener is closed  

| Param | Type | Description |
| --- | --- | --- |
| handler | `function` | The function to call after an overrun, or `null` to remove it |

**Example**  
```ucode
// Rebuild the link cache after lost events
listener.set_overrun_handler(() => {
    let dump = request(RTM_GETLINK, NLM_F_DUMP, {});
    let seen = {};

    if (dump === false)
        return;

    for (let link in dump ?? []) {
        seen[link.ifname] = true;
        links[link.ifname] = link;
    }

    for (let name in keys(links))
        if (!seen[name])
            delete links[name];
});
```

#### listener.close() ⇒ `boolean`
Close a netlink listener.

Closes the netlink listener and stops receiving messages.

**Kind**: instance method of [`listener`](#module_rtnl.listener)  
**Returns**: `boolean` - - true if successful, false on error  
**Example**  
```ucode
// Close the listener
listener.close();
```

### rtnl~Netlink message flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NLM_F_ACK | `number` | Request for acknowledgment |
| NLM_F_ACK_TLVS | `number` | Request for acknowledgment with TLVs |
| NLM_F_APPEND | `number` | Append to existing list |
| NLM_F_ATOMIC | `number` | Atomic operation |
| NLM_F_CAPPED | `number` | Request capped |
| NLM_F_CREATE | `number` | Create if not exists |
| NLM_F_DUMP | `number` | Dump request |
| NLM_F_DUMP_FILTERED | `number` | Dump filtered request |
| NLM_F_DUMP_INTR | `number` | Dump interrupted |
| NLM_F_ECHO | `number` | Echo request |
| NLM_F_EXCL | `number` | Exclusive creation |
| NLM_F_MATCH | `number` | Match request |
| NLM_F_MULTI | `number` | Multi-part message |
| NLM_F_NONREC | `number` | Non-recursive operation |
| NLM_F_REPLACE | `number` | Replace existing |
| NLM_F_REQUEST | `number` | Request message |
| NLM_F_ROOT | `number` | Root operation |
| NLM_F_STRICT_CHK | `number` | Strict checking |

### rtnl~IPv6 address generation modes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IN6_ADDR_GEN_MODE_EUI64 | `number` | EUI-64 mode |
| IN6_ADDR_GEN_MODE_NONE | `number` | No mode |
| IN6_ADDR_GEN_MODE_STABLE_PRIVACY | `number` | Stable privacy mode |
| IN6_ADDR_GEN_MODE_RANDOM | `number` | Random mode |

### rtnl~MACVLAN modes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| MACVLAN_MODE_PRIVATE | `number` | Private mode |
| MACVLAN_MODE_VEPA | `number` | VEPA mode |
| MACVLAN_MODE_BRIDGE | `number` | Bridge mode |
| MACVLAN_MODE_PASSTHRU | `number` | Pass-through mode |
| MACVLAN_MODE_SOURCE | `number` | Source mode |

### rtnl~MACVLAN MAC address commands
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| MACVLAN_MACADDR_ADD | `number` | Add MAC address |
| MACVLAN_MACADDR_DEL | `number` | Delete MAC address |
| MACVLAN_MACADDR_FLUSH | `number` | Flush MAC addresses |
| MACVLAN_MACADDR_SET | `number` | Set MAC address |

### rtnl~MACsec validation levels
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| MACSEC_VALIDATE_DISABLED | `number` | Disabled validation |
| MACSEC_VALIDATE_CHECK | `number` | Check validation |
| MACSEC_VALIDATE_STRICT | `number` | Strict validation |
| MACSEC_VALIDATE_MAX | `number` | Maximum validation |

### rtnl~MACsec offload modes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| MACSEC_OFFLOAD_OFF | `number` | Offload off |
| MACSEC_OFFLOAD_PHY | `number` | Physical offload |
| MACSEC_OFFLOAD_MAC | `number` | MAC offload |
| MACSEC_OFFLOAD_MAX | `number` | Maximum offload |

### rtnl~IPVLAN modes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IPVLAN_MODE_L2 | `number` | Layer 2 mode |
| IPVLAN_MODE_L3 | `number` | Layer 3 mode |
| IPVLAN_MODE_L3S | `number` | Layer 3 symmetric mode |

### rtnl~VXLAN data frame flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| VXLAN_DF_UNSET | `number` | Data frame unset |
| VXLAN_DF_SET | `number` | Data frame set |
| VXLAN_DF_INHERIT | `number` | Data frame inherit |
| VXLAN_DF_MAX | `number` | Maximum data frame |

### rtnl~Geneve data frame flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| GENEVE_DF_UNSET | `number` | Data frame unset |
| GENEVE_DF_SET | `number` | Data frame set |
| GENEVE_DF_INHERIT | `number` | Data frame inherit |
| GENEVE_DF_MAX | `number` | Maximum data frame |

### rtnl~GTP roles
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| GTP_ROLE_GGSN | `number` | GGSN role |
| GTP_ROLE_SGSN | `number` | SGSN role |

### rtnl~Port request types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| PORT_REQUEST_PREASSOCIATE | `number` | Pre-associate request |
| PORT_REQUEST_PREASSOCIATE_RR | `number` | Pre-associate round-robin request |
| PORT_REQUEST_ASSOCIATE | `number` | Associate request |
| PORT_REQUEST_DISASSOCIATE | `number` | Disassociate request |

### rtnl~Port VDP responses
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| PORT_VDP_RESPONSE_SUCCESS | `number` | Success response |
| PORT_VDP_RESPONSE_INVALID_FORMAT | `number` | Invalid format response |
| PORT_VDP_RESPONSE_INSUFFICIENT_RESOURCES | `number` | Insufficient resources response |
| PORT_VDP_RESPONSE_UNUSED_VTID | `number` | Unused VTID response |
| PORT_VDP_RESPONSE_VTID_VIOLATION | `number` | VTID violation response |
| PORT_VDP_RESPONSE_VTID_VERSION_VIOALTION | `number` | VTID version violation response |
| PORT_VDP_RESPONSE_OUT_OF_SYNC | `number` | Out of sync response |

### rtnl~Port profile responses
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| PORT_PROFILE_RESPONSE_SUCCESS | `number` | Success response |
| PORT_PROFILE_RESPONSE_INPROGRESS | `number` | In progress response |
| PORT_PROFILE_RESPONSE_INVALID | `number` | Invalid response |
| PORT_PROFILE_RESPONSE_BADSTATE | `number` | Bad state response |
| PORT_PROFILE_RESPONSE_INSUFFICIENT_RESOURCES | `number` | Insufficient resources response |
| PORT_PROFILE_RESPONSE_ERROR | `number` | Error response |

### rtnl~IPoIB modes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IPOIB_MODE_DATAGRAM | `number` | Datagram mode |
| IPOIB_MODE_CONNECTED | `number` | Connected mode |

### rtnl~HSR protocols
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| HSR_PROTOCOL_HSR | `number` | HSR protocol |
| HSR_PROTOCOL_PRP | `number` | PRP protocol |

### rtnl~CAN controller modes
Flag bits used in the `mask` and `flags` members of the `ctrlmode`
attribute of `can` type links.

**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| CAN_CTRLMODE_LOOPBACK | `number` | Loopback mode |
| CAN_CTRLMODE_LISTENONLY | `number` | Listen-only mode |
| CAN_CTRLMODE_3_SAMPLES | `number` | Triple sampling mode |
| CAN_CTRLMODE_ONE_SHOT | `number` | One-shot mode |
| CAN_CTRLMODE_BERR_REPORTING | `number` | Bus error reporting |
| CAN_CTRLMODE_FD | `number` | CAN FD mode |
| CAN_CTRLMODE_PRESUME_ACK | `number` | Ignore missing CAN ACKs |
| CAN_CTRLMODE_FD_NON_ISO | `number` | CAN FD in non-ISO mode |
| CAN_CTRLMODE_CC_LEN8_DLC | `number` | Classic CAN DLC option |

### rtnl~CAN operational states
Values of the `state` attribute of `can` type links.

**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| CAN_STATE_ERROR_ACTIVE | `number` | RX/TX error count < 96 |
| CAN_STATE_ERROR_WARNING | `number` | RX/TX error count < 128 |
| CAN_STATE_ERROR_PASSIVE | `number` | RX/TX error count < 256 |
| CAN_STATE_BUS_OFF | `number` | RX/TX error count >= 256 |
| CAN_STATE_STOPPED | `number` | Device is stopped |
| CAN_STATE_SLEEPING | `number` | Device is sleeping |

### rtnl~Link extended statistics types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| LINK_XSTATS_TYPE_UNSPEC | `number` | Unspecified type |
| LINK_XSTATS_TYPE_BRIDGE | `number` | Bridge type |
| LINK_XSTATS_TYPE_BOND | `number` | Bond type |

### rtnl~XDP attach types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| XDP_ATTACHED_NONE | `number` | Not attached |
| XDP_ATTACHED_DRV | `number` | Driver attached |
| XDP_ATTACHED_SKB | `number` | SKB attached |
| XDP_ATTACHED_HW | `number` | Hardware attached |
| XDP_ATTACHED_MULTI | `number` | Multi attached |

### rtnl~FDB notification bits
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| FDB_NOTIFY_BIT | `number` | Notify bit |
| FDB_NOTIFY_INACTIVE_BIT | `number` | Inactive notify bit |

### rtnl~Route commands
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RTM_BASE | `number` | Base command |
| RTM_NEWLINK | `number` | New link |
| RTM_DELLINK | `number` | Delete link |
| RTM_GETLINK | `number` | Get link |
| RTM_SETLINK | `number` | Set link |
| RTM_NEWADDR | `number` | New address |
| RTM_DELADDR | `number` | Delete address |
| RTM_GETADDR | `number` | Get address |
| RTM_NEWROUTE | `number` | New route |
| RTM_DELROUTE | `number` | Delete route |
| RTM_GETROUTE | `number` | Get route |
| RTM_NEWRULE | `number` | New rule |
| RTM_DELRULE | `number` | Delete rule |
| RTM_GETRULE | `number` | Get rule |
| RTM_NEWQDISC | `number` | New queue discipline |
| RTM_DELQDISC | `number` | Delete queue discipline |
| RTM_GETQDISC | `number` | Get queue discipline |
| RTM_NEWTCLASS | `number` | New traffic class |
| RTM_DELTCLASS | `number` | Delete traffic class |
| RTM_GETTCLASS | `number` | Get traffic class |
| RTM_NEWTFILTER | `number` | New traffic filter |
| RTM_DELTFILTER | `number` | Delete traffic filter |
| RTM_GETTFILTER | `number` | Get traffic filter |
| RTM_NEWACTION | `number` | New action |
| RTM_DELACTION | `number` | Delete action |
| RTM_GETACTION | `number` | Get action |
| RTM_NEWPREFIX | `number` | New prefix |
| RTM_GETMULTICAST | `number` | Get multicast |
| RTM_GETANYCAST | `number` | Get anycast |
| RTM_NEWNEIGHTBL | `number` | New neighbor table |
| RTM_GETNEIGHTBL | `number` | Get neighbor table |
| RTM_SETNEIGHTBL | `number` | Set neighbor table |
| RTM_NEWNDUSEROPT | `number` | New neighbor user option |
| RTM_NEWADDRLABEL | `number` | New address label |
| RTM_DELADDRLABEL | `number` | Delete address label |
| RTM_GETADDRLABEL | `number` | Get address label |
| RTM_GETDCB | `number` | Get DCB |
| RTM_SETDCB | `number` | Set DCB |
| RTM_NEWNETCONF | `number` | New network configuration |
| RTM_DELNETCONF | `number` | Delete network configuration |
| RTM_GETNETCONF | `number` | Get network configuration |
| RTM_NEWMDB | `number` | New multicast database |
| RTM_DELMDB | `number` | Delete multicast database |
| RTM_GETMDB | `number` | Get multicast database |
| RTM_NEWNSID | `number` | New network namespace ID |
| RTM_DELNSID | `number` | Delete network namespace ID |
| RTM_GETNSID | `number` | Get network namespace ID |
| RTM_NEWSTATS | `number` | New statistics |
| RTM_GETSTATS | `number` | Get statistics |
| RTM_NEWCACHEREPORT | `number` | New cache report |
| RTM_NEWCHAIN | `number` | New chain |
| RTM_DELCHAIN | `number` | Delete chain |
| RTM_GETCHAIN | `number` | Get chain |
| RTM_NEWNEXTHOP | `number` | New next hop |
| RTM_DELNEXTHOP | `number` | Delete next hop |
| RTM_GETNEXTHOP | `number` | Get next hop |
| RTM_NEWLINKPROP | `number` | New link property |
| RTM_DELLINKPROP | `number` | Delete link property |
| RTM_GETLINKPROP | `number` | Get link property |
| RTM_NEWVLAN | `number` | New VLAN |
| RTM_DELVLAN | `number` | Delete VLAN |
| RTM_GETVLAN | `number` | Get VLAN |

### rtnl~Route types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RTN_UNSPEC | `number` | Unspecified route |
| RTN_UNICAST | `number` | Unicast route |
| RTN_LOCAL | `number` | Local route |
| RTN_BROADCAST | `number` | Broadcast route |
| RTN_ANYCAST | `number` | Anycast route |
| RTN_MULTICAST | `number` | Multicast route |
| RTN_BLACKHOLE | `number` | Blackhole route |
| RTN_UNREACHABLE | `number` | Unreachable route |
| RTN_PROHIBIT | `number` | Prohibited route |
| RTN_THROW | `number` | Throw route |
| RTN_NAT | `number` | NAT route |
| RTN_XRESOLVE | `number` | External resolve route |

### rtnl~Route scopes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RT_SCOPE_UNIVERSE | `number` | Universe scope |
| RT_SCOPE_SITE | `number` | Site scope |
| RT_SCOPE_LINK | `number` | Link scope |
| RT_SCOPE_HOST | `number` | Host scope |
| RT_SCOPE_NOWHERE | `number` | Nowhere scope |

### rtnl~Route tables
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RT_TABLE_UNSPEC | `number` | Unspecified table |
| RT_TABLE_COMPAT | `number` | Compatibility table |
| RT_TABLE_DEFAULT | `number` | Default table |
| RT_TABLE_MAIN | `number` | Main table |
| RT_TABLE_LOCAL | `number` | Local table |
| RT_TABLE_MAX | `number` | Maximum table |

### rtnl~Route metrics
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RTAX_MTU | `number` | Maximum transmission unit |
| RTAX_HOPLIMIT | `number` | Hop limit |
| RTAX_ADVMSS | `number` | Advertised MSS |
| RTAX_REORDERING | `number` | Reordering |
| RTAX_RTT | `number` | Round trip time |
| RTAX_WINDOW | `number` | Window size |
| RTAX_CWND | `number` | Congestion window |
| RTAX_INITCWND | `number` | Initial congestion window |
| RTAX_INITRWND | `number` | Initial receive window |
| RTAX_FEATURES | `number` | Features |
| RTAX_QUICKACK | `number` | Quick acknowledgment |
| RTAX_CC_ALGO | `number` | Congestion control algorithm |
| RTAX_RTTVAR | `number` | RTT variance |
| RTAX_SSTHRESH | `number` | Slow start threshold |
| RTAX_FASTOPEN_NO_COOKIE | `number` | Fast open no cookie |

### rtnl~Prefix types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| PREFIX_UNSPEC | `number` | Unspecified prefix |
| PREFIX_ADDRESS | `number` | Address prefix |
| PREFIX_CACHEINFO | `number` | Cache info prefix |

### rtnl~Neighbor discovery user option types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NDUSEROPT_UNSPEC | `number` | Unspecified option |
| NDUSEROPT_SRCADDR | `number` | Source address option |

### rtnl~Multicast groups
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RTNLGRP_NONE | `number` | No group |
| RTNLGRP_LINK | `number` | Link group |
| RTNLGRP_NOTIFY | `number` | Notify group |
| RTNLGRP_NEIGH | `number` | Neighbor group |
| RTNLGRP_TC | `number` | Traffic control group |
| RTNLGRP_IPV4_IFADDR | `number` | IPv4 interface address group |
| RTNLGRP_IPV4_MROUTE | `number` | IPv4 multicast route group |
| RTNLGRP_IPV4_ROUTE | `number` | IPv4 route group |
| RTNLGRP_IPV4_RULE | `number` | IPv4 rule group |
| RTNLGRP_IPV6_IFADDR | `number` | IPv6 interface address group |
| RTNLGRP_IPV6_MROUTE | `number` | IPv6 multicast route group |
| RTNLGRP_IPV6_ROUTE | `number` | IPv6 route group |
| RTNLGRP_IPV6_IFINFO | `number` | IPv6 interface info group |
| RTNLGRP_DECnet_IFADDR | `number` | DECnet interface address group |
| RTNLGRP_NOP2 | `number` | No operation 2 |
| RTNLGRP_DECnet_ROUTE | `number` | DECnet route group |
| RTNLGRP_DECnet_RULE | `number` | DECnet rule group |
| RTNLGRP_NOP4 | `number` | No operation 4 |
| RTNLGRP_IPV6_PREFIX | `number` | IPv6 prefix group |
| RTNLGRP_IPV6_RULE | `number` | IPv6 rule group |
| RTNLGRP_ND_USEROPT | `number` | Neighbor discovery user option group |
| RTNLGRP_PHONET_IFADDR | `number` | Phonet interface address group |
| RTNLGRP_PHONET_ROUTE | `number` | Phonet route group |
| RTNLGRP_DCB | `number` | Data Center Bridging group |
| RTNLGRP_IPV4_NETCONF | `number` | IPv4 network configuration group |
| RTNLGRP_IPV6_NETCONF | `number` | IPv6 network configuration group |
| RTNLGRP_MDB | `number` | Multicast database group |
| RTNLGRP_MPLS_ROUTE | `number` | MPLS route group |
| RTNLGRP_NSID | `number` | Network namespace ID group |
| RTNLGRP_MPLS_NETCONF | `number` | MPLS network configuration group |
| RTNLGRP_IPV4_MROUTE_R | `number` | IPv4 multicast route reverse group |
| RTNLGRP_IPV6_MROUTE_R | `number` | IPv6 multicast route reverse group |
| RTNLGRP_NEXTHOP | `number` | Next hop group |
| RTNLGRP_BRVLAN | `number` | Bridge VLAN group |

### rtnl~Route flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| RTM_F_CLONED | `number` | Cloned route |
| RTM_F_EQUALIZE | `number` | Equalize route |
| RTM_F_FIB_MATCH | `number` | FIB match |
| RTM_F_LOOKUP_TABLE | `number` | Lookup table |
| RTM_F_NOTIFY | `number` | Notify |
| RTM_F_PREFIX | `number` | Prefix |

### rtnl~Address families
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| AF_UNSPEC | `number` | Unspecified address family |
| AF_INET | `number` | IPv4 address family |
| AF_INET6 | `number` | IPv6 address family |
| AF_MPLS | `number` | MPLS address family |
| AF_BRIDGE | `number` | Bridge address family |

### rtnl~Generic Routing Encapsulation flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| GRE_CSUM | `number` | Checksum flag |
| GRE_ROUTING | `number` | Routing flag |
| GRE_KEY | `number` | Key flag |
| GRE_SEQ | `number` | Sequence flag |
| GRE_STRICT | `number` | Strict flag |
| GRE_REC | `number` | Record flag |
| GRE_ACK | `number` | Acknowledgment flag |

### rtnl~Tunnel encapsulation types
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| TUNNEL_ENCAP_NONE | `number` | No encapsulation |
| TUNNEL_ENCAP_FOU | `number` | Foo over UDP |
| TUNNEL_ENCAP_GUE | `number` | Generic UDP Encapsulation |
| TUNNEL_ENCAP_MPLS | `number` | MPLS encapsulation |

### rtnl~Tunnel encapsulation flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| TUNNEL_ENCAP_FLAG_CSUM | `number` | Checksum flag |
| TUNNEL_ENCAP_FLAG_CSUM6 | `number` | IPv6 checksum flag |
| TUNNEL_ENCAP_FLAG_REMCSUM | `number` | Remote checksum flag |

### rtnl~IPv6 tunnel flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IP6_TNL_F_ALLOW_LOCAL_REMOTE | `number` | Allow local remote |
| IP6_TNL_F_IGN_ENCAP_LIMIT | `number` | Ignore encapsulation limit |
| IP6_TNL_F_MIP6_DEV | `number` | Mobile IPv6 device |
| IP6_TNL_F_RCV_DSCP_COPY | `number` | Receive DSCP copy |
| IP6_TNL_F_USE_ORIG_FLOWLABEL | `number` | Use original flow label |
| IP6_TNL_F_USE_ORIG_FWMARK | `number` | Use original firewall mark |
| IP6_TNL_F_USE_ORIG_TCLASS | `number` | Use original traffic class |

### rtnl~Interface flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NTF_EXT_LEARNED | `number` | Externally learned |
| NTF_MASTER | `number` | Master interface |
| NTF_OFFLOADED | `number` | Offloaded |
| NTF_PROXY | `number` | Proxy |
| NTF_ROUTER | `number` | Router |
| NTF_SELF | `number` | Self |
| NTF_STICKY | `number` | Sticky |
| NTF_USE | `number` | Use |

### rtnl~Neighbor states
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NUD_DELAY | `number` | Delay state |
| NUD_FAILED | `number` | Failed state |
| NUD_INCOMPLETE | `number` | Incomplete state |
| NUD_NOARP | `number` | No ARP |
| NUD_NONE | `number` | No state |
| NUD_PERMANENT | `number` | Permanent state |
| NUD_PROBE | `number` | Probe state |
| NUD_REACHABLE | `number` | Reachable state |
| NUD_STALE | `number` | Stale state |

### rtnl~Address flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IFA_F_DADFAILED | `number` | DAD failed |
| IFA_F_DEPRECATED | `number` | Deprecated |
| IFA_F_HOMEADDRESS | `number` | Home address |
| IFA_F_MANAGETEMPADDR | `number` | Manage temporary address |
| IFA_F_MCAUTOJOIN | `number` | Multicast auto join |
| IFA_F_NODAD | `number` | No DAD |
| IFA_F_NOPREFIXROUTE | `number` | No prefix route |
| IFA_F_OPTIMISTIC | `number` | Optimistic |
| IFA_F_PERMANENT | `number` | Permanent |
| IFA_F_SECONDARY | `number` | Secondary |
| IFA_F_STABLE_PRIVACY | `number` | Stable privacy |
| IFA_F_TEMPORARY | `number` | Temporary |
| IFA_F_TENTATIVE | `number` | Tentative |

### rtnl~FIB rule flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| FIB_RULE_PERMANENT | `number` | Permanent rule |
| FIB_RULE_INVERT | `number` | Invert rule |
| FIB_RULE_UNRESOLVED | `number` | Unresolved rule |
| FIB_RULE_IIF_DETACHED | `number` | Interface detached |
| FIB_RULE_DEV_DETACHED | `number` | Device detached |
| FIB_RULE_OIF_DETACHED | `number` | Output interface detached |

### rtnl~FIB rule actions
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| FR_ACT_TO_TBL | `number` | To table action |
| FR_ACT_GOTO | `number` | Goto action |
| FR_ACT_NOP | `number` | No operation action |
| FR_ACT_BLACKHOLE | `number` | Blackhole action |
| FR_ACT_UNREACHABLE | `number` | Unreachable action |
| FR_ACT_PROHIBIT | `number` | Prohibit action |

### rtnl~Network configuration indices
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| NETCONFA_IFINDEX_ALL | `number` | All interfaces |
| NETCONFA_IFINDEX_DEFAULT | `number` | Default interface |

### rtnl~Bridge flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| BRIDGE_FLAGS_MASTER | `number` | Master flag |
| BRIDGE_FLAGS_SELF | `number` | Self flag |

### rtnl~Bridge modes
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| BRIDGE_MODE_VEB | `number` | Virtual Ethernet Bridge mode |
| BRIDGE_MODE_VEPA | `number` | Virtual Ethernet Port Aggregator mode |
| BRIDGE_MODE_UNDEF | `number` | Undefined mode |
| BRIDGE_MODE_UNSPEC | `number` | Unspecified mode |
| BRIDGE_MODE_HAIRPIN | `number` | Hairpin mode |

### rtnl~Bridge VLAN information flags
**Kind**: inner typedef of [`rtnl`](#module_rtnl)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| BRIDGE_VLAN_INFO_MASTER | `number` | Master VLAN info |
| BRIDGE_VLAN_INFO_PVID | `number` | Primary VLAN ID |
| BRIDGE_VLAN_INFO_UNTAGGED | `number` | Untagged VLAN |
| BRIDGE_VLAN_INFO_RANGE_BEGIN | `number` | Range begin |
| BRIDGE_VLAN_INFO_RANGE_END | `number` | Range end |
| BRIDGE_VLAN_INFO_BRENTRY | `number` | Bridge entry |

---

# ucode module: serial

> **Live docs:** https://ucode.mein.io/module-serial.html

---

## Serial Port Access

The `serial` module provides raw access to the termios terminal API and
the serial port modem control lines.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { attr, B115200 } from 'serial';

  let fd = io.open('/dev/ttyS0', io.O_RDWR);
  print(attr(fd));
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as serial from 'serial';

  let fd = io.open('/dev/ttyS0', io.O_RDWR);
  print(serial.attr(fd));
  ```

Additionally, the serial module namespace may also be imported by invoking
the `ucode` interpreter with the `-lserial` switch.

### serial.error() ⇒ `string`
Query error information.

Returns a string containing a description of the last occurred error or
`null` if there is no error information.

**Kind**: instance method of [`serial`](#module_serial)  

### serial.isatty(fd) ⇒ `boolean`
Check whether the file descriptor refers to a terminal.

**Kind**: instance method of [`serial`](#module_serial)  
**Returns**: `boolean` - Returns `true` if the file descriptor refers to a terminal device,
`false` otherwise, or `null` if an error occurred.  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.attr(fd) ⇒ `object`
Get terminal attributes.

Retrieves the current termios attributes for the file descriptor.

Returns an object containing the `iflag`, `oflag`, `cflag` and `lflag`
flag values, the `ispeed` and `ospeed` baud rates, and a `cc` array of
control character settings.

Returns `null` if an error occurred or if the descriptor is not a terminal.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.setattr(fd, attrs, [when]) ⇒ `boolean`
Set terminal attributes.

Updates the termios attributes for the file descriptor. The given object
may contain any of the following properties:

 - `iflag`: input flags
 - `oflag`: output flags
 - `cflag`: control flags
 - `lflag`: local flags
 - `ispeed`: input baud rate
 - `ospeed`: output baud rate
 - `cc`: array of control character settings

Only the provided properties are modified, all other attributes are left
unchanged.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `object` |  | The file descriptor, or an object with a `fileno()` method. |
| attrs | `object` |  | The terminal attributes to set. |
| [when] | `number` | `0` | When to apply the changes (`TCSANOW`, `TCSADRAIN` or `TCSAFLUSH`). |

### serial.setspeed(fd, speed, [when]) ⇒ `boolean`
Set the terminal baud rate.

Sets both the input and output baud rate of the file descriptor to the
given speed.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `object` |  | The file descriptor, or an object with a `fileno()` method. |
| speed | `number` |  | The baud rate to set, e.g. `B115200`. |
| [when] | `number` | `0` | When to apply the changes (`TCSANOW`, `TCSADRAIN` or `TCSAFLUSH`). |

### serial.setraw(fd, [when]) ⇒ `boolean`
Put the terminal into raw mode.

Disables input and output processing, canonical mode, signal generation
and echo, following the behaviour of `cfmakeraw()`.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `object` |  | The file descriptor, or an object with a `fileno()` method. |
| [when] | `number` | `0` | When to apply the changes (`TCSANOW`, `TCSADRAIN` or `TCSAFLUSH`). |

### serial.setblocking(fd, vmin, vtime, [when]) ⇒ `boolean`
Configure the terminal read blocking behaviour.

Sets the `VMIN` and `VTIME` control character settings which determine
how reads from the terminal block:

 - `vmin = 0`, `vtime = 0`: non-blocking reads
 - `vmin = 0`, `vtime > 0`: reads time out after `vtime` tenths of a second
 - `vmin > 0`, `vtime = 0`: reads block until at least `vmin` bytes arrive
 - `vmin > 0`, `vtime > 0`: reads block until `vmin` bytes arrive or the
   inter-byte `vtime` timeout expires

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `object` |  | The file descriptor, or an object with a `fileno()` method. |
| vmin | `number` |  | Minimum number of bytes to read before a read operation returns. |
| vtime | `number` |  | Read timeout in tenths of a second. |
| [when] | `number` | `0` | When to apply the changes (`TCSANOW`, `TCSADRAIN` or `TCSAFLUSH`). |

### serial.mget(fd) ⇒ `number`
Get the serial port modem control line status.

Returns a bitmask of the current modem control line states, using the
`TIOCM_*` constants to test individual lines.

Returns `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.mset(fd, bits) ⇒ `boolean`
Set the serial port modem control line states.

Replaces the full set of modem control line states with the given bitmask.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| bits | `number` | The modem control line states to set, as a bitmask of `TIOCM_*` constants. |

### serial.mbis(fd, bits) ⇒ `boolean`
Set individual serial port modem control lines.

Sets the modem control lines selected by the given bitmask, leaving all
other lines unchanged.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| bits | `number` | The modem control lines to set, as a bitmask of `TIOCM_*` constants. |

### serial.mbic(fd, bits) ⇒ `boolean`
Clear individual serial port modem control lines.

Clears the modem control lines selected by the given bitmask, leaving all
other lines unchanged.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| bits | `number` | The modem control lines to clear, as a bitmask of `TIOCM_*` constants. |

### serial.dtr(fd, on) ⇒ `boolean`
Assert or deassert the DTR (Data Terminal Ready) modem control line.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| on | `boolean` | Whether to assert (`true`) or deassert (`false`) the line. |

### serial.rts(fd, on) ⇒ `boolean`
Assert or deassert the RTS (Request To Send) modem control line.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| on | `boolean` | Whether to assert (`true`) or deassert (`false`) the line. |

### serial.sendbreak(fd, [duration]) ⇒ `boolean`
Send a break signal on the serial line.

If the terminal is in canonical mode, the break is sent after the current
input line has been processed, otherwise it is sent immediately.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `object` |  | The file descriptor, or an object with a `fileno()` method. |
| [duration] | `number` | `0` | The break duration in seconds, or `0` to send a standard length break. |

### serial.drain(fd) ⇒ `boolean`
Wait for pending output to be written.

Blocks until all output written to the file descriptor has been
transmitted.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.flush(fd, [queue]) ⇒ `boolean`
Flush the terminal input and/or output queues.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| fd | `number` \| `object` |  | The file descriptor, or an object with a `fileno()` method. |
| [queue] | `number` | `TCIOFLUSH` | The queue(s) to flush: `TCIFLUSH` for input, `TCOFLUSH` for output, or `TCIOFLUSH` for both. |

### serial.input\_waiting(fd) ⇒ `number`
Get the number of bytes waiting in the input queue.

Returns the number of bytes available for reading without blocking, or
`null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.output\_waiting(fd) ⇒ `number`
Get the number of bytes waiting in the output queue.

Returns the number of bytes pending transmission, or `null` if an error
occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.getinfo(fd) ⇒ `object`
Get the serial port configuration.

Retrieves the serial port specific configuration (setserial style) for
the file descriptor.

Returns an object containing the `type`, `line`, `port`, `irq`, `flags`,
`xmit_fifo_size`, `custom_divisor`, `baud_base`, `close_delay`,
`closing_wait`, `hub6`, `io_type`, `port_high` and `iomem_reg_shift`
properties, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |

### serial.setinfo(fd, opts) ⇒ `boolean`
Set the serial port configuration.

Updates the serial port specific configuration (setserial style) for the
file descriptor. The given object may contain any of the following
properties:

 - `type`: port type
 - `port`: I/O port address
 - `irq`: interrupt line
 - `flags`: port flags
 - `xmit_fifo_size`: transmit FIFO size
 - `custom_divisor`: custom baud rate divisor
 - `baud_base`: base clock frequency
 - `close_delay`: delay before closing the port
 - `closing_wait`: wait time when closing the port
 - `hub6`: HUB6 port selection
 - `port_high`: high I/O port address
 - `iomem_reg_shift`: I/O memory register shift

Only the provided properties are modified, all other settings are left
unchanged.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| opts | `object` | The serial port configuration options to set. |

### serial.lowlatency(fd, on) ⇒ `boolean`
Enable or disable the low latency mode.

Toggles the `ASYNC_LOW_LATENCY` flag in the serial port configuration,
which reduces the latency of the serial port at the cost of increased
CPU usage.

Returns `true` on success, or `null` if an error occurred.

**Kind**: instance method of [`serial`](#module_serial)  

| Param | Type | Description |
| --- | --- | --- |
| fd | `number` \| `object` | The file descriptor, or an object with a `fileno()` method. |
| on | `boolean` | Whether to enable (`true`) or disable (`false`) the low latency mode. |

### serial~Apply Modes
The `TCS*` constants are used as the optional *when* argument of
[setattr()](#module_serial+setattr),
[setspeed()](#module_serial+setspeed),
[setraw()](#module_serial+setraw) and
[setblocking()](#module_serial+setblocking) to control when the
attribute changes take effect.

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| TCSANOW | `number` | Apply the changes immediately. |
| TCSADRAIN | `number` | Apply the changes after all pending output has been transmitted (default). |
| TCSAFLUSH | `number` | Apply the changes after all pending output has been transmitted, discarding any unread input. |

### serial~Flush Queues
The `TC*FLUSH` constants are used as the optional *queue* argument of
[flush()](#module_serial+flush) to select the queue(s) to flush.

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| TCIFLUSH | `number` | Flush data received but not read. |
| TCOFLUSH | `number` | Flush data written but not yet transmitted. |
| TCIOFLUSH | `number` | Flush both received and written data (default). |

### serial~Control Flags
The `cflag` constants select the control mode of the port and are used
with the `cflag` property of [setattr()](#module_serial+setattr).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| CSIZE | `number` | Mask for the character size bits. |
| CS5 | `number` | Use 5 data bits per character. |
| CS6 | `number` | Use 6 data bits per character. |
| CS7 | `number` | Use 7 data bits per character. |
| CS8 | `number` | Use 8 data bits per character. |
| CSTOPB | `number` | Use two stop bits (one if clear). |
| CREAD | `number` | Enable the receiver. |
| PARENB | `number` | Enable parity generation and detection. |
| PARODD | `number` | Use odd parity (even if clear). |
| HUPCL | `number` | Hang up (drop the carrier) when the last file descriptor is closed. |
| CLOCAL | `number` | Ignore the modem status lines. |
| CRTSCTS | `number` | Enable in-band (hardware) flow control. |
| CMSPAR | `number` | Use "stick" (space/mark) parity. |
| CBAUD | `number` | Mask for the baud rate bits. |
| CBAUDEX | `number` | Extended baud rate bits. |

### serial~Input Flags
The `iflag` constants control input processing and are used with the
`iflag` property of [setattr()](#module_serial+setattr).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IGNBRK | `number` | Ignore the break condition. |
| BRKINT | `number` | If IGNBRK is not set, a break causes an interrupt signal. |
| IGNPAR | `number` | Ignore characters with parity errors. |
| PARMRK | `number` | Mark parity errors with a three-byte sequence. |
| INPCK | `number` | Enable input parity checking. |
| ISTRIP | `number` | Strip the eighth bit of input characters. |
| INLCR | `number` | Map NL to CR on input. |
| IGNCR | `number` | Ignore CR on input. |
| ICRNL | `number` | Map CR to NL on input. |
| IUCLC | `number` | Map uppercase to lowercase on input. |
| IXON | `number` | Enable XON/XOFF flow control output. |
| IXANY | `number` | Allow any character to restart output. |
| IXOFF | `number` | Enable XON/XOFF flow control input. |
| IMAXBEL | `number` | Ring the bell when the input queue is full. |
| IUTF8 | `number` | Input characters are UTF-8 encoded. |

### serial~Output Flags
The `oflag` constants control output processing and are used with the
`oflag` property of [setattr()](#module_serial+setattr).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| OPOST | `number` | Enable implementation-defined output processing. |
| OLCUC | `number` | Map lowercase to uppercase on output. |
| ONLCR | `number` | Map NL to CR-NL on output. |
| OCRNL | `number` | Map CR to NL on output. |
| ONOCR | `number` | Translate CR to NUL in the first column. |
| ONLRET | `number` | Do not transmit CR. |
| OFILL | `number` | Use fill characters for timing. |
| OFDEL | `number` | Use DEL characters for fill (NUL if clear). |

### serial~Local Flags
The `lflag` constants control local (non-modem) behaviour and are used
with the `lflag` property of [setattr()](#module_serial+setattr).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| ISIG | `number` | Enable signal generation (INTR, QUIT, SUSP). |
| ICANON | `number` | Enable canonical mode (line-buffered input). |
| ECHO | `number` | Enable echoing of input characters. |
| ECHOE | `number` | Erase the last character on ERASE. |
| ECHOK | `number` | Ring the bell on the kill character. |
| ECHONL | `number` | Echo NL even if ECHO is not set. |
| ECHOCTL | `number` | Echo control characters in hat notation. |
| ECHOKE | `number` | Erase a killed line. |
| NOFLSH | `number` | Disable flushing on signal. |
| TOSTOP | `number` | Generate SIGTTOU for background writes. |
| IEXTEN | `number` | Enable implementation-defined input extensions. |

### serial~Control Character Indices
The `V*` constants are indices into the `cc` array returned by
[attr()](#module_serial+attr) and accepted by
[setattr()](#module_serial+setattr). `NCCS` is the number of
control characters in the array.

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| VINTR | `number` | Interrupt character (sends SIGINT). |
| VQUIT | `number` | Quit character (sends SIGQUIT). |
| VERASE | `number` | Erase character (erases the last character). |
| VKILL | `number` | Kill character (erases the current line). |
| VEOF | `number` | End-of-file character. |
| VTIME | `number` | Read timeout in tenths of a second. |
| VMIN | `number` | Minimum number of bytes for a read. |
| VSWTC | `number` | Switch character (XON/XOFF switching). |
| VSTART | `number` | Restart character (XON). |
| VSTOP | `number` | Stop character (XOFF). |
| VSUSP | `number` | Suspend character (sends SIGTSTP). |
| VEOL | `number` | End-of-line character (first). |
| VREPRINT | `number` | Reprint character (reprints the line). |
| VDISCARD | `number` | Discard mode toggle character. |
| VWERASE | `number` | Word-erase character. |
| VLNEXT | `number` | Literal next character (disables special characters). |
| VEOL2 | `number` | End-of-line character (second). |
| NCCS | `number` | Number of control characters. |

### serial~Baud Rates
The `B*` constants select the port baud rate and are used with the
`ispeed`/`ospeed` properties of [setattr()](#module_serial+setattr)
or as the *speed* argument of
[setspeed()](#module_serial+setspeed).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| B0 | `number` | Hang up (no carrier). |
| B50 | `number` | 50 baud. |
| B75 | `number` | 75 baud. |
| B110 | `number` | 110 baud. |
| B134 | `number` | 134.5 baud. |
| B150 | `number` | 150 baud. |
| B200 | `number` | 200 baud. |
| B300 | `number` | 300 baud. |
| B600 | `number` | 600 baud. |
| B1200 | `number` | 1200 baud. |
| B1800 | `number` | 1800 baud. |
| B2400 | `number` | 2400 baud. |
| B4800 | `number` | 4800 baud. |
| B9600 | `number` | 9600 baud. |
| B19200 | `number` | 19200 baud. |
| B38400 | `number` | 38400 baud. |
| B57600 | `number` | 57600 baud. |
| B115200 | `number` | 115200 baud. |
| B230400 | `number` | 230400 baud. |
| B460800 | `number` | 460800 baud. |
| B500000 | `number` | 500000 baud. |
| B576000 | `number` | 576000 baud. |
| B921600 | `number` | 921600 baud. |
| B1000000 | `number` | 1000000 baud. |
| B1152000 | `number` | 1152000 baud. |
| B1500000 | `number` | 1500000 baud. |
| B2000000 | `number` | 2000000 baud. |
| B2500000 | `number` | 2500000 baud. |
| B3000000 | `number` | 3000000 baud. |
| B3500000 | `number` | 3500000 baud. |
| B4000000 | `number` | 4000000 baud. |

### serial~Modem Control Line Bits
The `TIOCM_*` constants identify the serial port modem control lines
and are used with [mget()](#module_serial+mget),
[mset()](#module_serial+mset),
[mbis()](#module_serial+mbis) and
[mbic()](#module_serial+mbic).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| TIOCM_LE | `number` | Loopback output. |
| TIOCM_DTR | `number` | Data Terminal Ready. |
| TIOCM_RTS | `number` | Request To Send. |
| TIOCM_ST | `number` | Secondary transmit (TX2). |
| TIOCM_SR | `number` | Secondary receive (RX2). |
| TIOCM_CTS | `number` | Clear To Send. |
| TIOCM_CAR | `number` | Carrier Detect. |
| TIOCM_CD | `number` | Carrier Detect (alias). |
| TIOCM_RNG | `number` | Ring Indicator. |
| TIOCM_RI | `number` | Ring Indicator (alias). |
| TIOCM_DSR | `number` | Data Set Ready. |

### serial~Serial Port Flags
The `ASYNC_*` constants are flags of the `flags` property returned by
[getinfo()](#module_serial+getinfo) and accepted by
[setinfo()](#module_serial+setinfo).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| ASYNC_HUP_NOTIFY | `number` | Send SIGHUP when the port is closed. |
| ASYNC_FOURPORT | `number` | Enable four-port mode. |
| ASYNC_SAK | `number` | Enable special "SAK" character handling. |
| ASYNC_SPD_HI | `number` | High speed serial support (> 115200). |
| ASYNC_SPD_VHI | `number` | Very high speed serial support (> 230400). |
| ASYNC_SPD_SHI | `number` | Shigh speed serial support (1.5-3 Mbit). |
| ASYNC_SPD_CUST | `number` | Custom divisor baud rate. |
| ASYNC_SPD_WARP | `number` | Warp speed serial (bit-banged). |
| ASYNC_SPD_MASK | `number` | Mask for the speed selection bits. |
| ASYNC_SKIP_TEST | `number` | Skip the UART presence test. |
| ASYNC_AUTO_IRQ | `number` | Auto-detect the IRQ line. |
| ASYNC_CALLOUT_NOHUP | `number` | Do not send SIGHUP on close. |
| ASYNC_LOW_LATENCY | `number` | Enable low latency mode. |
| ASYNC_BUGGY_UART | `number` | Workaround for buggy UARTs. |
| ASYNC_CLOSING_WAIT_INF | `number` | Infinite closing wait. |
| ASYNC_CLOSING_WAIT_NONE | `number` | No closing wait. |

### serial~Serial Port Types
The `PORT_*` constants identify the serial port type of the `type`
property returned by [getinfo()](#module_serial+getinfo) and
accepted by [setinfo()](#module_serial+setinfo).

**Kind**: inner typedef of [`serial`](#module_serial)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| PORT_UNKNOWN | `number` | Unknown port type. |
| PORT_8250 | `number` | Generic 8250 UART. |
| PORT_16450 | `number` | 16450 UART. |
| PORT_16550 | `number` | 16550 UART. |
| PORT_16550A | `number` | 16550A UART. |
| PORT_16650 | `number` | 16650 UART. |
| PORT_16650V2 | `number` | 16650V2 UART. |
| PORT_16750 | `number` | 16750 UART. |

---

# ucode module: socket

> **Live docs:** https://ucode.mein.io/module-socket.html

---

## Socket Module

The `socket` module provides functions for interacting with sockets.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```text
  import { AF_INET, SOCK_STREAM, create as socket } from 'socket';

  let sock = socket(AF_INET, SOCK_STREAM, 0);
  sock.connect('192.168.1.1', 80);
  sock.send(…);
  sock.recv(…);
  sock.close();
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```text
  import * as socket from 'socket';

  let sock = socket.create(socket.AF_INET, socket.SOCK_STREAM, 0);
  sock.connect('192.168.1.1', 80);
  sock.send(…);
  sock.recv(…);
  sock.close();
  ```

Additionally, the socket module namespace may also be imported by invoking
the `ucode` interpreter with the `-lsocket` switch.

### socket.error([numeric]) ⇒ `string` \| `number`
Query error information.

Returns a string containing a description of the last occurred error when
the *numeric* argument is absent or false.

Returns a positive (`errno`) or negative (`EAI_*` constant) error code number
when the *numeric* argument is `true`.

Returns `null` if there is no error information.

**Kind**: instance method of [`socket`](#module_socket)  

| Param | Type | Description |
| --- | --- | --- |
| [numeric] | `boolean` | Whether to return a numeric error code (`true`) or a human readable error message (false). |

**Example**  
```ucode
// Trigger socket error by attempting to bind IPv6 address with IPv4 socket
socket.create(socket.AF_INET, socket.SOCK_STREAM, 0).bind("::", 8080);

// Print error (should yield "Address family not supported by protocol")
print(socket.error(), "\n");

// Trigger resolve error
socket.addrinfo("doesnotexist.org");

// Query error code (should yield -2 for EAI_NONAME)
print(socket.error(true), "\n");  //
```

### socket.strerror(code) ⇒ `string`
Returns a string containing a description of the positive (`errno`) or
negative (`EAI_*` constant) error code number given by the *code* argument.

Returns `null` if the error code number is unknown.

**Kind**: instance method of [`socket`](#module_socket)  

| Param | Type | Description |
| --- | --- | --- |
| code | `number` | The error code. |

**Example**  
```ucode
// Should output 'Name or service not known'.
print(socket.strerror(-2), '\n');

// Should output 'No route to host'.
print(socket.strerror(113), '\n');
```

### socket.sockaddr(address) ⇒ [`SocketAddress`](#module_socket.socket.SocketAddress)
Parses the provided address value into a socket address representation.

This function parses the given address value into a socket address
representation required for a number of socket operations. The address value
can be provided in various formats:
- For IPv4 addresses, it can be a string representing the IP address,
  optionally followed by a port number separated by colon, e.g.
  `192.168.0.1:8080`.
- For IPv6 addresses, it must be an address string enclosed in square
  brackets if a port number is specified, otherwise the brackets are
  optional. The address string may also include a scope ID in the form
  `%ifname` or `%number`, e.g. `[fe80::1%eth0]:8080` or `fe80::1%15`.
- Any string value containing a slash is treated as UNIX domain socket path.
- Alternatively, it can be provided as an array returned by
  [iptoarr()](module:core#iptoarr), representing the address octets.
- It can also be an object representing a network address, with properties
  for `address` (the IP address) and `port` or a single property `path` to
  denote a UNIX domain socket address.

**Kind**: instance method of [`socket`](#module_socket)  
**Returns**: [`SocketAddress`](#module_socket.socket.SocketAddress) - A socket address representation of the provided address value, or `null` if
the address could not be parsed.  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| `Array.<number>` \| [`SocketAddress`](#module_socket.socket.SocketAddress) | The address value to parse. |

**Example**  
```ucode
// Parse an IP address string with port
const address1 = sockaddr('192.168.0.1:8080');

// Parse an IPv6 address string with port and scope identifier
const address2 = sockaddr('[fe80::1%eth0]:8080');

// Parse an array representing an IP address
const address3 = sockaddr([192, 168, 0, 1]);

// Parse a network address object
const address4 = sockaddr({ address: '192.168.0.1', port: 8080 });

// Convert a path value to a UNIX domain socket address
const address5 = sockaddr('/var/run/daemon.sock');
```

### socket.nameinfo(address, [flags]) ⇒ `Object`
Resolves the given network address into hostname and service name.

The `nameinfo()` function provides an API for reverse DNS lookup and service
name resolution. It returns an object containing the following properties:
- `hostname`: The resolved hostname.
- `service`: The resolved service name.

Returns an object representing the resolved hostname and service name.
Return `null` if an error occurred during resolution.

**Kind**: instance method of [`socket`](#module_socket)  
**See**

- {@link module:socket~"Socket Types"|Socket Types}
- {@link module:socket~"Name Info Constants"|AName Info Constants}

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| [`SocketAddress`](#module_socket.socket.SocketAddress) | The network address to resolve. It can be specified as: - A string representing the IP address. - An object representing the address with properties `address` and `port`. |
| [flags] | `number` | Optional flags that provide additional control over the resolution process, specified as bitwise OR-ed number of `NI_*` constants. |

**Example**  
```ucode
// Resolve a network address into hostname and service name
const result = network.getnameinfo('192.168.1.1:80');
print(result); // { "hostname": "example.com", "service": "http" }
```

### socket.addrinfo(hostname, [service], [hints]) ⇒ [`Array.<AddressInfo>`](#module_socket.AddressInfo)
Resolves the given hostname and optional service name into a list of network
addresses, according to the provided hints.

The `addrinfo()` function provides an API for performing DNS and service name
resolution. It returns an array of objects, each representing a resolved
address.

Returns an array of resolved addresses.
Returns `null` if an error occurred during resolution.

**Kind**: instance method of [`socket`](#module_socket)  
**See**

- {@link module:socket~"Socket Types"|Socket Types}
- {@link module:socket~"Address Info Flags"|Address Info Flags}

| Param | Type | Description |
| --- | --- | --- |
| hostname | `string` | The hostname to resolve. |
| [service] | `string` | Optional service name to resolve. If not provided, the service field of the resulting address information structures is left uninitialized. |
| [hints] | `Object` | Optional hints object that provides additional control over the resolution process. It can contain the following properties: - `family`: The preferred address family (`AF_INET` or `AF_INET6`). - `socktype`: The socket type (`SOCK_STREAM`, `SOCK_DGRAM`, etc.). - `protocol`: The protocol of returned addresses. - `flags`: Bitwise OR-ed `AI_*` flags to control the resolution behavior. |

**Example**  
```ucode
// Resolve all addresses
const addresses = socket.addrinfo('example.org');

// Resolve IPv4 addresses for a given hostname and service
const ipv4addresses = socket.addrinfo('example.com', 'http', { family: socket.AF_INET });

// Resolve IPv6 addresses without specifying a service
const ipv6Addresses = socket.addrinfo('example.com', null, { family: socket.AF_INET6 });
```

### socket.poll(timeout, ...sockets) ⇒ [`Array.<PollSpec>`](#module_socket.PollSpec)
Polls a number of sockets for state changes.

Returns an array of `[socket, flags]` tuples for each socket with pending
events. When a tuple is passed as socket argument, it is included as-is into
the result tuple array, with the flags entry changed to a bitwise OR-ed value
describing the pending events for this socket. When a plain socket instance
(or another kind of handle) is passed, a new tuple array is created for this
socket within the result tuple array, containing this socket as first and the
bitwise OR-ed pending events as second element.

Returns `null` if an error occurred.

**Kind**: instance method of [`socket`](#module_socket)  

| Param | Type | Description |
| --- | --- | --- |
| timeout | `number` | Amount of milliseconds to wait for socket activity before aborting the poll call. If set to `0`, the poll call will return immediately if none of the provided sockets has pending events, if set to a negative value, the poll call will wait indefinitely, in all other cases the poll call will wait at most for the given amount of milliseconds before returning. |
| ...sockets | [`socket`](#module_socket.socket) \| [`PollSpec`](#module_socket.PollSpec) | An arbitrary amount of socket arguments. Each argument may be either a plain [socket instance](#module_socket.socket) (or any other kind of handle implementing a `fileno()` method) or a `[socket, flags]` tuple specifying the socket and requested poll flags. If a plain socket (or other kind of handle) instead of a tuple is provided, the requested poll flags default to `POLLIN|POLLERR|POLLHUP` for this socket. |

**Example**  
```ucode
let x = socket.connect("example.org", 80);
let y = socket.connect("example.com", 80);

// Pass plain socket arguments
let events = socket.poll(10, x, y);
print(events); // [ [ "<socket 0x7>", 0 ], [ "<socket 0x8>", 0 ] ]

// Passing tuples allows attaching state information and requesting
// different I/O events
let events = socket.poll(10,
	[ x, socket.POLLOUT | socket.POLLHUP, "This is example.org" ],
	[ y, socket.POLLOUT | socket.POLLHUP, "This is example.com" ]
);
print(events); // [ [ "<socket 0x7>", 4, "This is example.org" ],
               //   [ "<socket 0x8>", 4, "This is example.com" ] ]
```

### socket.connect(host, [service], [hints], [timeout]) ⇒ [`socket`](#module_socket.socket)
Creates a network socket and connects it to the specified host and service.

This high level function combines the functionality of
[create()](#module_socket+create),
[addrinfo()](#module_socket+addrinfo) and
[connect()](#module_socket.socket+connect) to simplify connection
establishment with the socket module.

**Kind**: instance method of [`socket`](#module_socket)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| host | `string` \| `Array.<number>` \| [`SocketAddress`](#module_socket.socket.SocketAddress) |  | The host to connect to, can be an IP address, hostname, [SocketAddress](#module_socket.socket.SocketAddress), or an array value returned by [iptoarr()](module:core#iptoarr). |
| [service] | `string` \| `number` |  | The service to connect to, can be a symbolic service name (such as "http") or a port number. Optional if host is specified as [SocketAddress](#module_socket.socket.SocketAddress). |
| [hints] | `Object` |  | Optional preferences for the socket. It can contain the following properties: - `family`: The preferred address family (`AF_INET` or `AF_INET6`). - `socktype`: The socket type (`SOCK_STREAM`, `SOCK_DGRAM`, etc.). - `protocol`: The protocol of the created socket. - `flags`: Bitwise OR-ed `AI_*` flags to control the resolution behavior. If no hints are not provided, the default socket type preference is set to `SOCK_STREAM`. |
| [timeout] | `number` | `-1` | The timeout in milliseconds for socket connect operations. If set to a negative value, no specifc time limit is imposed and the function will block until either a connection was successfull or the underlying operating system timeout is reached. |

**Example**  
```ucode
// Resolve host, try to connect to both resulting IPv4 and IPv6 addresses
let conn = socket.connect("example.org", 80);

// Enforce usage of IPv6
let conn = socket.connect("example.com", 80, { family: socket.AF_INET6 });

// Connect a UDP socket
let conn = socket.connect("192.168.1.1", 53, { socktype: socket.SOCK_DGRAM });

// Bypass name resolution by specifying a SocketAddress structure
let conn = socket.connect({ address: "127.0.0.1", port: 9000 });

// Use SocketAddress structure to connect a UNIX domain socket
let conn = socket.connect({ path: "/var/run/daemon.sock" });
```

### socket.listen(host, [service], [hints], [backlog], [reuseaddr]) ⇒ [`socket`](#module_socket.socket)
Binds a listening network socket to the specified host and service.

This high-level function combines the functionality of
[create()](#module_socket+create),
[addrinfo()](#module_socket+addrinfo),
[bind()](#module_socket.socket+bind), and
[listen()](#module_socket.socket+listen) to simplify setting up a
listening socket with the socket module.

**Kind**: instance method of [`socket`](#module_socket)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| host | `string` \| `Array.<number>` \| [`SocketAddress`](#module_socket.socket.SocketAddress) |  | The host to bind to, can be an IP address, hostname, [SocketAddress](#module_socket.socket.SocketAddress), or an array value returned by [iptoarr()](module:core#iptoarr). |
| [service] | `string` \| `number` |  | The service to listen on, can be a symbolic service name (such as "http") or a port number. Optional if host is specified as [SocketAddress](#module_socket.socket.SocketAddress). |
| [hints] | `Object` |  | Optional preferences for the socket. It can contain the following properties: - `family`: The preferred address family (`AF_INET` or `AF_INET6`). - `socktype`: The socket type (`SOCK_STREAM`, `SOCK_DGRAM`, etc.). - `protocol`: The protocol of the created socket. - `flags`: Bitwise OR-ed `AI_*` flags to control the resolution behavior. If no hints are provided, the default socket type preference is set to `SOCK_STREAM`. |
| [backlog] | `number` | `128` | The maximum length of the queue of pending connections. |
| [reuseaddr] | `boolean` |  | Whether to set the SO_REUSEADDR option before calling bind(). |

**Example**  
```ucode
// Listen for incoming TCP connections on port 80
let server = socket.listen("localhost", 80);

// Listen on IPv6 address only
let server = socket.listen("machine.local", 8080, { family: socket.AF_INET6 });

// Listen on a UNIX domain socket
let server = socket.listen({ path: "/var/run/server.sock" });
```

### socket.create([domain], [type], [protocol]) ⇒ [`socket`](#module_socket.socket)
Creates a network socket instance.

This function creates a new network socket with the specified domain and
type, determined by one of the modules `AF_*` and `SOCK_*` constants
respectively, and returns the resulting socket instance for use in subsequent
socket operations.

The domain argument specifies the protocol family, such as AF_INET or
AF_INET6, and defaults to AF_INET if not provided.

The type argument specifies the socket type, such as SOCK_STREAM or
SOCK_DGRAM, and defaults to SOCK_STREAM if not provided. It may also
be bitwise OR-ed with SOCK_NONBLOCK to enable non-blocking mode or
SOCK_CLOEXEC to enable close-on-exec semantics.

The protocol argument may be used to indicate a particular protocol
to be used with the socket, and it defaults to 0 (automatically
determined protocol) if not provided.

Returns a socket descriptor representing the newly created socket.

Returns `null` if an error occurred during socket creation.

**Kind**: instance method of [`socket`](#module_socket)  
**Returns**: [`socket`](#module_socket.socket) - A socket instance representing the newly created socket.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [domain] | `number` | `AF_INET` | The communication domain for the socket, e.g., AF_INET or AF_INET6. |
| [type] | `number` | `SOCK_STREAM` | The socket type, e.g., SOCK_STREAM or SOCK_DGRAM. It may also be bitwise OR-ed with SOCK_NONBLOCK or SOCK_CLOEXEC. |
| [protocol] | `number` | `0` | The protocol to be used with the socket. |

**Example**  
```ucode
// Create a TCP socket
const tcp_socket = create(AF_INET, SOCK_STREAM);

// Create a nonblocking IPv6 UDP socket
const udp_socket = create(AF_INET6, SOCK_DGRAM | SOCK_NONBLOCK);
```

### socket.open([fd]) ⇒ [`socket`](#module_socket.socket)
Creates a network socket instance from an existing file descriptor.

Returns a socket descriptor representing the newly created socket.

Returns `null` if an error occurred during socket creation.

**Kind**: instance method of [`socket`](#module_socket)  
**Returns**: [`socket`](#module_socket.socket) - A socket instance representing the socket.  

| Param | Type | Description |
| --- | --- | --- |
| [fd] | `number` | The file descriptor number |

### socket.pair([type]) ⇒ `Array.<?module:socket.socket>`
Creates a connected socket instance with a pair file descriptor.

This function creates new network sockets with the specified type,
determined by one of the `SOCK_*` constants, and returns resulting socket
instances for use in subsequent socket operations.

The type argument specifies the socket type, such as SOCK_STREAM or
SOCK_DGRAM, and defaults to SOCK_STREAM if not provided. It may also
be bitwise OR-ed with SOCK_NONBLOCK to enable non-blocking mode or
SOCK_CLOEXEC to enable close-on-exec semantics.

Returns an array of socket descriptors.

Returns `null` if an error occurred during socket creation.

**Kind**: instance method of [`socket`](#module_socket)  
**Returns**: `Array.<?module:socket.socket>` - Socket instances representing the newly created sockets.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [type] | `number` | `SOCK_STREAM` | The socket type, e.g., SOCK_STREAM or SOCK_DGRAM. It may also be bitwise OR-ed with SOCK_NONBLOCK or SOCK_CLOEXEC. |

**Example**  
```ucode
// Create a TCP socket pair
const tcp_sockets = pair(SOCK_STREAM);

// Create a nonblocking IPv6 UDP socket pair
const udp_sockets = pair(SOCK_DGRAM | SOCK_NONBLOCK);
```

### socket.socket
**Kind**: static class of [`socket`](#module_socket)  
**See**: [create()](#module_socket+create)  

* [.socket](#module_socket.socket)
    * _instance_
        * [.setopt(level, option, value)](#module_socket.socket+setopt) ⇒ `boolean`
        * [.getopt(level, option)](#module_socket.socket+getopt) ⇒ `\*`
        * [.fileno()](#module_socket.socket+fileno) ⇒ `number`
        * [.connect(address, port)](#module_socket.socket+connect) ⇒ `boolean`
        * [.send(data, [flags], [address])](#module_socket.socket+send) ⇒ `number`
        * [.recv([length], [flags], [address])](#module_socket.socket+recv) ⇒ `string`
        * [.sendmsg([data], [ancillaryData], [address], [flags])](#module_socket.socket+sendmsg) ⇒ `number`
        * [.recvmsg([sizes], [ancillarySize], [flags])](#module_socket.socket+recvmsg) ⇒ [`ReceivedMessage`](#module_socket.socket.ReceivedMessage)
        * [.bind(address)](#module_socket.socket+bind) ⇒ `boolean`
        * [.listen([backlog])](#module_socket.socket+listen) ⇒ `boolean`
        * [.accept([address], [flags])](#module_socket.socket+accept) ⇒ [`socket`](#module_socket.socket)
        * [.shutdown(how)](#module_socket.socket+shutdown) ⇒ `boolean`
        * [.peercred()](#module_socket.socket+peercred) ⇒ [`PeerCredentials`](#module_socket.socket.PeerCredentials)
        * [.peername()](#module_socket.socket+peername) ⇒ [`SocketAddress`](#module_socket.socket.SocketAddress)
        * [.sockname()](#module_socket.socket+sockname) ⇒ [`SocketAddress`](#module_socket.socket.SocketAddress)
        * [.close()](#module_socket.socket+close) ⇒ `boolean`
        * [.error([numeric])](#module_socket.socket+error) ⇒ `string` \| `number`
    * _static_
        * [.SocketAddress](#module_socket.socket.SocketAddress) : `Object`
        * [.ControlMessage](#module_socket.socket.ControlMessage) : `Object`
        * [.ReceivedMessage](#module_socket.socket.ReceivedMessage) : `Object`
        * [.PeerCredentials](#module_socket.socket.PeerCredentials) : `Object`

#### socket.setopt(level, option, value) ⇒ `boolean`
Sets options on the socket.

Sets the specified option on the socket to the given value.

Returns `true` if the option was successfully set.

Returns `null` if an error occurred.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Description |
| --- | --- | --- |
| level | `number` | The protocol level at which the option resides. This can be a level such as `SOL_SOCKET` for the socket API level or a specific protocol level defined by the system. |
| option | `number` | The socket option to set. This can be an integer representing the option, such as `SO_REUSEADDR`, or a constant defined by the system. |
| value | `\*` | The value to set the option to. The type of this argument depends on the specific option being set. It can be an integer, a boolean, a string, or a dictionary representing the value to set. If a dictionary is provided, it is internally translated to the corresponding C struct type required by the option. |

#### socket.getopt(level, option) ⇒ `\*`
Gets options from the socket.

Retrieves the value of the specified option from the socket.

Returns the value of the requested option.

Returns `null` if an error occurred or if the option is not supported.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**Returns**: `\*` - The value of the requested option. The type of the returned value depends
on the specific option being retrieved. It can be an integer, a boolean, a
string, or a dictionary representing a complex data structure.  

| Param | Type | Description |
| --- | --- | --- |
| level | `number` | The protocol level at which the option resides. This can be a level such as `SOL_SOCKET` for the socket API level or a specific protocol level defined by the system. |
| option | `number` | The socket option to retrieve. This can be an integer representing the option, such as `SO_REUSEADDR`, or a constant defined by the system. |

#### socket.fileno() ⇒ `number`
Returns the UNIX file descriptor number associated with the socket.

Returns the file descriptor number.

Returns `-1` if an error occurred.

**Kind**: instance method of [`socket`](#module_socket.socket)  

#### socket.connect(address, port) ⇒ `boolean`
Connects the socket to a remote address.

Attempts to establish a connection to the specified remote address.

Returns `true` if the connection is successfully established.
Returns `null` if an error occurred during the connection attempt.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| [`SocketAddress`](#module_socket.socket.SocketAddress) | The address of the remote endpoint to connect to. |
| port | `number` | The port number of the remote endpoint to connect to. |

#### socket.send(data, [flags], [address]) ⇒ `number`
Sends data through the socket.

Sends the provided data through the socket handle to the specified remote
address, if provided.

Returns the number of bytes sent.
Returns `null` if an error occurred during the send operation.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**See**: [sockaddr()](#module_socket+sockaddr)  

| Param | Type | Description |
| --- | --- | --- |
| data | `\*` | The data to be sent through the socket. String data is sent as-is, any other type is implicitly converted to a string first before being sent on the socket. |
| [flags] | `number` | Optional flags that modify the behavior of the send operation. |
| [address] | [`SocketAddress`](#module_socket.socket.SocketAddress) \| `Array.<number>` \| `string` | The address of the remote endpoint to send the data to. It can be either an IP address string, an array returned by [iptoarr()](module:core#iptoarr), or an object representing a network address. If not provided, the data is sent to the remote endpoint the socket is connected to. |

**Example**  
```ucode
// Send to connected socket
let tcp_sock = socket.create(socket.AF_INET, socket.SOCK_STREAM);
tcp_sock.connect("192.168.1.1", 80);
tcp_sock.send("GET / HTTP/1.0\r\n\r\n");

// Send a datagram on unconnected socket
let udp_sock = socket.create(socket.AF_INET, socket.SOCK_DGRAM);
udp_sock.send("Hello there!", 0, "255.255.255.255:9000");
udp_sock.send("Hello there!", 0, {
  family: socket.AF_INET,      // optional
  address: "255.255.255.255",
  port: 9000
});
```

#### socket.recv([length], [flags], [address]) ⇒ `string`
Receives data from the socket.

Receives data from the socket handle, optionally specifying the maximum
length of data to receive, flags to modify the receive behavior, and an
optional address dictionary where the function will place the address from
which the data was received (for unconnected sockets).

Returns a string containing the received data.
Returns an empty string if the remote side closed the socket.
Returns `null` if an error occurred during the receive operation.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [length] | `number` | `4096` | The maximum number of bytes to receive. |
| [flags] | `number` |  | Optional flags that modify the behavior of the receive operation. |
| [address] | `Object` |  | An object where the function will store the address from which the data was received. If provided, it will be filled with the details obtained from the sockaddr argument of the underlying `recvfrom()` syscall. See the type definition of [SocketAddress](#module_socket.socket.SocketAddress) for details on the format. |

#### socket.sendmsg([data], [ancillaryData], [address], [flags]) ⇒ `number`
Sends a message through the socket.

Sends a message through the socket handle, supporting complex message
structures including multiple data buffers and ancillary data. This function
allows for precise control over the message content and delivery behavior.

Returns the number of sent bytes.

Returns `null` if an error occurred.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**Returns**: `number` - Returns the number of bytes sent on success, or `null` if an error occurred.  

| Param | Type | Description |
| --- | --- | --- |
| [data] | `\*` | The data to be sent. If a string is provided, it is sent as is. If an array is specified, each item is sent as a separate `struct iovec`. Non-string values are implicitly converted to a string and sent. If omitted, only ancillary data and address are considered. |
| [ancillaryData] | [`Array.<ControlMessage>`](#module_socket.socket.ControlMessage) \| `string` | Optional ancillary data to be sent. If an array is provided, each element is converted to a control message. If a string is provided, it is sent as-is without further interpretation. Refer to [`recvmsg()`](#module_socket.socket+recvmsg) and [ControlMessage](#module_socket.socket.ControlMessage) for details. |
| [address] | [`SocketAddress`](#module_socket.socket.SocketAddress) | The destination address for the message. If provided, it sets or overrides the packet destination address. |
| [flags] | `number` | Optional flags to modify the behavior of the send operation. This should be a bitwise OR-ed combination of `MSG_*` flag values. |

**Example**  
```ucode
// Send file descriptors over domain socket
const f1 = fs.open("example.txt", "w");
const f2 = fs.popen("date +%s", "r");
const sk = socket.connect({ family: socket.AF_UNIX, path: "/tmp/socket" });
sk.sendmsg("Hi there, here's some descriptors!", [
	{ level: socket.SOL_SOCKET, type: socket.SCM_RIGHTS, data: [ f1, f2 ] }
]);

// Send multiple values in one datagram
sk.sendmsg([ "This", "is", "one", "message" ]);
```

#### socket.recvmsg([sizes], [ancillarySize], [flags]) ⇒ [`ReceivedMessage`](#module_socket.socket.ReceivedMessage)
Receives a message from the socket.

Receives a message from the socket handle, allowing for more complex data
reception compared to `recv()`. This includes the ability to receive
ancillary data (such as file descriptors, credentials, etc.), multiple
message segments, and optional flags to modify the receive behavior.

Returns an object containing the received message data, ancillary data,
and the sender's address.

Returns `null` if an error occurred during the receive operation.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**Returns**: [`ReceivedMessage`](#module_socket.socket.ReceivedMessage) - An object containing the received message data, ancillary data,
and the sender's address.  

| Param | Type | Description |
| --- | --- | --- |
| [sizes] | `Array.<number>` \| `number` | Specifies the sizes of the buffers used for receiving the message. If an array of numbers is provided, each number determines the size of an individual buffer segment, creating multiple `struct iovec` for reception. If a single number is provided, a single buffer of that size is used. |
| [ancillarySize] | `number` | The size allocated for the ancillary data buffer. If not provided, ancillary data is not processed. |
| [flags] | `number` | Optional flags to modify the behavior of the receive operation. This should be a bitwise OR-ed combination of flag values. |

**Example**  
```ucode
// Receive file descriptors over domain socket
const sk = socket.listen({ family: socket.AF_UNIX, path: "/tmp/socket" });
sk.setopt(socket.SOL_SOCKET, socket.SO_PASSCRED, true);

const msg = sk.recvmsg(1024, 1024);
for (let cmsg in msg.ancillary)
  if (cmsg.level == socket.SOL_SOCKET && cmsg.type == socket.SCM_RIGHTS)
    print(`Got some descriptors: ${cmsg.data}!\n`);

// Receive message in segments of 10, 128 and 512 bytes
const msg = sk.recvmsg([ 10, 128, 512 ]);
print(`Message parts: ${msg.data[0]}, ${msg.data[1]}, ${msg.data[2]}\n`);

// Peek buffer
const msg = sk.recvmsg(0, 0, socket.MSG_PEEK|socket.MSG_TRUNC);
print(`Received ${length(msg.data)} bytes, ${msg.length} bytes available\n`);
```

#### socket.bind(address) ⇒ `boolean`
Binds a socket to a specific address.

This function binds the socket to the specified address.

Returns `true` if the socket is successfully bound.

Returns `null` on error, e.g. when the address is in use.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Description |
| --- | --- | --- |
| address | `string` \| [`SocketAddress`](#module_socket.socket.SocketAddress) | The IP address to bind the socket to. |

**Example**  
```text
const sock = socket.create(…);
const success = sock.bind("192.168.0.1:80");

if (success)
    print(`Socket bound successfully!\n`);
else
    print(`Failed to bind socket: ${sock.error()}.\n`);
```

#### socket.listen([backlog]) ⇒ `boolean`
Listen for connections on a socket.

This function marks the socket as a passive socket, that is, as a socket that
will be used to accept incoming connection requests using `accept()`.

The `backlog` parameter specifies the maximum length to which the queue of
pending connections may grow. If a connection request arrives when the queue
is full, the client connection might get refused.

If `backlog` is not provided, it defaults to 128.

Returns `true` if the socket is successfully marked as passive.
Returns `null` if an error occurred, e.g. when the requested port is in use.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**See**: [accept()](#module_socket.socket+accept)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [backlog] | `number` | `128` | The maximum length of the queue of pending connections. |

**Example**  
```text
const sock = socket.create(…);
sock.bind(…);

const success = sock.listen(10);
if (success)
    print(`Socket is listening for incoming connections!\n`);
else
    print(`Failed to listen on socket: ${sock.error()}\n`);
```

#### socket.accept([address], [flags]) ⇒ [`socket`](#module_socket.socket)
Accept a connection on a socket.

This function accepts a connection on the socket. It extracts the first
connection request on the queue of pending connections, creates a new
connected socket, and returns a new socket handle referring to that socket.
The newly created socket is not in listening state and has no backlog.

When a optional `address` dictionary is provided, it is populated with the
remote address details of the peer socket.

The optional `flags` parameter is a bitwise-or-ed number of flags to modify
the behavior of accepted peer socket. Possible values are:
- `SOCK_CLOEXEC`: Enable close-on-exec semantics for the new socket.
- `SOCK_NONBLOCK`: Enable nonblocking mode for the new socket.

Returns a socket handle representing the newly created peer socket of the
accepted connection.

Returns `null` if an error occurred.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Description |
| --- | --- | --- |
| [address] | `object` | An optional dictionary to receive the address details of the peer socket. See [SocketAddress](#module_socket.socket.SocketAddress) for details. |
| [flags] | `number` | Optional flags to modify the behavior of the peer socket. |

**Example**  
```text
const sock = socket.create(…);
sock.bind(…);
sock.listen();

const peerAddress = {};
const newSocket = sock.accept(peerAddress, socket.SOCK_CLOEXEC);
if (newSocket)
    print(`Accepted connection from: ${peerAddress}\n`);
else
    print(`Failed to accept connection: ${sock.error()}\n`);
```

#### socket.shutdown(how) ⇒ `boolean`
Shutdown part of a full-duplex connection.

This function shuts down part of the full-duplex connection associated with
the socket handle. The `how` parameter specifies which half of the connection
to shut down. It can take one of the following constant values:

- `SHUT_RD`: Disables further receive operations.
- `SHUT_WR`: Disables further send operations.
- `SHUT_RDWR`: Disables further send and receive operations.

Returns `true` if the shutdown operation is successful.
Returns `null` if an error occurred.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Description |
| --- | --- | --- |
| how | `number` | Specifies which half of the connection to shut down. It can be one of the following constant values: `SHUT_RD`, `SHUT_WR`, or `SHUT_RDWR`. |

**Example**  
```text
const sock = socket.create(…);
sock.connect(…);
// Perform data exchange…

const success = sock.shutdown(socket.SHUT_WR);
if (success)
    print(`Send operations on socket shut down successfully.\n`);
else
    print(`Failed to shut down send operations: ${sock.error()}\n`);
```

#### socket.peercred() ⇒ [`PeerCredentials`](#module_socket.socket.PeerCredentials)
Retrieves the peer credentials.

This function retrieves the remote uid, gid and pid of a connected UNIX
domain socket.

Returns the remote credentials if the operation is successful.
Returns `null` on error.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**Example**  
```text
const sock = socket.create(socket.AF_UNIX, …);
sock.connect(…);

const peerCredentials = sock.peercred();
if (peerCredentials)
    print(`Peer credentials: ${peerCredentials}\n`);
else
    print(`Failed to retrieve peer credentials: ${sock.error()}\n`);
```

#### socket.peername() ⇒ [`SocketAddress`](#module_socket.socket.SocketAddress)
Retrieves the remote address.

This function retrieves the remote address of a connected socket.

Returns the remote address if the operation is successful.
Returns `null` on error.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**See**: [sockname()](#module_socket.socket+sockname)  
**Example**  
```text
const sock = socket.create(…);
sock.connect(…);

const peerAddress = sock.peername();
if (peerAddress)
    print(`Connected to ${peerAddress}\n`);
else
    print(`Failed to retrieve peer address: ${sock.error()}\n`);
```

#### socket.sockname() ⇒ [`SocketAddress`](#module_socket.socket.SocketAddress)
Retrieves the local address.

This function retrieves the local address of a bound or connected socket.

Returns the local address if the operation is successful.
Returns `null` on error.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**See**: [peername()](#module_socket.socket+peername)  
**Example**  
```text
const sock = socket.create(…);
sock.connect(…);

const myAddress = sock.sockname();
if (myAddress)
    print(`My source IP address is ${myAddress}\n`);
else
    print(`Failed to retrieve peer address: ${sock.error()}\n`);
```

#### socket.close() ⇒ `boolean`
Closes the socket.

This function closes the socket, releasing its resources and terminating its
associated connections.

Returns `true` if the socket was successfully closed.
Returns `null` on error.

**Kind**: instance method of [`socket`](#module_socket.socket)  
**Example**  
```text
const sock = socket.create(…);
sock.connect(…);
// Perform operations with the socket…
sock.close();
```

#### socket.error([numeric]) ⇒ `string` \| `number`
Query error information.

Returns a string containing a description of the last occurred error when
the *numeric* argument is absent or false.

Returns a positive (`errno`) or negative (`EAI_*` constant) error code number
when the *numeric* argument is `true`.

Returns `null` if there is no error information.

**Kind**: instance method of [`socket`](#module_socket.socket)  

| Param | Type | Description |
| --- | --- | --- |
| [numeric] | `boolean` | Whether to return a numeric error code (`true`) or a human readable error message (false). |

**Example**  
```ucode
// Trigger socket error by attempting to bind IPv6 address with IPv4 socket
socket.create(socket.AF_INET, socket.SOCK_STREAM, 0).bind("::", 8080);

// Print error (should yield "Address family not supported by protocol")
print(socket.error(), "\n");

// Trigger resolve error
socket.addrinfo("doesnotexist.org");

// Query error code (should yield -2 for EAI_NONAME)
print(socket.error(true), "\n");  //
```

#### socket.SocketAddress : `Object`
**Kind**: static typedef of [`socket`](#module_socket.socket)  
**Properties**

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| family | `number` |  | Address family, one of AF_INET, AF_INET6, AF_UNIX, AF_PACKET or AF_CAN. |
| address | `string` |  | IPv4/IPv6 address string (AF_INET or AF_INET6 only) or hardware address in hexadecimal notation (AF_PACKET only). |
| [port] | `number` |  | Port number (AF_INET or AF_INET6 only). |
| [flowinfo] | `number` |  | IPv6 flow information (AF_INET6 only). |
| [interface] | `string` \| `number` |  | Link local address scope (for IPv6 sockets) or bound network interface (for packet and CAN sockets), either a network device name string or a nonzero positive integer representing a network interface index (AF_INET6, AF_PACKET and AF_CAN only). |
| path | `string` |  | Domain socket filesystem path (AF_UNIX only). |
| [protocol] | `number` | `0` | Physical layer protocol (AF_PACKET only). |
| [hardware_type] | `number` | `0` | ARP hardware type (AF_PACKET only). |
| [packet_type] | `number` | `PACKET_HOST` | Packet type (AF_PACKET only). |

#### socket.ControlMessage : `Object`
Represents a single control (ancillary data) message returned
in the *ancillary* array by [`recvmsg()`](#module_socket.socket+recvmsg).

**Kind**: static typedef of [`socket`](#module_socket.socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| level | `number` | The message socket level (`cmsg_level`), e.g. `SOL_SOCKET`. |
| type | `number` | The protocol specific message type (`cmsg_type`), e.g. `SCM_RIGHTS`. |
| data | `\*` | The payload of the control message. If the control message type is known by the socket module, it is represented as a mixed value (array, object, number, etc.) with structure specific to the control message type. If the control message cannot be decoded, *data* is set to a string value containing the raw payload. |

#### socket.ReceivedMessage : `Object`
Represents a message object returned by
[`recvmsg()`](#module_socket.socket+recvmsg).

**Kind**: static typedef of [`socket`](#module_socket.socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| flags | `number` | Integer value containing bitwise OR-ed `MSG_*` result flags returned by the underlying receive call. |
| length | `number` | Integer value containing the number of bytes returned by the `recvmsg()` syscall, which might be larger than the received data in case `MSG_TRUNC` was passed. |
| address | [`SocketAddress`](#module_socket.socket.SocketAddress) | The address from which the message was received. |
| data | `Array.<string>` \| `string` | An array of strings, each representing the received message data. Each string corresponds to one buffer size specified in the *sizes* argument. If a single receive size was passed instead of an array of sizes, *data* will hold a string containing the received data. |
| [ancillary] | [`Array.<ControlMessage>`](#module_socket.socket.ControlMessage) | An array of received control messages. Only included if a non-zero positive *ancillarySize* was passed to `recvmsg()`. |

#### socket.PeerCredentials : `Object`
Represents a credentials information object returned by
[`peercred()`](#module_socket.socket+peercred).

**Kind**: static typedef of [`socket`](#module_socket.socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| uid | `number` | The effective user ID the remote socket endpoint. |
| gid | `number` | The effective group ID the remote socket endpoint. |
| pid | `number` | The ID of the process the remote socket endpoint belongs to. |

### socket.AddressInfo : `Object`
Represents a network address information object returned by
[`addrinfo()`](#module_socket+addrinfo).

**Kind**: static typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| addr | [`SocketAddress`](#module_socket.socket.SocketAddress) |  | A socket address structure. |
| [canonname] | `string` | `null` | The canonical hostname associated with the address. |
| family | `number` |  | The address family (e.g., `2` for `AF_INET`, `10` for `AF_INET6`). |
| flags | `number` |  | Additional flags indicating properties of the address. |
| protocol | `number` |  | The protocol number. |
| socktype | `number` |  | The socket type (e.g., `1` for `SOCK_STREAM`, `2` for `SOCK_DGRAM`). |

### socket.PollSpec : `Array`
Represents a poll state serving as input parameter and return value type for
[`poll()`](#module_socket+poll).

**Kind**: static typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| 0 | [`socket`](#module_socket.socket) | The polled socket instance. |
| 1 | `number` | Requested or returned status flags of the polled socket instance. |

### socket~Address Families
Constants representing address families and socket domains.

**Kind**: inner typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| AF_UNSPEC | `number` | Unspecified address family. |
| AF_UNIX | `number` | UNIX domain sockets. |
| AF_INET | `number` | IPv4 Internet protocols. |
| AF_INET6 | `number` | IPv6 Internet protocols. |
| AF_PACKET | `number` | Low-level packet interface. |
| AF_CAN | `number` | Controller Area Network sockets. |

### socket~Socket Types
The `SOCK_*` type and flag constants are used by
[create()](#module_socket+create) to specify the type of socket to
open. The [accept()](#module_socket.socket+accept) function
recognizes the `SOCK_NONBLOCK` and `SOCK_CLOEXEC` flags and applies them
to accepted peer sockets.

**Kind**: inner typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| SOCK_STREAM | `number` | Provides sequenced, reliable, two-way, connection-based byte streams. |
| SOCK_DGRAM | `number` | Supports datagrams (connectionless, unreliable messages of a fixed maximum length). |
| SOCK_RAW | `number` | Provides raw network protocol access. |
| SOCK_PACKET | `number` | Obsolete and should not be used. |
| SOCK_NONBLOCK | `number` | Enables non-blocking operation. |
| SOCK_CLOEXEC | `number` | Sets the close-on-exec flag on the new file descriptor. |

### socket~Message Flags
The `MSG_*` flag constants are commonly used in conjunction with the
[send()](#module_socket.socket+send) and
[recv()](#module_socket.socket+recv) functions.

**Kind**: inner typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| MSG_CONFIRM | `number` | Confirm path validity. |
| MSG_DONTROUTE | `number` | Send without using routing tables. |
| MSG_DONTWAIT | `number` | Enables non-blocking operation. |
| MSG_EOR | `number` | End of record. |
| MSG_MORE | `number` | Sender will send more. |
| MSG_NOSIGNAL | `number` | Do not generate SIGPIPE. |
| MSG_OOB | `number` | Process out-of-band data. |
| MSG_FASTOPEN | `number` | Send data in TCP SYN. |
| MSG_CMSG_CLOEXEC | `number` | Sets the close-on-exec flag on the received file descriptor. |
| MSG_ERRQUEUE | `number` | Receive errors from ICMP. |
| MSG_PEEK | `number` | Peeks at incoming messages. |
| MSG_TRUNC | `number` | Report if datagram truncation occurred. |
| MSG_WAITALL | `number` | Wait for full message. |

### socket~IP Protocol Constants
The `IPPROTO_IP` constant specifies the IP protocol number and may be
passed as third argument to [create()](#module_socket+create) as well
as *level* argument value to [getopt()](#module_socket.socket+getopt)
and [setopt()](#module_socket.socket+setopt).

The `IP_*` constants are option names recognized by
[getopt()](#module_socket.socket+getopt)
and [setopt()](#module_socket.socket+setopt), in conjunction with
the `IPPROTO_IP` socket level.

**Kind**: inner typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IPPROTO_IP | `number` | Dummy protocol for IP. |
| IP_ADD_MEMBERSHIP | `number` | Add an IP group membership. |
| IP_ADD_SOURCE_MEMBERSHIP | `number` | Add an IP group/source membership. |
| IP_BIND_ADDRESS_NO_PORT | `number` | Bind to the device only. |
| IP_BLOCK_SOURCE | `number` | Block IP group/source. |
| IP_DROP_MEMBERSHIP | `number` | Drop an IP group membership. |
| IP_DROP_SOURCE_MEMBERSHIP | `number` | Drop an IP group/source membership. |
| IP_FREEBIND | `number` | Allow binding to an IP address not assigned to a network interface. |
| IP_HDRINCL | `number` | Header is included with data. |
| IP_MSFILTER | `number` | Filter IP multicast source memberships. |
| IP_MTU | `number` | Path MTU discovery. |
| IP_MTU_DISCOVER | `number` | Control Path MTU discovery. |
| IP_MULTICAST_ALL | `number` | Receive all multicast packets. |
| IP_MULTICAST_IF | `number` | Set outgoing interface for multicast packets. |
| IP_MULTICAST_LOOP | `number` | Control multicast packet looping. |
| IP_MULTICAST_TTL | `number` | Set time-to-live for outgoing multicast packets. |
| IP_NODEFRAG | `number` | Don't fragment IP packets. |
| IP_OPTIONS | `number` | Set/get IP options. |
| IP_PASSSEC | `number` | Pass security information. |
| IP_PKTINFO | `number` | Receive packet information. |
| IP_RECVERR | `number` | Receive all ICMP errors. |
| IP_RECVOPTS | `number` | Receive all IP options. |
| IP_RECVORIGDSTADDR | `number` | Receive original destination address of the socket. |
| IP_RECVTOS | `number` | Receive IP TOS. |
| IP_RECVTTL | `number` | Receive IP TTL. |
| IP_RETOPTS | `number` | Set/get IP options. |
| IP_ROUTER_ALERT | `number` | Receive ICMP msgs generated by router. |
| IP_TOS | `number` | IP type of service and precedence. |
| IP_TRANSPARENT | `number` | Transparent proxy support. |
| IP_TTL | `number` | IP time-to-live. |
| IP_UNBLOCK_SOURCE | `number` | Unblock IP group/source. |

### socket~IPv6 : `Object`
The `IPPROTO_IPV6` constant specifies the IPv6 protocol number and may be
passed as third argument to [create()](#module_socket+create) as well
as *level* argument value to [getopt()](#module_socket.socket+getopt)
and [setopt()](#module_socket.socket+setopt).

The `IPV6_*` constants are option names recognized by
[getopt()](#module_socket.socket+getopt)
and [setopt()](#module_socket.socket+setopt), in conjunction with
the `IPPROTO_IPV6` socket level.

**Kind**: inner typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| IPPROTO_IPV6 | `number` | The IPv6 protocol. |
| IPV6_ADDRFORM | `number` | Turn an AF_INET6 socket into a socket of a different address family. Only AF_INET is supported. |
| IPV6_ADDR_PREFERENCES | `number` | Specify preferences for address selection. |
| IPV6_ADD_MEMBERSHIP | `number` | Add an IPv6 group membership. |
| IPV6_AUTHHDR | `number` | Set delivery of the authentication header control message for incoming datagrams. |
| IPV6_AUTOFLOWLABEL | `number` | Enable or disable automatic flow labels. |
| IPV6_DONTFRAG | `number` | Control whether the socket allows IPv6 fragmentation. |
| IPV6_DROP_MEMBERSHIP | `number` | Drop an IPv6 group membership. |
| IPV6_DSTOPTS | `number` | Set delivery of the destination options control message for incoming datagrams. |
| IPV6_FLOWINFO_SEND | `number` | Control whether flow information is sent. |
| IPV6_FLOWINFO | `number` | Set delivery of the flow ID control message for incoming datagrams. |
| IPV6_FLOWLABEL_MGR | `number` | Manage flow labels. |
| IPV6_FREEBIND | `number` | Allow binding to an IP address not assigned to a network interface. |
| IPV6_HOPLIMIT | `number` | Set delivery of the hop limit control message for incoming datagrams. |
| IPV6_HOPOPTS | `number` | Set delivery of the hop options control message for incoming datagrams. |
| IPV6_JOIN_ANYCAST | `number` | Join an anycast group. |
| IPV6_LEAVE_ANYCAST | `number` | Leave an anycast group. |
| IPV6_MINHOPCOUNT | `number` | Set the minimum hop count. |
| IPV6_MTU | `number` | Retrieve or set the MTU to be used for the socket. |
| IPV6_MTU_DISCOVER | `number` | Control path-MTU discovery on the socket. |
| IPV6_MULTICAST_ALL | `number` | Control whether the socket receives all multicast packets. |
| IPV6_MULTICAST_HOPS | `number` | Set the multicast hop limit for the socket. |
| IPV6_MULTICAST_IF | `number` | Set the device for outgoing multicast packets on the socket. |
| IPV6_MULTICAST_LOOP | `number` | Control whether the socket sees multicast packets that it has sent itself. |
| IPV6_PKTINFO | `number` | Set delivery of the IPV6_PKTINFO control message on incoming datagrams. |
| IPV6_RECVDSTOPTS | `number` | Control receiving of the destination options control message. |
| IPV6_RECVERR | `number` | Control receiving of asynchronous error options. |
| IPV6_RECVFRAGSIZE | `number` | Control receiving of fragment size. |
| IPV6_RECVHOPLIMIT | `number` | Control receiving of hop limit. |
| IPV6_RECVHOPOPTS | `number` | Control receiving of hop options. |
| IPV6_RECVORIGDSTADDR | `number` | Control receiving of the original destination address. |
| IPV6_RECVPATHMTU | `number` | Control receiving of path MTU. |
| IPV6_RECVPKTINFO | `number` | Control receiving of packet information. |
| IPV6_RECVRTHDR | `number` | Control receiving of routing header. |
| IPV6_RECVTCLASS | `number` | Control receiving of traffic class. |
| IPV6_ROUTER_ALERT_ISOLATE | `number` | Control isolation of router alert messages. |
| IPV6_ROUTER_ALERT | `number` | Pass forwarded packets containing a router alert hop-by-hop option to this socket. |
| IPV6_RTHDR | `number` | Set delivery of the routing header control message for incoming datagrams. |
| IPV6_RTHDRDSTOPTS | `number` | Set delivery of the routing header destination options control message. |
| IPV6_TCLASS | `number` | Set the traffic class. |
| IPV6_TRANSPARENT | `number` | Enable transparent proxy support. |
| IPV6_UNICAST_HOPS | `number` | Set the unicast hop limit for the socket. |
| IPV6_UNICAST_IF | `number` | Set the interface for outgoing unicast packets. |
| IPV6_V6ONLY | `number` | Restrict the socket to sending and receiving IPv6 packets only. |

### socket~Socket Option Constants
The `SOL_SOCKET` constant is passed as *level* argument to the
[getopt()](#module_socket.socket+getopt) and
[setopt()](#module_socket.socket+setopt) functions in order to set
or retrieve generic socket option values.

The `SO_*` constants are passed as *option* argument in conjunction with
the `SOL_SOCKET` level to specify the specific option to get or set on
the socket.

**Kind**: inner typedef of [`socket`](#module_socket)  
**Properties**

| Name | Type | Description |
| --- | --- | --- |
| SOL_SOCKET | `number` | Socket options at the socket API level. |
| SO_ACCEPTCONN | `number` | Reports whether socket listening is enabled. |
| SO_ATTACH_BPF | `number` | Attach BPF program to socket. |
| SO_ATTACH_FILTER | `number` | Attach a socket filter. |
| SO_ATTACH_REUSEPORT_CBPF | `number` | Attach BPF program for cgroup and skb program reuseport hook. |
| SO_ATTACH_REUSEPORT_EBPF | `number` | Attach eBPF program for cgroup and skb program reuseport hook. |
| SO_BINDTODEVICE | `number` | Bind socket to a specific interface. |
| SO_BROADCAST | `number` | Allow transmission of broadcast messages. |
| SO_BUSY_POLL | `number` | Enable busy polling. |
| SO_DEBUG | `number` | Enable socket debugging. |
| SO_DETACH_BPF | `number` | Detach BPF program from socket. |
| SO_DETACH_FILTER | `number` | Detach a socket filter. |
| SO_DOMAIN | `number` | Retrieves the domain of the socket. |
| SO_DONTROUTE | `number` | Send packets directly without routing. |
| SO_ERROR | `number` | Retrieves and clears the error status for the socket. |
| SO_INCOMING_CPU | `number` | Retrieves the CPU number on which the last packet was received. |
| SO_INCOMING_NAPI_ID | `number` | Retrieves the NAPI ID of the device. |
| SO_KEEPALIVE | `number` | Enable keep-alive packets. |
| SO_LINGER | `number` | Set linger on close. |
| SO_LOCK_FILTER | `number` | Set or get the socket filter lock state. |
| SO_MARK | `number` | Set the mark for packets sent through the socket. |
| SO_OOBINLINE | `number` | Enables out-of-band data to be received in the normal data stream. |
| SO_PASSCRED | `number` | Enable the receiving of SCM_CREDENTIALS control messages. |
| SO_PASSSEC | `number` | Enable the receiving of security context. |
| SO_PEEK_OFF | `number` | Returns the number of bytes in the receive buffer without removing them. |
| SO_PEERCRED | `number` | Retrieves the credentials of the foreign peer. |
| SO_PEERSEC | `number` | Retrieves the security context of the foreign peer. |
| SO_PRIORITY | `number` | Set the protocol-defined priority for all packets. |
| SO_PROTOCOL | `number` | Retrieves the protocol number. |
| SO_RCVBUF | `number` | Set the receive buffer size. |
| SO_RCVBUFFORCE | `number` | Set the receive buffer size forcefully. |
| SO_RCVLOWAT | `number` | Set the minimum number of bytes to

---

# ucode module: struct

> **Live docs:** https://ucode.mein.io/module-struct.html

---

## Handle Packed Binary Data

The `struct` module provides routines for interpreting byte strings as packed
binary data.

Functions can be individually imported and directly accessed using the
[named import](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import#named_import)
syntax:

  ```ucode
  import { pack, unpack } from 'struct';

  let buffer = pack('bhl', -13, 1234, 444555666);
  let values = unpack('bhl', buffer);
  ```

Alternatively, the module namespace can be imported
using a wildcard import statement:

  ```ucode
  import * as struct from 'struct';

  let buffer = struct.pack('bhl', -13, 1234, 444555666);
  let values = struct.unpack('bhl', buffer);
  ```

Additionally, the struct module namespace may also be imported by invoking
the `ucode` interpreter with the `-lstruct` switch.

## Format Strings

Format strings describe the data layout when packing and unpacking data.
They are built up from format-characters, which specify the type of data
being packed/unpacked. In addition, special characters control the byte
order, size and alignment.

Each format string consists of an optional prefix character which describes
the overall properties of the data and one or more format characters which
describe the actual data values and padding.

### Byte Order, Size, and Alignment

By default, C types are represented in the machine's native format and byte
order, and properly aligned by skipping pad bytes if necessary (according to
the rules used by the C compiler).

This behavior is chosen so that the bytes of a packed struct correspond
exactly to the memory layout of the corresponding C struct.

Whether to use native byte ordering and padding or standard formats depends
on the application.

Alternatively, the first character of the format string can be used to indicate
the byte order, size and alignment of the packed data, according to the
following table:

| Character | Byte order             | Size     | Alignment |
|-----------|------------------------|----------|-----------|
| `@`       | native                 | native   | native    |
| `=`       | native                 | standard | none      |
| `<`       | little-endian          | standard | none      |
| `>`       | big-endian             | standard | none      |
| `!`       | network (= big-endian) | standard | none      |

If the first character is not one of these, `'@'` is assumed.

Native byte order is big-endian or little-endian, depending on the
host system. For example, Intel x86, AMD64 (x86-64), and Apple M1 are
little-endian; IBM z and many legacy architectures are big-endian.

Native size and alignment are determined using the C compiler's
`sizeof` expression. This is always combined with native byte order.

Standard size depends only on the format character; see the table in
the `format-characters` section.

Note the difference between `'@'` and `'='`: both use native byte order,
but the size and alignment of the latter is standardized.

The form `'!'` represents the network byte order which is always big-endian
as defined in `IETF RFC 1700`.

There is no way to indicate non-native byte order (force byte-swapping); use
the appropriate choice of `'<'` or `'>'`.

Notes:

(1) Padding is only automatically added between successive structure members.
    No padding is added at the beginning or the end of the encoded struct.

(2) No padding is added when using non-native size and alignment, e.g.
    with '<', '>', '=', and '!'.

(3) To align the end of a structure to the alignment requirement of a
    particular type, end the format with the code for that type with a repeat
    count of zero.

### Format Characters

Format characters have the following meaning; the conversion between C and
ucode values should be obvious given their types.  The 'Standard size' column
refers to the size of the packed value in bytes when using standard size;
that is, when the format string starts with one of `'<'`, `'>'`, `'!'` or
`'='`.  When using native size, the size of the packed value is platform
dependent.

| Format | C Type               | Ucode type | Standard size  | Notes    |
|--------|----------------------|------------|----------------|----------|
| `x`    | *pad byte*           | *no value* |                | (7)      |
| `c`    | `char`               | string     | 1              |          |
| `b`    | `signed char`        | int        | 1              | (1), (2) |
| `B`    | `unsigned char`      | int        | 1              | (2)      |
| `?`    | `_Bool`              | bool       | 1              | (1)      |
| `h`    | `short`              | int        | 2              | (2)      |
| `H`    | `unsigned short`     | int        | 2              | (2)      |
| `i`    | `int`                | int        | 4              | (2)      |
| `I`    | `unsigned int`       | int        | 4              | (2)      |
| `l`    | `long`               | int        | 4              | (2)      |
| `L`    | `unsigned long`      | int        | 4              | (2)      |
| `q`    | `long long`          | int        | 8              | (2)      |
| `Q`    | `unsigned long long` | int        | 8              | (2)      |
| `n`    | `ssize_t`            | int        |                | (3)      |
| `N`    | `size_t`             | int        |                | (3)      |
| `e`    | (6)                  | double     | 2              | (4)      |
| `f`    | `float`              | double     | 4              | (4)      |
| `d`    | `double`             | double     | 8              | (4)      |
| `s`    | `char[]`             | double     |                | (9)      |
| `p`    | `char[]`             | double     |                | (8)      |
| `P`    | `void *`             | int        |                | (5)      |
| `*`    | `char[]`             | string     |                | (10)     |
| `X`    | `char[]`             | string     |                | (11)     |
| `Z`    | `char[]`             | string     |                | (12)     |

Notes:

- (1) The `'?'` conversion code corresponds to the `_Bool` type defined by
   C99. If this type is not available, it is simulated using a `char`. In
   standard mode, it is always represented by one byte.

- (2) When attempting to pack a non-integer using any of the integer
   conversion codes, this module attempts to convert the given value into an
   integer. If the value is not convertible, a type error exception is thrown.

- (3) The `'n'` and `'N'` conversion codes are only available for the native
   size (selected as the default or with the `'@'` byte order character).
   For the standard size, you can use whichever of the other integer formats
   fits your application.

- (4) For the `'f'`, `'d'` and `'e'` conversion codes, the packed
   representation uses the IEEE 754 binary32, binary64 or binary16 format
   (for `'f'`, `'d'` or `'e'` respectively), regardless of the floating-point
   format used by the platform.

- (5) The `'P'` format character is only available for the native byte
   ordering (selected as the default or with the `'@'` byte order character).
   The byte order character `'='` chooses to use little- or big-endian
   ordering based on the host system. The struct module does not interpret
   this as native ordering, so the `'P'` format is not available.

- (6) The IEEE 754 binary16 "half precision" type was introduced in the 2008
   revision of the `IEEE 754` standard. It has a sign bit, a 5-bit exponent
   and 11-bit precision (with 10 bits explicitly stored), and can represent
   numbers between approximately `6.1e-05` and `6.5e+04` at full precision.
   This type is not widely supported by C compilers: on a typical machine, an
   unsigned short can be used for storage, but not for math operations. See
   the Wikipedia page on the `half-precision floating-point format` for more
   information.

- (7) When packing, `'x'` inserts one NUL byte.

- (8) The `'p'` format character encodes a "Pascal string", meaning a short
   variable-length string stored in a *fixed number of bytes*, given by the
   count. The first byte stored is the length of the string, or 255,
   whichever is smaller.  The bytes of the string follow.  If the string
   passed in to `pack()` is too long (longer than the count minus 1), only
   the leading `count-1` bytes of the string are stored.  If the string is
   shorter than `count-1`, it is padded with null bytes so that exactly count
   bytes in all are used.  Note that for `unpack()`, the `'p'` format
   character consumes `count` bytes, but that the string returned can never
   contain more than 255 bytes.

- (9) For the `'s'` format character, the count is interpreted as the length
   of the bytes, not a repeat count like for the other format characters; for
   example, `'10s'` means a single 10-byte string mapping to or from a single
   ucode byte string, while `'10c'` means 10 separate one byte character
   elements (e.g., `cccccccccc`) mapping to or from ten different ucode byte
   strings. If a count is not given, it defaults to 1. For packing, the
   string is truncated or padded with null bytes as appropriate to make it
   fit. For unpacking, the resulting bytes object always has exactly the
   specified number of bytes.  As a special case, `'0s'` means a single,
   empty string (while `'0c'` means 0 characters).

- (10) The `*` format character serves as wildcard. For `pack()` it will
   append the corresponding byte argument string as-is, not applying any
   padding or zero filling. When a repeat count is given, that many bytes of
   the input byte string argument will be appended at most on `pack()`,
   effectively truncating longer input strings. For `unpack()`, the wildcard
   format will yield a byte string containing the entire remaining input data
   bytes, or - when a repeat count is given - that many bytes of input data
   at most.

- (11) The `X` format character handles hexadecimal encoding of binary data.
   On `pack()`, the argument is a hexadecimal string; with no repeat count the
   entire string is decoded into binary, while a repeat count limits the
   number of output bytes (truncating longer input). On `unpack()`, the input
   binary data is converted into a hexadecimal string, using all remaining
   bytes by default, or at most the specified number of bytes when a repeat
   count is given. Decoding accepts both upper- and lowercase hex digits, but
   encoding always produces lowercase output. The encoded text length is
   exactly twice the number of processed binary bytes.

- (12) The `Z` format character behaves like `X`, but uses base64 encoding
   instead of hexadecimal. On `pack()`, the argument is a base64 string; by
   default the entire string is decoded into binary, or at most the specified
   number of bytes when a repeat count is given. On `unpack()`, the input
   binary data is converted into a base64 string, consuming all remaining
   bytes by default, or at most the repeat count if given. The encoded base64
   string is approximately 1.4 times the size of the processed binary data.

A format character may be preceded by an integral repeat count.  For example,
the format string `'4h'` means exactly the same as `'hhhh'`.

Whitespace characters between formats are ignored; a count and its format
must not contain whitespace though.

When packing a value `x` using one of the integer formats (`'b'`,
`'B'`, `'h'`, `'H'`, `'i'`, `'I'`, `'l'`, `'L'`,
`'q'`, `'Q'`), if `x` is outside the valid range for that format, a type
error exception is raised.

For the `'?'` format character, the return value is either `true` or `false`.
When packing, the truish result value of the argument is used. Either 0 or 1
in the native or standard bool representation will be packed, and any
non-zero value will be `true` when unpacking.

## Examples

Note:
   Native byte order examples (designated by the `'@'` format prefix or
   lack of any prefix character) may not match what the reader's
   machine produces as
   that depends on the platform and compiler.

Pack and unpack integers of three different sizes, using big endian
ordering:

```ucode
import { pack, unpack } from 'struct';

pack(">bhl", 1, 2, 3);  // "\x01\x00\x02\x00\x00\x00\x03"
unpack(">bhl", "\x01\x00\x02\x00\x00\x00\x03");  // [ 1, 2, 3 ]
```

Attempt to pack an integer which is too large for the defined field:

```bash
$ ucode -lstruct -p 'struct.pack(">h", 99999)'
Type error: Format 'h' requires numeric argument between -32768 and 32767
In [-p argument], line 1, byte 24:

 `struct.pack(">h", 99999)`
  Near here -------------^
```

Demonstrate the difference between `'s'` and `'c'` format characters:

```ucode
import { pack } from 'struct';

pack("@ccc", "1", "2", "3");  // "123"
pack("@3s", "123");           // "123"
```

The ordering of format characters may have an impact on size in native
mode since padding is implicit. In standard mode, the user is
responsible for inserting any desired padding.

Note in the first `pack()` call below that three NUL bytes were added after
the packed `'#'` to align the following integer on a four-byte boundary.
In this example, the output was produced on a little endian machine:

```ucode
import { pack } from 'struct';

pack("@ci", "#", 0x12131415);  // "#\x00\x00\x00\x15\x14\x13\x12"
pack("@ic", 0x12131415, "#");  // "\x15\x14\x13\x12#"
```

The following format `'ih0i'` results in two pad bytes being added at the
end, assuming the platform's ints are aligned on 4-byte boundaries:

```ucode
import { pack } from 'struct';

pack("ih0i", 0x01010101, 0x0202);  // "\x01\x01\x01\x01\x02\x02\x00\x00"
```

Use the wildcard format to extract the remainder of the input data:

```ucode
import { unpack } from 'struct';

unpack("ccc*", "foobarbaz");   // [ "f", "o", "o", "barbaz" ]
unpack("ccc3*", "foobarbaz");  // [ "f", "o", "o", "bar" ]
```

Use the wildcard format to pack binary stings as-is into the result data:

```ucode
import { pack } from 'struct';

pack("h*h", 0x0101, "\x02\x00\x03", 0x0404);  // "\x01\x01\x02\x00\x03\x04\x04"
pack("c3*c", "a", "foobar", "c");  // "afooc"
```

### struct.pack(format, ...values) ⇒ `string`
Pack given values according to specified format.

The `pack()` function creates a byte string containing the argument values
packed according to the given format string.

Returns the packed string.

Raises a runtime exception if a given argument value does not match the
required type of the corresponding format string directive or if and invalid
format string is provided.

**Kind**: instance method of [`struct`](#module_struct)  

| Param | Type | Description |
| --- | --- | --- |
| format | `string` | The format string. |
| ...values | `\*` | Variable number of values to pack. |

**Example**  
```ucode
// Pack the values 1, 2, 3 as three consecutive unsigned int values
// in network byte order.
const data = pack('!III', 1, 2, 3);
```

### struct.unpack(format, input, [offset]) ⇒ `array`
Unpack given byte string according to specified format.

The `unpack()` function interpretes a byte string according to the given
format string and returns the resulting values. If the optional offset
argument is given, unpacking starts from this byte position within the input.
If not specified, the start offset defaults to `0`, the start of the given
input string.

Returns an array of unpacked values.

Raises a runtime exception if the format string is invalid or if an invalid
input string or offset value is given.

**Kind**: instance method of [`struct`](#module_struct)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| format | `string` |  | The format string. |
| input | `string` |  | The input string to unpack. |
| [offset] | `number` | `0` | The offset within the input string to start unpacking from. |

**Example**  
```ucode
// Unpack three consecutive unsigned int values in network byte order.
const numbers =
  unpack('!III', '\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03');
print(numbers, "\n"); // [ 1, 2, 3 ]
```

### struct.new(format) ⇒ [`instance`](#module_struct.instance)
Precompile format string.

The `new()` function precompiles the given format string argument and returns
a `struct` object instance useful for packing and unpacking multiple items
without having to recompute the internal format each time.

Returns an precompiled struct format instance.

Raises a runtime exception if the format string is invalid.

**Kind**: instance method of [`struct`](#module_struct)  

| Param | Type | Description |
| --- | --- | --- |
| format | `string` | The format string. |

**Example**  
```ucode
// Create a format of three consecutive unsigned int values in network byte order.
const fmt = struct.new('!III');
const buf = fmt.pack(1, 2, 3);  // "\x00\x00\x00\x01…"
print(fmt.unpack(buf), "\n");   // [ 1, 2, 3 ]
```

### struct.buffer([initialData]) ⇒ [`buffer`](#module_struct.buffer)
Creates a new struct buffer instance.

The `buffer()` function creates a new struct buffer object that can be used
for incremental packing and unpacking of binary data. If an initial data
string is provided, the buffer is initialized with this content.

Note that even when initial data is provided, the buffer position is always
set to zero. This design assumes that the primary intent when initializing
a buffer with data is to read (unpack) from the beginning. If you want to
append data to a pre-initialized buffer, you need to explicitly move the
position to the end, either by calling `end()` or by setting the position
manually with `pos()`.

Returns a new struct buffer instance.

**Kind**: instance method of [`struct`](#module_struct)  

| Param | Type | Description |
| --- | --- | --- |
| [initialData] | `string` | Optional initial data to populate the buffer with. |

**Example**  
```ucode
// Create an empty buffer
const emptyBuf = struct.buffer();

// Create a buffer with initial data
const dataBuf = struct.buffer("\x01\x02\x03\x04");

// Read from the beginning of the initialized buffer
const value = dataBuf.get('I');

// Append data to the initialized buffer
dataBuf.end().put('I', 5678);

// Alternative chained syntax for initializing and appending
const buf = struct.buffer("\x01\x02\x03\x04").end().put('I', 5678);
```

### struct.instance
**Kind**: static class of [`struct`](#module_struct)  
**See**: [new()](#module_struct+new)  

* [.instance](#module_struct.instance)
    * [.pack(...values)](#module_struct.instance+pack) ⇒ `string`
    * [.unpack(input, [offset])](#module_struct.instance+unpack) ⇒ `array`

#### instance.pack(...values) ⇒ `string`
Pack given values.

The `pack()` function creates a byte string containing the argument values
packed according to the given format instance.

Returns the packed string.

Raises a runtime exception if a given argument value does not match the
required type of the corresponding format string directive.

**Kind**: instance method of [`instance`](#module_struct.instance)  

| Param | Type | Description |
| --- | --- | --- |
| ...values | `\*` | Variable number of values to pack. |

**Example**  
```text
const fmt = struct.new(…);
const data = fmt.pack(…);
```

#### instance.unpack(input, [offset]) ⇒ `array`
Unpack given byte string.

The `unpack()` function interpretes a byte string according to the given
format instance and returns the resulting values. If the optional offset
argument is given, unpacking starts from this byte position within the input.
If not specified, the start offset defaults to `0`, the start of the given
input string.

Returns an array of unpacked values.

Raises a runtime exception if an invalid input string or offset value is
given.

**Kind**: instance method of [`instance`](#module_struct.instance)  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| input | `string` |  | The input string to unpack. |
| [offset] | `number` | `0` | The offset within the input string to start unpacking from. |

**Example**  
```text
const fmt = struct.new(…);
const values = fmt.unpack(…);
```

### struct.buffer
**Kind**: static class of [`struct`](#module_struct)  
**See**: [buffer()](#module_struct+buffer)  

* [.buffer](#module_struct.buffer)
    * [.pos([position])](#module_struct.buffer+pos) ⇒ `number` \| [`buffer`](#module_struct.buffer)
    * [.length([length])](#module_struct.buffer+length) ⇒ `number` \| [`buffer`](#module_struct.buffer)
    * [.start()](#module_struct.buffer+start) ⇒ [`buffer`](#module_struct.buffer)
    * [.end()](#module_struct.buffer+end) ⇒ [`buffer`](#module_struct.buffer)
    * [.put(format, ...values)](#module_struct.buffer+put) ⇒ [`buffer`](#module_struct.buffer)
    * [.get(format)](#module_struct.buffer+get) ⇒ `\*`
    * [.get(format)](#module_struct.buffer+get) ⇒ `array`
    * [.slice([start], [end])](#module_struct.buffer+slice) ⇒ `string`
    * [.set([value], [start], [end])](#module_struct.buffer+set) ⇒ [`buffer`](#module_struct.buffer)
    * [.pull()](#module_struct.buffer+pull) ⇒ `string`

#### buffer.pos([position]) ⇒ `number` \| [`buffer`](#module_struct.buffer)
Get or set the current position in the buffer.

If called without arguments, returns the current position.
If called with a position argument, sets the current position to that value.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: `number` \| [`buffer`](#module_struct.buffer) - If called without arguments, returns the current position.
If called with a position argument, returns the buffer instance for chaining.  

| Param | Type | Description |
| --- | --- | --- |
| [position] | `number` | The position to set. If omitted, the current position is returned. |

**Example**  
```ucode
const currentPos = buf.pos();
buf.pos(10);  // Set position to 10
```

#### buffer.length([length]) ⇒ `number` \| [`buffer`](#module_struct.buffer)
Get or set the current buffer length.

If called without arguments, returns the current length of the buffer.
If called with a length argument, sets the buffer length to that value,
padding the data with trailing zero bytes or truncating it depending on
whether the updated length is larger or smaller than the current length
respectively.

In case the updated length is smaller than the current buffer offset, the
position is updated accordingly, so that it points to the new end of the
truncated buffer data.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: `number` \| [`buffer`](#module_struct.buffer) - If called without arguments, returns the current length.
If called with a length argument, returns the buffer instance for chaining.  

| Param | Type | Description |
| --- | --- | --- |
| [length] | `number` | The length to set. If omitted, the current length is returned. |

**Example**  
```ucode
const buf = struct.buffer("abc"); // Initialize buffer with three bytes
const currentLen = buf.length();  // Returns 3

buf.length(6);                    // Extend to 6 bytes
buf.slice();                      // Trailing null bytes: "abc\x00\x00\x00"

buf.length(2);                    // Truncate to 2 bytes
buf.slice();                      // Truncated data: "ab"
```

#### buffer.start() ⇒ [`buffer`](#module_struct.buffer)
Set the buffer position to the start (0).

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: [`buffer`](#module_struct.buffer) - The buffer instance.  
**Example**  
```ucode
buf.start();
```

#### buffer.end() ⇒ [`buffer`](#module_struct.buffer)
Set the buffer position to the end.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: [`buffer`](#module_struct.buffer) - The buffer instance.  
**Example**  
```ucode
buf.end();
```

#### buffer.put(format, ...values) ⇒ [`buffer`](#module_struct.buffer)
Pack data into the buffer at the current position.

The `put()` function packs the given values into the buffer according to
the specified format string, starting at the current buffer position.
The format string follows the same syntax as used in `struct.pack()`.

For a detailed explanation of the format string syntax, refer to the
["Format Strings" section](#module_struct) in the module
documentation.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: [`buffer`](#module_struct.buffer) - The buffer instance.  
**See**: [struct.pack()](#module_struct+pack)  

| Param | Type | Description |
| --- | --- | --- |
| format | `string` | The format string specifying how to pack the data. |
| ...values | `\*` | The values to pack into the buffer. |

**Example**  
```ucode
buf.put('II', 1234, 5678);
```

#### buffer.get(format) ⇒ `\*`
Unpack a single value from the buffer at the current position.

The `get()` function unpacks a single value from the buffer according to the
specified format string, starting at the current buffer position.
The format string follows the same syntax as used in `struct.unpack()`.

For a detailed explanation of the format string syntax, refer to the
["Format Strings" section](#module_struct) in the module documentation.

Alternatively, `get()` accepts a postive or negative integer as format, which
specifies the length of a string to unpack before or after the current
position. Negative values extract that many bytes before the current offset
while postive ones extracts that many bytes after.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: `\*` - The unpacked value.  
**See**: [struct.unpack()](#module_struct+unpack)  

| Param | Type | Description |
| --- | --- | --- |
| format | `string` \| `number` | The format string specifying how to unpack the data. |

**Example**  
```ucode
const val = buf.get('I');
const str = buf.get(5);    // equivalent to buf.get('5s')
const str = buf.get(-3);   // equivalent to buf.pos(buf.pos() - 3).get('3s')
```

#### buffer.get(format) ⇒ `array`
Unpack multiple values from the buffer at the current position.

The `read()` function unpacks multiple values from the buffer according to
the specified format string, starting at the current buffer position.
The format string follows the same syntax as used in `struct.unpack()`.

For a detailed explanation of the format string syntax, refer to the
["Format Strings" section](#module_struct) in the module documentation.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: `array` - An array containing the unpacked values.  
**See**: [struct.unpack()](#module_struct+unpack)  

| Param | Type | Description |
| --- | --- | --- |
| format | `string` | The format string specifying how to unpack the data. |

**Example**  
```ucode
const values = buf.get('II');
```

#### buffer.slice([start], [end]) ⇒ `string`
Extract a slice of the buffer content.

The `slice()` function returns a substring of the buffer content
between the specified start and end positions.

Both the start and end position values may be negative, in which case they're
relative to the end of the buffer, e.g. `slice(-3)` will extract the last
three bytes of data.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: `string` - A string containing the specified slice of the buffer content.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [start] | `number` | `0` | The starting position of the slice. |
| [end] | `number` | `buffer.length()` | The ending position of the slice (exclusive). |

**Example**  
```ucode
const slice = buf.slice(4, 8);
```

#### buffer.set([value], [start], [end]) ⇒ [`buffer`](#module_struct.buffer)
Set a slice of the buffer content to given byte value.

The `set()` function overwrites a substring of the buffer content with the
given byte value, similar to the C `memset()` function, between the specified
start and end positions.

Both the start and end position values may be negative, in which case they're
relative to the end of the buffer, e.g. `set(0, -2)` will overwrite the last
two bytes of data with `\x00`.

When the start or end positions are beyond the current buffer length, the
buffer is grown accordingly.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: [`buffer`](#module_struct.buffer) - The buffer instance.  

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| [value] | `number` \| `string` | `0` | The byte value to use when overwriting buffer contents. When a string is given, the first character is used as value. |
| [start] | `number` | `0` | The position to start overwriting from. |
| [end] | `number` | `buffer.length()` | The position to end overwriting (exclusive). |

**Example**  
```ucode
const buf = struct.buffer("abcde");
buf.set("X", 2, 4).slice();  // Buffer content is now "abXXe"
buf.set().slice();           // Buffer content is now "\x00\x00\x00\x00\x00"
```

#### buffer.pull() ⇒ `string`
Extract and remove all content from the buffer.

The `pull()` function returns all content of the buffer as a string
and resets the buffer to an empty state.

**Kind**: instance method of [`buffer`](#module_struct.buffer)  
**Returns**: `string` - A string containing all the buffer content.  
**Example**  
```ucode
const allData = buf.pull();
```

---

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
