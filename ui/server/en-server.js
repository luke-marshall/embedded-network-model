Meteor.methods({
    'runSimulation': function(participants) {
        var syncHTTP = Meteor.wrapAsync(HTTP.get);
        var url = "http://127.0.0.1:5000/";
        var result = syncHTTP(url, { data: { participants: participants } });
        console.log(result);
        return result.content;
        // return JSON.parse(result.content);
    }
});