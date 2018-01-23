# PIM_Mini_Tests

Python version: Python 2.7

## Test Harness

Boolean values stored inside `settings.py` are used to indicate whether a test will be run.
It is assumed that the following directories are already on the target device:

| Source directory | Target device directory |
| ---------------- | ----------------------- |
| `/leds`          | `/leds`                 |
| `/comms`         | `/comms`                |
| `/user_inputs`   | `/user_inputs`          |

The `*_controller.py` files start a deamon on the target via SSH, which listens to commands sent
in order to run tests. After 30 minutes of inactivity the daemons will stop. The daemons will also stop
after the tests have completed executing.

## Licenses

### python-periphery

GitHub repo: [https://github.com/vsergeev/python-periphery](https://github.com/vsergeev/python-periphery)

 Copyright (c) 2015-2016 vsergeev / Ivan (Vanya) A. Sergeev

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
