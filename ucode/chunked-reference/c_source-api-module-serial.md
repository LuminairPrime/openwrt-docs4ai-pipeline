---
title: 'ucode module: serial'
module: ucode
origin_type: c_source
token_count: 6700
source_file: L1-raw/ucode/c_source-api-module-serial.md
last_pipeline_run: '2026-11-01T18:17:43.472245+00:00'
source_commit: unknown
source_url: https://github.com/nicowillis/ucode/blob/unknown/lib/serial.c
source_locator: lib/serial.c
language: c
---

> **Source:** [https://github.com/nicowillis/ucode/blob/unknown/lib/serial.c](https://github.com/nicowillis/ucode/blob/unknown/lib/serial.c)
> **Kind:** c_source | **Commit:** unknown | **Method:** normalized
> **Normalized:** 2026-11-01

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
