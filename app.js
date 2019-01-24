const {PythonShell} = require('python-shell');
const fileUpload = require("express-fileupload");
const express = require("express");
const fs = require("fs");
const app = express();


app.use(fileUpload());

app.get("/", function(req, res) {
  res.sendFile(__dirname + "/UI/index.html");
});

app.post("/upload", function(req, res) {
  let sampleFile = req.files.sampleFile;
  var uploadPath = __dirname + '/uploads/' + sampleFile.name;

  sampleFile.mv(uploadPath, function(err) {
    if (err) return res.status(500).send(err);
    let options = {
      args: [uploadPath]
    };
    PythonShell.run('rotate.py', options, function(err) {
      if (err) throw err;
      console.log('finished');
    });
  });

  var data =fs.readFileSync(__dirname + '/rotate.'+sampleFile.name);
  res.contentType("application/pdf");
  res.send(data);

});


app.listen(process.env.PORT || 8080);
