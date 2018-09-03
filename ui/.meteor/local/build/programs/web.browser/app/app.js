var require = meteorInstall({"client":{"main.html":function(require,exports,module){

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                              //
// client/main.html                                                                                             //
//                                                                                                              //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                //
module.exports = require("./template.main.js");                                                                 // 1
                                                                                                                // 2
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

},"template.main.js":function(){

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                              //
// client/template.main.js                                                                                      //
//                                                                                                              //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                //
                                                                                                                // 1
Template.body.addContent((function() {                                                                          // 2
  var view = this;                                                                                              // 3
  return [ HTML.Raw("<h1>Embedded Network Model</h1>\n\n    "), HTML.DIV({                                      // 4
    class: "page-content"                                                                                       // 5
  }, "\n      ", HTML.DIV({                                                                                     // 6
    class: "sidebar"                                                                                            // 7
  }, "\n          ", Spacebars.include(view.lookupTemplate("hello")), "\n\n\n      "), "\n\n      ", HTML.DIV({
    class: "input-output"                                                                                       // 9
  }, " \n         ", Spacebars.include(view.lookupTemplate("participants")), "\n         ", Spacebars.include(view.lookupTemplate("graph")), "\n      "), "\n    ") ];
}));                                                                                                            // 11
Meteor.startup(Template.body.renderToDocument);                                                                 // 12
                                                                                                                // 13
Template.__checkName("hello");                                                                                  // 14
Template["hello"] = new Template("Template.hello", (function() {                                                // 15
  var view = this;                                                                                              // 16
  return [ HTML.Raw("<!-- <form class='add_participant'> -->\n    "), HTML.DIV({                                // 17
    class: "add-participant-form"                                                                               // 18
  }, "\n\n      ", HTML.Raw('<div class="participant-form-item">\n        Identification number <input type="test" name="id_num" id="id_num" placeholder="1" value="1">\n      </div>'), "\n      ", HTML.Raw('<div class="participant-form-item">\n        Participant name <input type="text" name="participant_name" id="participant_name" placeholder="Fred" value="Fred">\n      </div>'), "\n      ", HTML.Raw('<div class="participant-form-item">\n       Solar capacity (kW) <input type="text" name="solar_capacity" id="solar_capacity" placeholder="4" value="4">\n      </div>'), "\n      ", HTML.Raw('<div class="participant-form-item">\n       Battery export limit (kW) <input type="text" name="battery_export_limit" id="battery_export_limit" placeholder="4" value="4">\n      </div>'), "\n      ", HTML.Raw('<div class="participant-form-item">\n        Battery capacity (kWh) <input type="text" name="battery_capacity" id="battery_capacity" placeholder="4" value="4">\n      </div>'), "\n      ", HTML.Raw('<div class="participant-form-item">\n       Enova customer? (Y/N) <input type="test" name="enova_customer_flag" id="enova_customer_flag" placeholder="Y" value="Y">\n      </div>'), "\n      ", HTML.DIV({
    class: "participant-form-item"                                                                              // 20
  }, "\n        ", HTML.SELECT({                                                                                // 21
    name: "retail-tariff-selector",                                                                             // 22
    id: "retail-tariff-selector",                                                                               // 23
    class: "form-control",                                                                                      // 24
    value: function() {                                                                                         // 25
      return Spacebars.mustache(Spacebars.dot(view.lookup("retail_tariffs"), "0"));                             // 26
    }                                                                                                           // 27
  }, "\n        ", Blaze.Each(function() {                                                                      // 28
    return {                                                                                                    // 29
      _sequence: Spacebars.call(view.lookup("retail_tariffs")),                                                 // 30
      _variable: "tariff"                                                                                       // 31
    };                                                                                                          // 32
  }, function() {                                                                                               // 33
    return [ "\n          ", HTML.OPTION({                                                                      // 34
      value: function() {                                                                                       // 35
        return Spacebars.mustache(view.lookup("tariff"));                                                       // 36
      }                                                                                                         // 37
    }, Blaze.View("lookup:tariff", function() {                                                                 // 38
      return Spacebars.mustache(view.lookup("tariff"));                                                         // 39
    })), "\n        " ];                                                                                        // 40
  }), "\n        "), "\n\n       ", HTML.Raw("<!-- Retail tariff <input type='test' name='retail_tariff' id='retail_tariff' placeholder=\"Enova flat commercial\" value=\"Enova flat commercial\"> -->"), "\n      "), "\n      ", HTML.DIV({
    class: "participant-form-item"                                                                              // 42
  }, "\n          ", HTML.SELECT({                                                                              // 43
    name: "network-tariff-selector",                                                                            // 44
    class: "form-control",                                                                                      // 45
    value: function() {                                                                                         // 46
      return Spacebars.mustache(Spacebars.dot(view.lookup("network_tariffs"), "0"));                            // 47
    }                                                                                                           // 48
  }, "\n          ", Blaze.Each(function() {                                                                    // 49
    return {                                                                                                    // 50
      _sequence: Spacebars.call(view.lookup("network_tariffs")),                                                // 51
      _variable: "tariff"                                                                                       // 52
    };                                                                                                          // 53
  }, function() {                                                                                               // 54
    return [ "\n            ", HTML.OPTION({                                                                    // 55
      value: function() {                                                                                       // 56
        return Spacebars.mustache(view.lookup("tariff"));                                                       // 57
      }                                                                                                         // 58
    }, Blaze.View("lookup:tariff", function() {                                                                 // 59
      return Spacebars.mustache(view.lookup("tariff"));                                                         // 60
    })), "\n          " ];                                                                                      // 61
  }), "\n          "), "\n        "), "\n      ", HTML.Raw('<div class="participant-form-item">\n       <button type="submit">Add participant</button>\n      </div>'), "\n\n      ", HTML.Raw('<div class="btn btn-success" id="run-simulation">Run Simulation</div>'), "\n    "), HTML.Raw("\n  <!-- </form> -->") ];
}));                                                                                                            // 63
                                                                                                                // 64
Template.__checkName("participants");                                                                           // 65
Template["participants"] = new Template("Template.participants", (function() {                                  // 66
  var view = this;                                                                                              // 67
  return HTML.DIV({                                                                                             // 68
    class: "participant_table"                                                                                  // 69
  }, HTML.Raw("\n    <h2>Participants</h2>\n    "), HTML.TABLE({                                                // 70
    style: "width:100%",                                                                                        // 71
    class: "participant_table_table"                                                                            // 72
  }, "\n        ", HTML.TR("\n            ", HTML.TH("Participant id number"), "\n            ", HTML.TH("Name:"), " \n            ", HTML.TH("Solar capacity"), "\n            ", HTML.TH("Battery export limit (kW)"), "\n            ", HTML.TH("Battery capacity"), "\n            ", HTML.TH(" Enova customer? (Y/N)"), "\n            ", HTML.TH(" Retail tariff"), "\n            ", HTML.TH(" Network tariff"), "\n          "), "\n            ", Blaze.Each(function() {
    return {                                                                                                    // 74
      _sequence: Spacebars.call(view.lookup("participants")),                                                   // 75
      _variable: "participant"                                                                                  // 76
    };                                                                                                          // 77
  }, function() {                                                                                               // 78
    return [ "\n            ", HTML.TR("\n              ", HTML.TD(Blaze.View("lookup:participant.id_num", function() {
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "id_num"));                           // 80
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.name", function() {                         // 81
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "name"));                             // 82
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.solar_capacity", function() {               // 83
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "solar_capacity"));                   // 84
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.battery_export_limit", function() {         // 85
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "battery_export_limit"));             // 86
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.battery_capacity", function() {             // 87
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "battery_capacity"));                 // 88
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.enova_customer_flag", function() {          // 89
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "enova_customer_flag"));              // 90
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.retail_tariff", function() {                // 91
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "retail_tariff"));                    // 92
    })), "\n              ", HTML.TD(Blaze.View("lookup:participant.network_tariff", function() {               // 93
      return Spacebars.mustache(Spacebars.dot(view.lookup("participant"), "network_tariff"));                   // 94
    })), "\n            "), "\n             " ];                                                                // 95
  }), "\n    "), "\n\n  ");                                                                                     // 96
}));                                                                                                            // 97
                                                                                                                // 98
