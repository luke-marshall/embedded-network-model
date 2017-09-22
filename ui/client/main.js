import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';

import './main.html';

Template.hello.onCreated(function helloOnCreated() {
    // counter starts at 0
    this.counter = new ReactiveVar(0);
    Session.set("participants", []);
});



Template.hello.helpers({
    counter() {
        return Template.instance().counter.get();
    },
    retail_tariffs() {
        return ['Retail Tariff 1', 'Retail Tariff 2', 'Retail Tariff 3'];
    },
    network_tariffs() {
        return ['Network Tariff 1', 'Network Tariff 2', 'Network Tariff 3'];
    }

});

Template.participants.helpers({
    participants() {
        var participants = Session.get("participants");
        return participants;
    },
});

Template.hello.events({
    'click button' (event, instance) {
        console.log('Clicked the button!')
            // increment the counter when button is clicked
        var id_num = $('#id_num').val();
        var name = $('#participant_name').val();
        var solar_capacity = $('#solar_capacity').val();
        var battery_export_limit = $('#battery_export_limit').val();
        var battery_capacity = $('#battery_capacity').val();
        var enova_customer_flag = $('#enova_customer_flag').val();
        var retail_tariff = $('[name=retail_tariff_selector]').val();

        // retail_tariff = tmpl.find('#retail_tariff_selector :selected');


        // console.log(battery_capacity)
        instance.counter.set(instance.counter.get() + 1);
        var participants = Session.get("participants");

        participants.push({
            id_num: id_num,
            name: name,
            solar_capacity: solar_capacity,
            battery_export_limit: battery_export_limit,
            battery_capacity: battery_capacity,
            enova_customer_flag: enova_customer_flag,
            retail_tariff: retail_tariff
        });
        Session.set("participants", participants);
    },

    'click #run-simulation' (event, instance) {
        console.log('Running Simulation')
        Meteor.call('runSimulation', function(error, res) {
            console.log(res);
            console.log(JSON.parse(res))
        });
    }
});


