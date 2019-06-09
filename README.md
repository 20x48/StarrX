# StarrX #

**It is just an esolang! Let's writing the code that just like starry sky!**

[中文](./README_CN.md)

## Some Simple Demos ##

### Hello, world! ###

#### Code ####

```
   * "Hello, world! " .
```

#### Output ###

```
Hello, world!
```

### Output from 0 to 99 ###

#### Code ####

```
   * 100   * 0   * 1 ' * * *  * .  + *  *   +     * ^
```

#### Output ####

```
0
1
2
...
98
99
```

### Fibonacci Sequence ###

#### Code ####

```
 ,   * 1   * 0 ' * * *  * .     *  * *  +  * *      * *  *    * * *   * 1  *  *   +     * * * *  *      * ^
```

#### Input ####

```
10
```

#### Output ####

```
1
1
2
...
21
34
55
```

## Grammar ##

### Agreement ###

* Use `pointer` to determine the element's `insert`, `swap`, `copy` and `delete`.
* `pointer` will move with the operation of the element.
* The number of spaces before each symbol cannot be 0.
* There must be at least 1 space before any number.
* Of course, this is not necessary in strings, and extra spaces will be preserved.
* Usage of the interpreter: `StarrX.py <file>`

### Usage of Symbols ###

#### Symbol **\*** ####

This symbol is used to manipulate the `pointer` and some related elements read and write.

|Opcode 1|Opcode 2|Meaning|
|:-:|:-:|:--|
|3|/|`insert` element, the following should be `integer`, `float` or `string`.|
|4|/|Swap the element which pointed by `pointer` with the element which at `tail`.|
|5|/|Copy the element which pointed by `pointer` to `tail`.|
|6|/|`delete` the element pointed by the pointer.|
|1|1|Move `pointer` to `tail`.|
|2|1|Move `pointer` towards `tail` for one bit.|
|1|2|Move `pointer` towards `head` for one bit.|
|2|2|Move `pointer` to `head`.|

#### Symbol **+** ####

This symbol is used for arithmetic operations and rounding.

The element pointed to by `pointer` will be used as the first parameter, and the element at `tail` will be used as the second parameter (if needed).

Note that the result of the operation will be stored to the location where the first parameter is located (i.e. : the element pointed by `pointer`).

|Opcode 1|Opcode 2|Meaning|
|:-:|:-:|:--|
|2|/|addition (+)|
|3|/|subtraction (-)|
|4|/|multiplication (\*)|
|5|/|division (/)|
|6|/|mod (%)|
|7|/|power (^)|
|1|1|round-down (floor)|
|1|2|round|
|1|3|round-up (ceil)|

#### Symbol **-** ####

This symbol is used for relational operations.

The element pointed to by `pointer` will be used as the first parameter, and the element at `tail` will be used as the second parameter.

The result of the operation is 0 or 1, and it will be stored to `tail`.

|Opcode 1|Opcode 2|Meaning|
|:-:|:-:|:--|
|1|2|Less than (<)|
|1|3|Less than or equal to (<=)|
|2|1|Larger than (>)|
|3|1|Larger than or equal to (>=)|
|1|1|Equal (==)|
|2|2|Non-equal (!=)|

#### Symbol **"** ####

This symbol is used to represent a string. Appears after the "`insert` element" operation.

This symbol appears with N (N>0) spaces to indicate the beginning of the string. Use the same N spaces and a `"` symbol to ending a string.

#### Symbol **,** ####

This symbol is used to write the input to the location pointed by `pointer`.

|Opcode|Meaning|
|:-:|:--|
|1|Line feed after output.|
|2|Output without line feed.|

#### Symbol **'** ####

This symbol appears with N (N>0) spaces, used to create `tag N`.

#### Symbol **^** ####

This symbol appears with N (N>0) spaces.

The element at `tail` will be popped up and judged: if it is not 0, then `jump` to `tag N`.

It should be noted that `tag N` must be defined before `jump`. Also, newly defined `tag` with the same N value will overwrite the old `tag`.

#### Symbol **\`** ####

This symbol is used to `undo` the movement of  `pointer`.

Since `undo` is also a pointer movement, it is meaningless to `undo` all the time.

