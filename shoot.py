#!/usr/bin/env python3

import base64, gzip
import pysam
    
    
def b64encode_bam(bam_file):
    with open(bam_file, 'rb') as f:
        return base64.b64encode(f.read())


def slice_bam(input_bam, output_bam, contig, start, end):
    
    with pysam.AlignmentFile(input_bam, "rb") as input_bam,\
         pysam.AlignmentFile(output_bam, "wb", template=input_bam) as sliced_bam:
        
        for read in input_bam.fetch(contig, start, end):
            sliced_bam.write(read)
    

def get_igv_code(bam_path, contig, start, end):
    
    # name of the output/ BAM
    sliced_bam_path = bam_path[:-len('bam')] + \
                      '_'.join([contig, str(start), str(end)]) + '.bam'
                      
    # extract a section of the BAM
    slice_bam(bam_path, sliced_bam_path, contig, start, end)
    
    # encode the file in base64
    bam_slice_b64 = b64encode_bam(sliced_bam_path)
    
    coords = contig+':'+str(start)+'-'+str(end)

    code = """

        <div id="igvDiv" style="padding-top: 10px;padding-bottom: 10px; border:1px solid lightgray"></div>
        <script type="text/javascript">
                 
            document.addEventListener("DOMContentLoaded", function () {
            
                    const igvDiv = document.getElementById("igvDiv");
            
                    const options = { 
                        genome: "hg19",
                        locus: "%s",
                        tracks: [{
                            url: "data:application/gzip;base64,%s",
                            name: "sample id",
                            height: 500,
                            indexed: false,
                            type: "alignment"
                        }]
                    };
                    
                    igv.createBrowser(igvDiv, options);
                    
                });
                
        </script>
    """
    
    return code % (coords, bam_slice_b64.decode("utf-8"))
            

def get_head():
    return """
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <meta name="description" content="">
        <meta name="author" content="">
        <script src="igv.min.js"></script>
    """
    # alternatively: <script src="https://igv.org/web/release/2.1.0/dist/igv.min.js"></script>
    
            
def get_screenshot_html(bam, contig, start, end):

    return """<!DOCTYPE html><html lang="en">{head}<body>{content}</body></html>""" \
            .format(head = get_head(), 
                    content = get_igv_code(bam, contig, start, end))
    
    


if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.parse_args()
    
    print(get_screenshot_html('test.bam', 'chr2', 10183665, 10204021))