Template.graph.onRendered(function() {
    console.log('graph rendered!');

    var RenderControls = function(args) {

        var $ = jQuery;

        this.initialize = function() {

            this.element = args.element;
            this.graph = args.graph;
            this.settings = this.serialize();

            this.inputs = {
                renderer: this.element.elements.renderer,
                interpolation: this.element.elements.interpolation,
                offset: this.element.elements.offset
            };

            this.element.addEventListener('change', function(e) {

                this.settings = this.serialize();

                if (e.target.name == 'renderer') {
                    this.setDefaultOffset(e.target.value);
                }

                this.syncOptions();
                this.settings = this.serialize();

                var config = {
                    renderer: this.settings.renderer,
                    interpolation: this.settings.interpolation
                };

                if (this.settings.offset == 'value') {
                    config.unstack = true;
                    config.offset = 'zero';
                } else if (this.settings.offset == 'expand') {
                    config.unstack = false;
                    config.offset = this.settings.offset;
                } else {
                    config.unstack = false;
                    config.offset = this.settings.offset;
                }

                this.graph.configure(config);
                this.graph.render();

            }.bind(this), false);
        }

        this.serialize = function() {

            var values = {};
            var pairs = $(this.element).serializeArray();

            pairs.forEach(function(pair) {
                values[pair.name] = pair.value;
            });

            return values;
        };

        this.syncOptions = function() {

            var options = this.rendererOptions[this.settings.renderer];

            Array.prototype.forEach.call(this.inputs.interpolation, function(input) {

                if (options.interpolation) {
                    input.disabled = false;
                    input.parentNode.classList.remove('disabled');
                } else {
                    input.disabled = true;
                    input.parentNode.classList.add('disabled');
                }
            });

            Array.prototype.forEach.call(this.inputs.offset, function(input) {

                if (options.offset.filter(function(o) { return o == input.value }).length) {
                    input.disabled = false;
                    input.parentNode.classList.remove('disabled');

                } else {
                    input.disabled = true;
                    input.parentNode.classList.add('disabled');
                }

            }.bind(this));

        };

        this.setDefaultOffset = function(renderer) {

            var options = this.rendererOptions[renderer];

            if (options.defaults && options.defaults.offset) {

                Array.prototype.forEach.call(this.inputs.offset, function(input) {
                    if (input.value == options.defaults.offset) {
                        input.checked = true;
                    } else {
                        input.checked = false;
                    }

                }.bind(this));
            }
        };

        this.rendererOptions = {

            area: {
                interpolation: true,
                offset: ['zero', 'wiggle', 'expand', 'value'],
                defaults: { offset: 'zero' }
            },
            line: {
                interpolation: true,
                offset: ['expand', 'value'],
                defaults: { offset: 'value' }
            },
            bar: {
                interpolation: false,
                offset: ['zero', 'wiggle', 'expand', 'value'],
                defaults: { offset: 'zero' }
            },
            scatterplot: {
                interpolation: false,
                offset: ['value'],
                defaults: { offset: 'value' }
            }
        };

        this.initialize();
    };



    // set up our data series with 150 random data points

    var seriesData = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ];
    var random = new Rickshaw.Fixtures.RandomData(150);

    for (var i = 0; i < 150; i++) {
        random.addData(seriesData);
    }

    var palette = new Rickshaw.Color.Palette({ scheme: 'classic9' });

    // instantiate our graph!

    var graph = new Rickshaw.Graph({
        element: document.getElementById("chart"),
        width: 900,
        height: 500,
        renderer: 'area',
        stroke: true,
        preserve: true,
        series: [{
            color: palette.color(),
            data: seriesData[0],
            name: 'Moscow'
        }, {
            color: palette.color(),
            data: seriesData[1],
            name: 'Shanghai'
        }, {
            color: palette.color(),
            data: seriesData[2],
            name: 'Amsterdam'
        }, {
            color: palette.color(),
            data: seriesData[3],
            name: 'Paris'
        }, {
            color: palette.color(),
            data: seriesData[4],
            name: 'Tokyo'
        }, {
            color: palette.color(),
            data: seriesData[5],
            name: 'London'
        }, {
            color: palette.color(),
            data: seriesData[6],
            name: 'New York'
        }]
    });

    graph.render();

    var preview = new Rickshaw.Graph.RangeSlider.Preview({
        graph: graph,
        element: document.getElementById('preview'),
    });

    var hoverDetail = new Rickshaw.Graph.HoverDetail({
        graph: graph,
        xFormatter: function(x) {
            return new Date(x * 1000).toString();
        }
    });

    var annotator = new Rickshaw.Graph.Annotate({
        graph: graph,
        element: document.getElementById('timeline')
    });

    var legend = new Rickshaw.Graph.Legend({
        graph: graph,
        element: document.getElementById('legend')

    });

    var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
        graph: graph,
        legend: legend
    });

    var order = new Rickshaw.Graph.Behavior.Series.Order({
        graph: graph,
        legend: legend
    });

    var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
        graph: graph,
        legend: legend
    });

    var smoother = new Rickshaw.Graph.Smoother({
        graph: graph,
        element: document.querySelector('#smoother')
    });

    var ticksTreatment = 'glow';

    var xAxis = new Rickshaw.Graph.Axis.Time({
        graph: graph,
        ticksTreatment: ticksTreatment,
        timeFixture: new Rickshaw.Fixtures.Time.Local()
    });

    xAxis.render();

    var yAxis = new Rickshaw.Graph.Axis.Y({
        graph: graph,
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        ticksTreatment: ticksTreatment
    });

    yAxis.render();


    var controls = new RenderControls({
        element: document.querySelector('form'),
        graph: graph
    });

    // add some data every so often

    var messages = [
        "Changed home page welcome message",
        "Minified JS and CSS",
        "Changed button color from blue to green",
        "Refactored SQL query to use indexed columns",
        "Added additional logging for debugging",
        "Fixed typo",
        "Rewrite conditional logic for clarity",
        "Added documentation for new methods"
    ];

    setInterval(function() {
        random.removeData(seriesData);
        random.addData(seriesData);
        graph.update();

    }, 3000);

    function addAnnotation(force) {
        if (messages.length > 0 && (force || Math.random() >= 0.95)) {
            annotator.add(seriesData[2][seriesData[2].length - 1].x, messages.shift());
            annotator.update();
        }
    }

    addAnnotation(true);
    setTimeout(function() { setInterval(addAnnotation, 6000) }, 6000);

    console.log(preview)
    var previewXAxis = new Rickshaw.Graph.Axis.Time({
        graph: preview.previews[0],
        timeFixture: new Rickshaw.Fixtures.Time.Local(),
        ticksTreatment: ticksTreatment
    });

    previewXAxis.render();
});