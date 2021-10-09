---

name: Bug Report
about: Create a bug report to help us improve piso
title: "BUG:"
labels: "Bug"

---

- [ ] I have checked that this issue has not already been reported.

- [ ] I have confirmed this bug exists on the latest version of piso.

---

**Note**: Please read [this guide](https://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports) detailing how to provide the necessary information for us to reproduce your bug.

#### Code Sample, a copy-pastable example

```python
# Your code here

```

#### Problem description

[this should explain **why** the current behaviour is a problem and why the expected output is a better solution]

#### Expected Output

#### Dependency Versions``

Please run the following code:

```python
import piso
import staircase
import pandas
import numpy

for pkg in (piso, staircase, pandas, numpy):
    print(pkg.__name__, pkg.__version__)
```

<details>

[paste the output here leaving a blank line after the details tag]

</details>
