# Tips for programming python
[Python Data Structure Tutorial](https://docs.python.org/2/tutorial/datastructures.html)

1. Use **xrange()** instead of range() for looping over large amount of data
2. **List Comprehension**
```python
  >>> [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
  [(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
```
```python
  >>>{x: x**2 for x in (2, 4, 6)}
  {2: 4, 4: 16, 6: 36}
```
```python
  >>>vec = [[1,2,3], [4,5,6], [7,8,9]]
  >>>[num for elem in vec for num in elem]
  [1, 2, 3, 4, 5, 6, 7, 8, 9]
```
```python
  >>>f = open(r"temp.txt")
  >>>[[c for c in line] for line in f]
```

3. ```inspect```, an easy way to look at interface of functions
```
  >>> import re
  >>> import inspect
  >>> print inspect.getsource(re.compile)
  def compile(pattern, flags=0):
      "Compile a regular expression pattern, returning a pattern object."
      return _compile(pattern, flags)
```
