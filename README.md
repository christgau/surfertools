# Surfer Tools

Small self-contained, Python-based tools to work with Surfer Grid (sfg, grd) data files.
Both binary and text grid files are supported.

## Limitations

The scripts only processes two-dimensional data.
Only Surfer 6 grid files are supported.

## Grid to Pixmap Conversion (sfg2ppm)

Converts a grid file to a binary Portable Pixmap file format (ppm), optionally using a color palette.
The logarithm (base 10) of the data can be computed before the conversion takes place.
Further, the (logarithmic) data can be normalized, i.e. values will be between 0 and 1 before the actual pixmap conversion.
The conversion uses a gray scale by default.
A color palette file can be specified as well which is a ascii simple format that contains multiple rows of

```
low high r_start g_start b_start r_end g_end b_end
```

Where `low` and `high` are (inclusive) boundaries and the two rgb triples define the colors for the given range.
Linear interpolation between the start and end colors is applied for a value that is within the interval [low, high].
The rgb triples may be integers or float.
In case all of the color values includes are below 255, all color values are scaled into that range.

An example invocation looks like this

```
sfg2ppm -l -n -p color.palette input.grd > output.ppm
```

## Compute Difference Between Grids (sfgdelta)

Compute the difference between all data points in two grid files.
The grids in the file may be shifted against each other using the `dx` and `dy` option.
The maximum relative delta, the number of point above a fixed absolute delta threshold (0.0) and the values of the points with the largest delta are reported.
Additionally, the maximum and minimum values of the two input grids are reported

An example invocation looks like this

```
sfgdelta -dx 32 -dy -64 input1.grd input2.grd
```

## Resources

- [Surfer 6 Text Grid File Format](https://surferhelp.goldensoftware.com/topics/ascii_grid_file_format.htm)
- [Surfer 6 Text Binary File Format](https://surferhelp.goldensoftware.com/topics/surfer_6_grid_file_format.htm)
