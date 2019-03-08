#!/usr/bin/env python3

import base64, gzip
import pysam
import os
    
    
def b64encode_bam(bam_file):
    with open(bam_file, 'rb') as f:
        return base64.b64encode(f.read())


def slice_bam(input_bam, output_bam, contig, start, end):
    
    with pysam.AlignmentFile(input_bam, "rb") as input_bam,\
         pysam.AlignmentFile(output_bam, "wb", template=input_bam) as sliced_bam:
        
        for read in input_bam.fetch(contig, start, end):
            sliced_bam.write(read)
    
    
def get_track_code(bam_path, contig, start, end, remove_tmp_bam=True, tmp_dir='/tmp'):
    
    track_template =  """
       url: "data:application/gzip;base64,{data}",
       name: "%s",
       height: 500,
       indexed: false,
       type: "alignment"
    """ % os.path.basename(bam_path)
    
    # name of the output/ BAM
    sliced_bam_path = os.path.join(tmp_dir, 
                                   os.path.basename(bam_path)[:-len('bam')] + \
                                  '_'.join([contig, str(start), str(end)]) + '.bam')
                      
    # extract a section of the BAM
    slice_bam(bam_path, sliced_bam_path, contig, start, end)
    
    # encode the file in base64
    bam_slice_b64 = b64encode_bam(sliced_bam_path).decode("utf-8")
    
    if remove_tmp_bam:
        os.remove(sliced_bam_path)

    return track_template.format(data=bam_slice_b64)



def get_igv_code(bams, contig, start, end, genome_build):
           
    code = """

        <div id="igvDiv" style="padding-top: 10px;padding-bottom: 10px; border:1px solid lightgray"></div>
        <script type="text/javascript">
                 
            document.addEventListener("DOMContentLoaded", function () {
            
                    const igvDiv = document.getElementById("igvDiv");
            
                    const options = { 
                        genome: "%s",
                        locus: "%s",
                        tracks: [{%s}]
                    };
                    
                    igv.createBrowser(igvDiv, options);
                    
                });
                
        </script>
    """

    coords = contig+':'+str(start)+'-'+str(end)
    tracks = "},\n{".join([get_track_code(bam, contig, start, end) for bam in bams])
        
    return code % (genome_build, coords, tracks)
            

def get_head():
    template="""
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
        <meta name="description" content="">
        <meta name="author" content="">
        <script>{igv_js}</script>
    """
    # alternatively: <script src="https://igv.org/web/release/2.1.0/dist/igv.min.js"></script>
    
    with open('igv.min.js','r') as f:
        return template.format(igv_js=f.read())
        
    
    
            
def get_screenshot_html(bams, contig, start, end, genome_build):

    return """<!DOCTYPE html><html lang="en">{head}<body>{content}</body></html>""" \
            .format(head = get_head(), 
                    content = get_igv_code(bams, contig, start, end, genome_build))
    
    


if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--genome", choices=['hg19','hg38'], default='hg38', help='Genome build to use. Default: %(default)s')
    parser.add_argument("contig", help='Chromosome/contig of the interval to visualize')
    parser.add_argument("start", help='Start position of the interval to visualize', type=int)
    parser.add_argument("end", help='End position of the interval to visualize', type=int)
    parser.add_argument("html", help='Output HTML with IGV visualization')
    parser.add_argument("bam", nargs='+', help='Input BAM. Can be specified multiple times')

    args = parser.parse_args()

    # e.g. chr2 10183665 10204021
    
    with open(args.html, 'w') as out:
        out.write(get_screenshot_html(args.bam,
                                      args.contig,
                                      args.start, 
                                      args.end, 
                                      args.genome))
                  
    




