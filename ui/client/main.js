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
  participants() {
    var participants = Session.get("participants");
    return participants;
  },
});

Template.hello.events({
  'click button'(event, instance) {
    console.log('Clicked the button!')
    // increment the counter when button is clicked
    var id_num=$('#id_num').val();
    var name=$('#participant_name').val();
    var solar_capacity=$('#solar_capacity').val();
    var battery_export_limit=$('#battery_export_limit').val();
    var battery_capacity=$('#battery_capacity').val();
    var enova_customer_flag=$('#enova_customer_flag').val();
    var retail_tariff=$('#retail_tariff').val();
    // console.log(battery_capacity)
    instance.counter.set(instance.counter.get() + 1);
    var participants = Session.get("participants");
    
    participants.push({
      id_num : id_num,
      name : name, 
      solar_capacity: solar_capacity, 
      battery_export_limit : battery_export_limit, 
      battery_capacity:battery_capacity,
      enova_customer_flag : enova_customer_flag,
      retail_tariff : retail_tariff
    });
    Session.set("participants", participants);
  },
});
