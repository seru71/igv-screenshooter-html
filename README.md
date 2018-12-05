# IGV-screenshooter

A simple script that takes an <interactive screenshot> of a given interval of a BAM.
Slice of the BAM is saved in the HTML file making it self-contained.

IGV.js is used for interactive visualization.
The igv.min.js file is taken from the [igv.js](https://github.com/igvteam/igv.js) repo maintained by the [igvteam](https://github.com/igvteam).

## Usage
```
./shoot.py --help
usage: shoot.py [-h] [--genome {hg19,hg38}]
                contig start end html bam [bam ...]

positional arguments:
  contig                Chromosome/contig of the interval to visualize
  start                 Start position of the interval to visualize
  end                   End position of the interval to visualize
  html                  Output HTML with IGV visualization
  bam                   Input BAM. Can be specified multiple times

optional arguments:
  -h, --help            show this help message and exit
  --genome {hg19,hg38}  Genome build to use. Default: hg38
```