Template.__checkName("graph");                                                                                  // 99
Template["graph"] = new Template("Template.graph", (function() {                                                // 100
  var view = this;                                                                                              // 101
  return HTML.Raw('<div id="content" class="graph-content">\n    \n      <form id="side_panel">\n        <h2>Energy Flow</h2>\n        <section><div id="legend"></div></section>\n        <section>\n          <div id="renderer_form" class="toggler">\n            <input type="radio" name="renderer" id="area" value="area" checked="">\n            <label for="area">area</label>\n            <input type="radio" name="renderer" id="bar" value="bar">\n            <label for="bar">bar</label>\n            <input type="radio" name="renderer" id="line" value="line">\n            <label for="line">line</label>\n            <input type="radio" name="renderer" id="scatter" value="scatterplot">\n            <label for="scatter">scatter</label>\n          </div>\n        </section>\n        <section>\n          <div id="offset_form">\n            <label for="stack">\n              <input type="radio" name="offset" id="stack" value="zero" checked="">\n              <span>stack</span>\n            </label>\n            <label for="stream">\n              <input type="radio" name="offset" id="stream" value="wiggle">\n              <span>stream</span>\n            </label>\n            <label for="pct">\n              <input type="radio" name="offset" id="pct" value="expand">\n              <span>pct</span>\n            </label>\n            <label for="value">\n              <input type="radio" name="offset" id="value" value="value">\n              <span>value</span>\n            </label>\n          </div>\n          <div id="interpolation_form">\n            <label for="cardinal">\n              <input type="radio" name="interpolation" id="cardinal" value="cardinal" checked="">\n              <span>cardinal</span>\n            </label>\n            <label for="linear">\n              <input type="radio" name="interpolation" id="linear" value="linear">\n              <span>linear</span>\n            </label>\n            <label for="step">\n              <input type="radio" name="interpolation" id="step" value="step-after">\n              <span>step</span>\n            </label>\n          </div>\n        </section>\n        <section>\n          <h6>Smoothing</h6>\n          <div id="smoother"></div>\n        </section>\n        <section></section>\n      </form>\n    \n      <div id="chart_container">\n        <div id="chart"></div>\n        <div id="timeline"></div>\n        <div id="preview"></div>\n      </div>\n    \n    </div>');
}));                                                                                                            // 103
                                                                                                                // 104
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

},"main.js":function(require,exports,module){

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                              //
// client/main.js                                                                                               //
//                                                                                                              //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                //
var Template = void 0;                                                                                          // 1
module.watch(require("meteor/templating"), {                                                                    // 1
    Template: function (v) {                                                                                    // 1
        Template = v;                                                                                           // 1
    }                                                                                                           // 1
}, 0);                                                                                                          // 1
var ReactiveVar = void 0;                                                                                       // 1
module.watch(require("meteor/reactive-var"), {                                                                  // 1
    ReactiveVar: function (v) {                                                                                 // 1
        ReactiveVar = v;                                                                                        // 1
    }                                                                                                           // 1
}, 1);                                                                                                          // 1
module.watch(require("./main.html"));                                                                           // 1
Template.hello.onCreated(function () {                                                                          // 6
    function helloOnCreated() {                                                                                 // 6
        // counter starts at 0                                                                                  // 7
        this.counter = new ReactiveVar(0);                                                                      // 8
        Session.set("participants", []);                                                                        // 9
    }                                                                                                           // 10
                                                                                                                //
    return helloOnCreated;                                                                                      // 6
}());                                                                                                           // 6
Template.hello.helpers({                                                                                        // 14
    counter: function () {                                                                                      // 15
        return Template.instance().counter.get();                                                               // 16
    },                                                                                                          // 17
    retail_tariffs: function () {                                                                               // 18
        return ['Retail Tariff 1', 'Retail Tariff 2', 'Retail Tariff 3'];                                       // 19
    },                                                                                                          // 20
    network_tariffs: function () {                                                                              // 21
        return ['Network Tariff 1', 'Network Tariff 2', 'Network Tariff 3'];                                    // 22
    }                                                                                                           // 23
});                                                                                                             // 14
Template.participants.helpers({                                                                                 // 27
    participants: function () {                                                                                 // 28
        var participants = Session.get("participants");                                                         // 29
        return participants;                                                                                    // 30
    }                                                                                                           // 31
});                                                                                                             // 27
Template.hello.events({                                                                                         // 34
    'click button': function (event, instance) {                                                                // 35
        console.log('Clicked the button!'); // increment the counter when button is clicked                     // 36
                                                                                                                //
        var id_num = $('#id_num').val();                                                                        // 38
        var name = $('#participant_name').val();                                                                // 39
        var solar_capacity = $('#solar_capacity').val();                                                        // 40
        var battery_export_limit = $('#battery_export_limit').val();                                            // 41
        var battery_capacity = $('#battery_capacity').val();                                                    // 42
        var enova_customer_flag = $('#enova_customer_flag').val();                                              // 43
        var retail_tariff = $('[name=retail_tariff_selector]').val(); // retail_tariff = tmpl.find('#retail_tariff_selector :selected');
        // console.log(battery_capacity)                                                                        // 49
                                                                                                                //
        instance.counter.set(instance.counter.get() + 1);                                                       // 50
        var participants = Session.get("participants");                                                         // 51
        participants.push({                                                                                     // 53
            id_num: id_num,                                                                                     // 54
            name: name,                                                                                         // 55
            solar_capacity: solar_capacity,                                                                     // 56
            battery_export_limit: battery_export_limit,                                                         // 57
            battery_capacity: battery_capacity,                                                                 // 58
            enova_customer_flag: enova_customer_flag,                                                           // 59
            retail_tariff: retail_tariff                                                                        // 60
        });                                                                                                     // 53
        Session.set("participants", participants);                                                              // 62
    },                                                                                                          // 63
    'click #run-simulation': function (event, instance) {                                                       // 65
        console.log('Running Simulation');                                                                      // 66
        Meteor.call('runSimulation', function (error, res) {                                                    // 67
            console.log(res);                                                                                   // 68
            console.log(JSON.parse(res));                                                                       // 69
        });                                                                                                     // 70
    }                                                                                                           // 71
});                                                                                                             // 34
Template.graph.onRendered(function () {                                                                         // 75
    console.log('graph rendered!');                                                                             // 76
                                                                                                                //
    var RenderControls = function (args) {                                                                      // 78
        var $ = jQuery;                                                                                         // 80
                                                                                                                //
        this.initialize = function () {                                                                         // 82
            this.element = args.element;                                                                        // 84
            this.graph = args.graph;                                                                            // 85
            this.settings = this.serialize();                                                                   // 86
            this.inputs = {                                                                                     // 88
                renderer: this.element.elements.renderer,                                                       // 89
                interpolation: this.element.elements.interpolation,                                             // 90
                offset: this.element.elements.offset                                                            // 91
            };                                                                                                  // 88
            this.element.addEventListener('change', function (e) {                                              // 94
                this.settings = this.serialize();                                                               // 96
                                                                                                                //
                if (e.target.name == 'renderer') {                                                              // 98
                    this.setDefaultOffset(e.target.value);                                                      // 99
                }                                                                                               // 100
                                                                                                                //
                this.syncOptions();                                                                             // 102
                this.settings = this.serialize();                                                               // 103
                var config = {                                                                                  // 105
                    renderer: this.settings.renderer,                                                           // 106
                    interpolation: this.settings.interpolation                                                  // 107
                };                                                                                              // 105
                                                                                                                //
                if (this.settings.offset == 'value') {                                                          // 110
                    config.unstack = true;                                                                      // 111
                    config.offset = 'zero';                                                                     // 112
                } else if (this.settings.offset == 'expand') {                                                  // 113
                    config.unstack = false;                                                                     // 114
                    config.offset = this.settings.offset;                                                       // 115
                } else {                                                                                        // 116
                    config.unstack = false;                                                                     // 117
                    config.offset = this.settings.offset;                                                       // 118
                }                                                                                               // 119
                                                                                                                //
                this.graph.configure(config);                                                                   // 121
                this.graph.render();                                                                            // 122
            }.bind(this), false);                                                                               // 124
        };                                                                                                      // 125
                                                                                                                //
        this.serialize = function () {                                                                          // 127
            var values = {};                                                                                    // 129
            var pairs = $(this.element).serializeArray();                                                       // 130
            pairs.forEach(function (pair) {                                                                     // 132
                values[pair.name] = pair.value;                                                                 // 133
            });                                                                                                 // 134
            return values;                                                                                      // 136
        };                                                                                                      // 137
                                                                                                                //
        this.syncOptions = function () {                                                                        // 139
            var options = this.rendererOptions[this.settings.renderer];                                         // 141
            Array.prototype.forEach.call(this.inputs.interpolation, function (input) {                          // 143
                if (options.interpolation) {                                                                    // 145
                    input.disabled = false;                                                                     // 146
                    input.parentNode.classList.remove('disabled');                                              // 147
                } else {                                                                                        // 148
                    input.disabled = true;                                                                      // 149
                    input.parentNode.classList.add('disabled');                                                 // 150
                }                                                                                               // 151
            });                                                                                                 // 152
            Array.prototype.forEach.call(this.inputs.offset, function (input) {                                 // 154
                if (options.offset.filter(function (o) {                                                        // 156
                    return o == input.value;                                                                    // 156
                }).length) {                                                                                    // 156
                    input.disabled = false;                                                                     // 157
                    input.parentNode.classList.remove('disabled');                                              // 158
                } else {                                                                                        // 160
                    input.disabled = true;                                                                      // 161
                    input.parentNode.classList.add('disabled');                                                 // 162
                }                                                                                               // 163
            }.bind(this));                                                                                      // 165
        };                                                                                                      // 167
                                                                                                                //
        this.setDefaultOffset = function (renderer) {                                                           // 169
            var options = this.rendererOptions[renderer];                                                       // 171
                                                                                                                //
            if (options.defaults && options.defaults.offset) {                                                  // 173
                Array.prototype.forEach.call(this.inputs.offset, function (input) {                             // 175
                    if (input.value == options.defaults.offset) {                                               // 176
                        input.checked = true;                                                                   // 177
                    } else {                                                                                    // 178
                        input.checked = false;                                                                  // 179
                    }                                                                                           // 180
                }.bind(this));                                                                                  // 182
            }                                                                                                   // 183
        };                                                                                                      // 184
                                                                                                                //
        this.rendererOptions = {                                                                                // 186
            area: {                                                                                             // 188
                interpolation: true,                                                                            // 189
                offset: ['zero', 'wiggle', 'expand', 'value'],                                                  // 190
                defaults: {                                                                                     // 191
                    offset: 'zero'                                                                              // 191
                }                                                                                               // 191
            },                                                                                                  // 188
            line: {                                                                                             // 193
                interpolation: true,                                                                            // 194
                offset: ['expand', 'value'],                                                                    // 195
                defaults: {                                                                                     // 196
                    offset: 'value'                                                                             // 196
                }                                                                                               // 196
            },                                                                                                  // 193
            bar: {                                                                                              // 198
                interpolation: false,                                                                           // 199
                offset: ['zero', 'wiggle', 'expand', 'value'],                                                  // 200
                defaults: {                                                                                     // 201
                    offset: 'zero'                                                                              // 201
                }                                                                                               // 201
            },                                                                                                  // 198
            scatterplot: {                                                                                      // 203
                interpolation: false,                                                                           // 204
                offset: ['value'],                                                                              // 205
                defaults: {                                                                                     // 206
                    offset: 'value'                                                                             // 206
                }                                                                                               // 206
            }                                                                                                   // 203
        };                                                                                                      // 186
        this.initialize();                                                                                      // 210
    }; // set up our data series with 150 random data points                                                    // 211
                                                                                                                //
                                                                                                                //
    var seriesData = [[], [], [], [], [], [], [], [], []];                                                      // 217
    var random = new Rickshaw.Fixtures.RandomData(150);                                                         // 228
                                                                                                                //
    for (var i = 0; i < 150; i++) {                                                                             // 230
        random.addData(seriesData);                                                                             // 231
    }                                                                                                           // 232
                                                                                                                //
    var palette = new Rickshaw.Color.Palette({                                                                  // 234
        scheme: 'classic9'                                                                                      // 234
    }); // instantiate our graph!                                                                               // 234
                                                                                                                //
    var graph = new Rickshaw.Graph({                                                                            // 238
        element: document.getElementById("chart"),                                                              // 239
        width: 900,                                                                                             // 240
        height: 500,                                                                                            // 241
        renderer: 'area',                                                                                       // 242
        stroke: true,                                                                                           // 243
        preserve: true,                                                                                         // 244
        series: [{                                                                                              // 245
            color: palette.color(),                                                                             // 246
            data: seriesData[0],                                                                                // 247
            name: 'Moscow'                                                                                      // 248
        }, {                                                                                                    // 245
            color: palette.color(),                                                                             // 250
            data: seriesData[1],                                                                                // 251
            name: 'Shanghai'                                                                                    // 252
        }, {                                                                                                    // 249
            color: palette.color(),                                                                             // 254
            data: seriesData[2],                                                                                // 255
            name: 'Amsterdam'                                                                                   // 256
        }, {                                                                                                    // 253
            color: palette.color(),                                                                             // 258
            data: seriesData[3],                                                                                // 259
            name: 'Paris'                                                                                       // 260
        }, {                                                                                                    // 257
            color: palette.color(),                                                                             // 262
            data: seriesData[4],                                                                                // 263
            name: 'Tokyo'                                                                                       // 264
        }, {                                                                                                    // 261
            color: palette.color(),                                                                             // 266
            data: seriesData[5],                                                                                // 267
            name: 'London'                                                                                      // 268
        }, {                                                                                                    // 265
            color: palette.color(),                                                                             // 270
            data: seriesData[6],                                                                                // 271
            name: 'New York'                                                                                    // 272
        }]                                                                                                      // 269
    });                                                                                                         // 238
    graph.render();                                                                                             // 276
    var preview = new Rickshaw.Graph.RangeSlider.Preview({                                                      // 278
        graph: graph,                                                                                           // 279
        element: document.getElementById('preview')                                                             // 280
    });                                                                                                         // 278
    var hoverDetail = new Rickshaw.Graph.HoverDetail({                                                          // 283
        graph: graph,                                                                                           // 284
        xFormatter: function (x) {                                                                              // 285
            return new Date(x * 1000).toString();                                                               // 286
        }                                                                                                       // 287
    });                                                                                                         // 283
    var annotator = new Rickshaw.Graph.Annotate({                                                               // 290
        graph: graph,                                                                                           // 291
        element: document.getElementById('timeline')                                                            // 292
    });                                                                                                         // 290
    var legend = new Rickshaw.Graph.Legend({                                                                    // 295
        graph: graph,                                                                                           // 296
        element: document.getElementById('legend')                                                              // 297
    });                                                                                                         // 295
    var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({                                                  // 301
        graph: graph,                                                                                           // 302
        legend: legend                                                                                          // 303
    });                                                                                                         // 301
    var order = new Rickshaw.Graph.Behavior.Series.Order({                                                      // 306
        graph: graph,                                                                                           // 307
        legend: legend                                                                                          // 308
    });                                                                                                         // 306
    var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({                                            // 311
        graph: graph,                                                                                           // 312
        legend: legend                                                                                          // 313
    });                                                                                                         // 311
    var smoother = new Rickshaw.Graph.Smoother({                                                                // 316
        graph: graph,                                                                                           // 317
        element: document.querySelector('#smoother')                                                            // 318
    });                                                                                                         // 316
    var ticksTreatment = 'glow';                                                                                // 321
    var xAxis = new Rickshaw.Graph.Axis.Time({                                                                  // 323
        graph: graph,                                                                                           // 324
        ticksTreatment: ticksTreatment,                                                                         // 325
        timeFixture: new Rickshaw.Fixtures.Time.Local()                                                         // 326
    });                                                                                                         // 323
    xAxis.render();                                                                                             // 329
    var yAxis = new Rickshaw.Graph.Axis.Y({                                                                     // 331
        graph: graph,                                                                                           // 332
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,                                                        // 333
        ticksTreatment: ticksTreatment                                                                          // 334
    });                                                                                                         // 331
    yAxis.render();                                                                                             // 337
    var controls = new RenderControls({                                                                         // 340
        element: document.querySelector('form'),                                                                // 341
        graph: graph                                                                                            // 342
    }); // add some data every so often                                                                         // 340
                                                                                                                //
    var messages = ["Changed home page welcome message", "Minified JS and CSS", "Changed button color from blue to green", "Refactored SQL query to use indexed columns", "Added additional logging for debugging", "Fixed typo", "Rewrite conditional logic for clarity", "Added documentation for new methods"];
    setInterval(function () {                                                                                   // 358
        random.removeData(seriesData);                                                                          // 359
        random.addData(seriesData);                                                                             // 360
        graph.update();                                                                                         // 361
    }, 3000);                                                                                                   // 363
                                                                                                                //
    function addAnnotation(force) {                                                                             // 365
        if (messages.length > 0 && (force || Math.random() >= 0.95)) {                                          // 366
            annotator.add(seriesData[2][seriesData[2].length - 1].x, messages.shift());                         // 367
            annotator.update();                                                                                 // 368
        }                                                                                                       // 369
    }                                                                                                           // 370
                                                                                                                //
    addAnnotation(true);                                                                                        // 372
    setTimeout(function () {                                                                                    // 373
        setInterval(addAnnotation, 6000);                                                                       // 373
    }, 6000);                                                                                                   // 373
    console.log(preview);                                                                                       // 375
    var previewXAxis = new Rickshaw.Graph.Axis.Time({                                                           // 376
        graph: preview.previews[0],                                                                             // 377
        timeFixture: new Rickshaw.Fixtures.Time.Local(),                                                        // 378
        ticksTreatment: ticksTreatment                                                                          // 379
    });                                                                                                         // 376
    previewXAxis.render();                                                                                      // 382
});                                                                                                             // 383
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

}}},{
  "extensions": [
    ".js",
    ".json",
    ".html",
    ".css"
  ]
});
require("./client/template.main.js");
require("./client/main.js");