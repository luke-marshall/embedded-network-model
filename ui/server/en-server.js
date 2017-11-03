Meteor.methods({
    'runSimulation': function(participants) {
        var syncHTTP = Meteor.wrapAsync(HTTP.get);
        var url = Meteor.settings.simulation_api_url + "/";
        var result = syncHTTP(url, { data: { participants: participants } });
        console.log(result);
        return result.content;
        // return JSON.parse(result.content);
    },
    'participantNames': function() {
        var syncHTTP = Meteor.wrapAsync(HTTP.get);
        var url = Meteor.settings.simulation_api_url + "/participantNames";
        var result = syncHTTP(url, {});
        console.log(result);
        // return result.content;
        return JSON.parse(result.content);
    }
});