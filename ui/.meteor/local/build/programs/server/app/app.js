var require = meteorInstall({"server":{"en-server.js":function(){

///////////////////////////////////////////////////////////////////////
//                                                                   //
// server/en-server.js                                               //
//                                                                   //
///////////////////////////////////////////////////////////////////////
                                                                     //
Meteor.methods({                                                     // 1
    'runSimulation': function () {                                   // 2
        var syncHTTP = Meteor.wrapAsync(HTTP.get);                   // 3
        var url = "http://127.0.0.1:5000/";                          // 4
        var result = syncHTTP(url, {});                              // 5
        console.log(result);                                         // 6
        return result.content; // return JSON.parse(result.content);
    }                                                                // 9
});                                                                  // 1
///////////////////////////////////////////////////////////////////////

},"main.js":function(require,exports,module){

///////////////////////////////////////////////////////////////////////
//                                                                   //
// server/main.js                                                    //
//                                                                   //
///////////////////////////////////////////////////////////////////////
                                                                     //
var Meteor = void 0;                                                 // 1
module.watch(require("meteor/meteor"), {                             // 1
  Meteor: function (v) {                                             // 1
    Meteor = v;                                                      // 1
  }                                                                  // 1
}, 0);                                                               // 1
Meteor.startup(function () {// code to run on server at startup      // 3
});                                                                  // 5
///////////////////////////////////////////////////////////////////////

}}},{
  "extensions": [
    ".js",
    ".json"
  ]
});
require("./server/en-server.js");
require("./server/main.js");
//# sourceMappingURL=app.js.map
