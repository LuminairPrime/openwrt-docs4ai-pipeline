---
title: 'ucode module: math'
module: ucode
origin_type: c_source
token_count: 8716
source_file: L1-raw/ucode/c_source-api-module-math.md
last_pipeline_run: '2026-07-01T13:51:57.973723+00:00'
source_commit: unknown
source_url: https://github.com/nicowillis/ucode/blob/unknown/lib/math.c
source_locator: lib/math.c
language: c
ai_summary: Provides standard mathematical functions for ucode scripts, mirroring the JavaScript Math object surface. Implements abs(), atan2(), ceil(), cos(), exp(), floor(), log(), max(), min(), pow(), round(), sin(), sqrt(), and tan() along with the constants math.PI and math.E for floating-point arithmetic.
ai_when_to_use: Use for numerical calculations in LuCI view scripts, configuration validators, and network metric processors that need floating-point math beyond basic arithmetic operators available in ucode natively.
ai_related_topics:
- math.floor
- math.ceil
- math.abs
- math.sqrt
- math.pow
- math.round
---

> **Source:** [https://github.com/nicowillis/ucode/blob/unknown/lib/math.c](https://github.com/nicowillis/ucode/blob/unknown/lib/math.c)
> **Kind:** c_source | **Commit:** unknown | **Method:** normalized
> **Normalized:** 2026-07-01

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
