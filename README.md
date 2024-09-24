# uwledclient

uwledclient is a MicropPython library to interact with the [WLED JSON API](https://kno.wled.ge/interfaces/json-api/).

## Installation

Use the package manager [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip) to install uwledclient.

```python
>>> import mip
>>> mip.install('github:spierepf/uwledclient')
```

## Usage

```python
from uwledclient import WLEDNode

# Instantiate a wled node using its IP address
node = WLEDNode("http://4.3.2.1")

# or instantiate it using its mDNS name
node = WLEDNode("http://wled.local")

# then we can make all the LEDs on that node solid green
node.update().fx("Solid").col([[0, 255, 0]]).next().done()

# or perhaps have a few different segments doing different things:
node.update()\
    .length(16).fx("Pride 2015").next()\
    .length(16).pal("Aurora").fx("Aurora").next()\
    .length(16).pal("Magenta").fx("Dancing Shadows").next()\
    .length(16).col([[255,0,0]]).fx("Chunchun").next()\
    .done()
```

## Basics

Any of the JSON keys listed in the [Contents of the segment object](https://kno.wled.ge/interfaces/json-api/#contents-of-the-segment-object) table can be used as
method names.

The keys `start`, and `stop` are managed internally by this library.

You'll notice that `fx` and `pal` use a name lookup to determine the correct effect or
palette id. These methods can also use the `~`, `~-`, and `r` options as described in
the WLED documentation.

The `next()` method is used to commit the current segment and begin a new one.

The `length(n)` method determines the number of LEDs to assign to the current
segment. A segment without a `length(n)` call will use all remaining LEDs of the node.

Calling the `done()` method actually sends the request to the WLED node.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)