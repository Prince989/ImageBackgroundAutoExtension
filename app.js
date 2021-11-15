const express = require("express");
const app = express();
const cors = require("cors");
var fileUpload = require("express-fileupload");
const fs = require("fs");
const http = require("http");
const axios = require("axios");
const port = 9092;
const fileOriginPath = "E:/ImageSizeHandler/public/reqs/";
const { exec } = require("child_process");
const { stderr, stdout } = require("process");

var req_id = 0;

let options = {
    redirect: false
}
app.use(express.static('public', options));
app.use(cors());
app.use(express.json());
app.use(
  fileUpload({
    useTempFiles: true,
    tempFileDir: "/tmp/",
  })
);

app.post("/api/fix", fix);

function fix(req, res) {
  req_id++;
  let tReq = req_id;
  console.log(`This is request number : ${tReq}`);
  let url = req.body.url;
  let width = req.body.width;
  let height = req.body.height;
  let imagePath = `${fileOriginPath}/${tReq}.png`;
  try {
    axios({
      method: "get",
      url: url,
      responseType: "stream",
    }).then(function (response) {
      response.data.pipe(
        fs.createWriteStream(imagePath)
      );
      let cmd = `python "E:/ImageSizeHandler/sizeFixer.py" "${fileOriginPath}" ${tReq} ${width} ${height} `
      execute(cmd,(err,succ) => {
          if(err){
              console.log(err);
              return res.json({
                  Message : err
              })
          }
          return res.json({
              url : `http://192.168.10.120:9092/reqs/${tReq}_export.png`
          })
      })
    });
  } catch (e) {
    console.log(e);
    return res.json({
      Message: e,
    });
  }

  /*   img.mv(imagePath, (err) => {
    if (err) {
      console.log(err);
      return res.json({
        Message: err,
      });
    }
    return res.json({
      Message: "File Saved!",
    });
  }); */
}

function execute(cmd, callback) {
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.log(error);
      callback(error, null);
      return;
    }
    if (stderr) {
      console.log(stderr);
      callback(stderr, null);
      return;
    }
    console.log(stdout);
    callback(null, 1);
  });
}

app.listen(port, () => {
  console.log("Listening on port: " + port);
});
