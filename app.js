const {PythonShell} = require('python-shell');
const fileUpload = require("express-fileupload");
const express = require("express");
const fs = require("fs");
const app = express();


app.use(fileUpload());

app.get("/", function(req, res) {
  console.log("\n\nUser connectedDDDDDD\n\n");
  res.sendFile( __dirname + "/UI/index.html");
});

app.post("/upload", function(req, res) {
  console.log("\n\nPDF uploaded\n\n");
  let sampleFile = req.files.sampleFile;
  console.log("\n\nFile: " + sampleFile + "\n\n");
  var uploadPath =  __dirname + '/uploads/' + sampleFile.name;
  console.log("\n\nUPLOAD PATH: " + uploadPath + "\n\n");

  sampleFile.mv(uploadPath, function(err) {
    if (err) {
      console.log("\n\nsampleFile.mv error\n\n");
    }
    let options = {
      args: [uploadPath]
    };
    PythonShell.run('rotate.py', options, function(err) {
      if (err) {
        console.log("\n\nPythonShell rotate error\n\n");
      }
      console.log('finished');

      var data =fs.readFileSync(__dirname + '/rotate.'+sampleFile.name);
      res.contentType("application/pdf");
      console.log("\n\nSetting content type header and sending\n\n");
      res.send(data);
      console.log("\n\nSent\n\n");
    });
  });



});


app.listen(process.env.PORT || 8080);
