// express
const express = require("express");
const PORT = process.env.PORT || 3001;
const path = require("path");
const app = express();
let ejs = require("ejs");

app.get("/", function (req, res) {
  res.sendFile(path.join(__dirname + "/leafletkmz.html"));
});

app.get('/',function(req,res){
  var title = "PERFORMANCE OVERVIEW";
  res.render('leafletkmz.html',{name:title});
})

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`, "0.0.0.0");
});
