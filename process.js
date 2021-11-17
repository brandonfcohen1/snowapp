var fs = require("fs"),
  xml2js = require("xml2js");

var parser = new xml2js.Parser();
fs.readFile("./nohrsc_nsm_20211115.kml", function (err, data) {
  parser.parseString(data, function (err, result) {
    const res = result.kml.Document[0].Folder;
    const snowDepth = res.filter((n) => n.name == "Snow Depth")[0];
    const legend = snowDepth.ScreenOverlay.filter((n) => n.name == "legend");
    const tiles = snowDepth.GroundOverlay;

    let leafletPrep = [];

    for (let tile of tiles) {
      const href = tile.Icon[0].href;
      const bounds = [
        [tile.LatLonBox[0].north[0], tile.LatLonBox[0].east[0]],
        [tile.LatLonBox[0].south[0], tile.LatLonBox[0].west[0]],
      ];

      leafletPrep.push({ href: href, bounds: bounds });
    }

    console.log(leafletPrep);
    fs.writeFile(
      "leafletPrep.json",
      JSON.stringify(leafletPrep),
      "utf8",
      function (err) {
        if (err) throw err;
        console.log("complete");
      }
    );
  });
});
