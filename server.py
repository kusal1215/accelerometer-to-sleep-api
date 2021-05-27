from flask import *  
from analyze_sleep import *
from json2html import *



app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return '''

<!DOCTYPE html>
<html>
<head>
    <title>SLEEP ANALYZE</title>


<link href="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">
	

    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
@media (max-width: 767px){h1{font-size:30px;font-size:8vw}div#links{margin-top:2em;margin-bottom:1em}div.help_links{margin-top:-1em}.alert{max-width:75%;display:inline-block;margin:0.8em 0 0.5em;padding:0.3em}.form-inline{max-width:75%}input#submit{margin-top:0.5em}}@media (min-width: 768px){div #links{margin-top:2.5em;margin-bottom:3em}div.help_links{margin-top:-1em}.alert{max-width:330px;display:inline-block;margin:1em 0 0.5em;padding:0.3em}}@media (min-width: 992px){.vertical-align{display:flex;align-items:center;justify-content:center}}ul{list-style-type:none;padding:0;margin:0}#browsebutton{background-color:white}#my-file-selector{display:none}
</style>

    </head>

<body>
<div class="container-fluid">
<center>
<h2>Sleep Analyze With Accelerometer Data</h2>
</center>
  


<div class="row">
    <form class="form-inline center-block" action="/analyze" method="POST" enctype="multipart/form-data">
        <div style="display:none;"><input id="csrf_token" name="csrf_token" type="hidden" value="1622068751##84c919d6d3b037f53f5db8405f8e4a09b7b78693"></div>
        <div class="input-group">
            <label id="browsebutton" class="btn btn-default input-group-addon" for="my-file-selector">
                <input id="my-file-selector" name="file" type="file">
                Browse...
            </label>
            <input type="text" class="form-control" readonly>
        </div>
        <center>
        <input class="btn btn-primary" id="submit" name="submit" type="submit" value="Analyze">         
        </center>
    </form>
</div>




</div>


<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.5/js/bootstrap.min.js"></script>
		


<script>
$(document).on('change', '#browsebutton :file', function() {
  var input = $(this),
      numFiles = input.get(0).files ? input.get(0).files.length : 1,
      label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
  input.trigger('fileselect', [numFiles, label]);
});

$(document).ready( function() {
    $('#browsebutton :file').on('fileselect', function(event, numFiles, label) {
        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

        if( input.length ) {
            input.val(log);
        } else {
            if( log ) alert(log);
        }

    });
});
</script>



</body>
</html>

    '''


html_r = '''
<html>
<head>
<title>Analyzed File Result</title>
      <meta name = "viewport" content = "width = device-width, initial-scale = 1">      
      <link rel = "stylesheet"
         href = "https://fonts.googleapis.com/icon?family=Material+Icons">
      <link rel = "stylesheet"
         href = "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/css/materialize.min.css">
      <script type = "text/javascript"
         src = "https://code.jquery.com/jquery-2.1.1.min.js"></script>           
      <script src = "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.3/js/materialize.min.js">
      </script>             
      
</head>
<center>
<body>
<h1> Result </h1>
{}
</body>
</center>
</html>

'''





 
@app.route('/analyze', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
      f = request.files['file']  
      if f.filename.split('.')[-1] in ['CSV','csv']:
        f.save(f.filename)  
        return html_r.format(json2html.convert(json = analyze(f.filename)))
      else:
        return 'invalid file format ! '

  
if __name__ == '__main__':  
    app.run(debug = True,port=3004)  
