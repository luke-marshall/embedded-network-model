//////////////////////////////////////////////////////////////////////////
//                                                                      //
// This is a generated file. You can view the original                  //
// source in your browser if your browser supports source maps.         //
// Source maps are supported by all recent versions of Chrome, Safari,  //
// and Firefox, and by Internet Explorer 11.                            //
//                                                                      //
//////////////////////////////////////////////////////////////////////////


(function () {

/* Imports */
var Meteor = Package.meteor.Meteor;
var global = Package.meteor.global;
var meteorEnv = Package.meteor.meteorEnv;
var AllowDeny = Package['allow-deny'].AllowDeny;
var Random = Package.random.Random;
var EJSON = Package.ejson.EJSON;
var _ = Package.underscore._;
var LocalCollection = Package.minimongo.LocalCollection;
var Minimongo = Package.minimongo.Minimongo;
var DDP = Package['ddp-client'].DDP;
var Tracker = Package.tracker.Tracker;
var Deps = Package.tracker.Deps;
var DiffSequence = Package['diff-sequence'].DiffSequence;
var MongoID = Package['mongo-id'].MongoID;
var check = Package.check.check;
var Match = Package.check.Match;
var meteorInstall = Package.modules.meteorInstall;
var meteorBabelHelpers = Package['babel-runtime'].meteorBabelHelpers;
var Promise = Package.promise.Promise;
var Symbol = Package['ecmascript-runtime-client'].Symbol;
var Map = Package['ecmascript-runtime-client'].Map;
var Set = Package['ecmascript-runtime-client'].Set;

/* Package-scope variables */
var LocalCollectionDriver, Mongo;

var require = meteorInstall({"node_modules":{"meteor":{"mongo":{"local_collection_driver.js":function(){

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                              //
// packages/mongo/local_collection_driver.js                                                                    //
//                                                                                                              //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                //
LocalCollectionDriver = function () {                                                                           // 1
  var self = this;                                                                                              // 2
  self.noConnCollections = {};                                                                                  // 3
};                                                                                                              // 4
                                                                                                                //
var ensureCollection = function (name, collections) {                                                           // 6
  if (!(name in collections)) collections[name] = new LocalCollection(name);                                    // 7
  return collections[name];                                                                                     // 9
};                                                                                                              // 10
                                                                                                                //
_.extend(LocalCollectionDriver.prototype, {                                                                     // 12
  open: function (name, conn) {                                                                                 // 13
    var self = this;                                                                                            // 14
    if (!name) return new LocalCollection();                                                                    // 15
                                                                                                                //
    if (!conn) {                                                                                                // 17
      return ensureCollection(name, self.noConnCollections);                                                    // 18
    }                                                                                                           // 19
                                                                                                                //
    if (!conn._mongo_livedata_collections) conn._mongo_livedata_collections = {}; // XXX is there a way to keep track of a connection's collections without
    // dangling it off the connection object?                                                                   // 23
                                                                                                                //
    return ensureCollection(name, conn._mongo_livedata_collections);                                            // 24
  }                                                                                                             // 25
}); // singleton                                                                                                // 12
                                                                                                                //
                                                                                                                //
LocalCollectionDriver = new LocalCollectionDriver();                                                            // 29
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

},"collection.js":function(require,exports,module){

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                              //
// packages/mongo/collection.js                                                                                 //
//                                                                                                              //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
                                                                                                                //
// options.connection, if given, is a LivedataClient or LivedataServer                                          // 1
// XXX presently there is no way to destroy/clean up a Collection                                               // 2
/**                                                                                                             // 4
 * @summary Namespace for MongoDB-related items                                                                 //
 * @namespace                                                                                                   //
 */Mongo = {}; /**                                                                                              //
                * @summary Constructor for a Collection                                                         //
                * @locus Anywhere                                                                               //
                * @instancename collection                                                                      //
                * @class                                                                                        //
                * @param {String} name The name of the collection.  If null, creates an unmanaged (unsynchronized) local collection.
                * @param {Object} [options]                                                                     //
                * @param {Object} options.connection The server connection that will manage this collection. Uses the default connection if not specified.  Pass the return value of calling [`DDP.connect`](#ddp_connect) to specify a different server. Pass `null` to specify no connection. Unmanaged (`name` is null) collections cannot specify a connection.
                * @param {String} options.idGeneration The method of generating the `_id` fields of new documents in this collection.  Possible values:
                                                                                                                //
                - **`'STRING'`**: random strings                                                                //
                - **`'MONGO'`**:  random [`Mongo.ObjectID`](#mongo_object_id) values                            //
                                                                                                                //
               The default id generation technique is `'STRING'`.                                               //
                * @param {Function} options.transform An optional transformation function. Documents will be passed through this function before being returned from `fetch` or `findOne`, and before being passed to callbacks of `observe`, `map`, `forEach`, `allow`, and `deny`. Transforms are *not* applied for the callbacks of `observeChanges` or to cursors returned from publish functions.
                * @param {Boolean} options.defineMutationMethods Set to `false` to skip setting up the mutation methods that enable insert/update/remove from client code. Default `true`.
                */                                                                                              //
                                                                                                                //
Mongo.Collection = function (name, options) {                                                                   // 27
  var self = this;                                                                                              // 28
  if (!(self instanceof Mongo.Collection)) throw new Error('use "new" to construct a Mongo.Collection');        // 29
                                                                                                                //
  if (!name && name !== null) {                                                                                 // 32
    Meteor._debug("Warning: creating anonymous collection. It will not be " + "saved or synchronized over the network. (Pass null for " + "the collection name to turn off this warning.)");
                                                                                                                //
    name = null;                                                                                                // 36
  }                                                                                                             // 37
                                                                                                                //
  if (name !== null && typeof name !== "string") {                                                              // 39
    throw new Error("First argument to new Mongo.Collection must be a string or null");                         // 40
  }                                                                                                             // 42
                                                                                                                //
  if (options && options.methods) {                                                                             // 44
    // Backwards compatibility hack with original signature (which passed                                       // 45
    // "connection" directly instead of in options. (Connections must have a "methods"                          // 46
    // method.)                                                                                                 // 47
    // XXX remove before 1.0                                                                                    // 48
    options = {                                                                                                 // 49
      connection: options                                                                                       // 49
    };                                                                                                          // 49
  } // Backwards compatibility: "connection" used to be called "manager".                                       // 50
                                                                                                                //
                                                                                                                //
  if (options && options.manager && !options.connection) {                                                      // 52
    options.connection = options.manager;                                                                       // 53
  }                                                                                                             // 54
                                                                                                                //
  options = _.extend({                                                                                          // 55
    connection: undefined,                                                                                      // 56
    idGeneration: 'STRING',                                                                                     // 57
    transform: null,                                                                                            // 58
    _driver: undefined,                                                                                         // 59
    _preventAutopublish: false                                                                                  // 60
  }, options);                                                                                                  // 55
                                                                                                                //
  switch (options.idGeneration) {                                                                               // 63
    case 'MONGO':                                                                                               // 64
      self._makeNewID = function () {                                                                           // 65
        var src = name ? DDP.randomStream('/collection/' + name) : Random.insecure;                             // 66
        return new Mongo.ObjectID(src.hexString(24));                                                           // 67
      };                                                                                                        // 68
                                                                                                                //
      break;                                                                                                    // 69
                                                                                                                //
    case 'STRING':                                                                                              // 70
    default:                                                                                                    // 71
      self._makeNewID = function () {                                                                           // 72
        var src = name ? DDP.randomStream('/collection/' + name) : Random.insecure;                             // 73
        return src.id();                                                                                        // 74
      };                                                                                                        // 75
                                                                                                                //
      break;                                                                                                    // 76
  }                                                                                                             // 63
                                                                                                                //
  self._transform = LocalCollection.wrapTransform(options.transform);                                           // 79
  if (!name || options.connection === null) // note: nameless collections never have a connection               // 81
    self._connection = null;else if (options.connection) self._connection = options.connection;else if (Meteor.isClient) self._connection = Meteor.connection;else self._connection = Meteor.server;
                                                                                                                //
  if (!options._driver) {                                                                                       // 91
    // XXX This check assumes that webapp is loaded so that Meteor.server !==                                   // 92
    // null. We should fully support the case of "want to use a Mongo-backed                                    // 93
    // collection from Node code without webapp", but we don't yet.                                             // 94
    // #MeteorServerNull                                                                                        // 95
    if (name && self._connection === Meteor.server && typeof MongoInternals !== "undefined" && MongoInternals.defaultRemoteCollectionDriver) {
      options._driver = MongoInternals.defaultRemoteCollectionDriver();                                         // 99
    } else {                                                                                                    // 100
      options._driver = LocalCollectionDriver;                                                                  // 101
    }                                                                                                           // 102
  }                                                                                                             // 103
                                                                                                                //
  self._collection = options._driver.open(name, self._connection);                                              // 105
  self._name = name;                                                                                            // 106
  self._driver = options._driver;                                                                               // 107
                                                                                                                //
  if (self._connection && self._connection.registerStore) {                                                     // 109
    // OK, we're going to be a slave, replicating some remote                                                   // 110
    // database, except possibly with some temporary divergence while                                           // 111
    // we have unacknowledged RPC's.                                                                            // 112
    var ok = self._connection.registerStore(name, {                                                             // 113
      // Called at the beginning of a batch of updates. batchSize is the number                                 // 114
      // of update calls to expect.                                                                             // 115
      //                                                                                                        // 116
      // XXX This interface is pretty janky. reset probably ought to go back to                                 // 117
      // being its own function, and callers shouldn't have to calculate                                        // 118
      // batchSize. The optimization of not calling pause/remove should be                                      // 119
      // delayed until later: the first call to update() should buffer its                                      // 120
      // message, and then we can either directly apply it at endUpdate time if                                 // 121
      // it was the only update, or do pauseObservers/apply/apply at the next                                   // 122
      // update() if there's another one.                                                                       // 123
      beginUpdate: function (batchSize, reset) {                                                                // 124
        // pause observers so users don't see flicker when updating several                                     // 125
        // objects at once (including the post-reconnect reset-and-reapply                                      // 126
        // stage), and so that a re-sorting of a query can take advantage of the                                // 127
        // full _diffQuery moved calculation instead of applying change one at a                                // 128
        // time.                                                                                                // 129
        if (batchSize > 1 || reset) self._collection.pauseObservers();                                          // 130
        if (reset) self._collection.remove({});                                                                 // 133
      },                                                                                                        // 135
      // Apply an update.                                                                                       // 137
      // XXX better specify this interface (not in terms of a wire message)?                                    // 138
      update: function (msg) {                                                                                  // 139
        var mongoId = MongoID.idParse(msg.id);                                                                  // 140
                                                                                                                //
        var doc = self._collection.findOne(mongoId); // Is this a "replace the whole doc" message coming from the quiescence
        // of method writes to an object? (Note that 'undefined' is a valid                                     // 144
        // value meaning "remove it".)                                                                          // 145
                                                                                                                //
                                                                                                                //
        if (msg.msg === 'replace') {                                                                            // 146
          var replace = msg.replace;                                                                            // 147
                                                                                                                //
          if (!replace) {                                                                                       // 148
            if (doc) self._collection.remove(mongoId);                                                          // 149
          } else if (!doc) {                                                                                    // 151
            self._collection.insert(replace);                                                                   // 152
          } else {                                                                                              // 153
            // XXX check that replace has no $ ops                                                              // 154
            self._collection.update(mongoId, replace);                                                          // 155
          }                                                                                                     // 156
                                                                                                                //
          return;                                                                                               // 157
        } else if (msg.msg === 'added') {                                                                       // 158
          if (doc) {                                                                                            // 159
            throw new Error("Expected not to find a document already present for an add");                      // 160
          }                                                                                                     // 161
                                                                                                                //
          self._collection.insert(_.extend({                                                                    // 162
            _id: mongoId                                                                                        // 162
          }, msg.fields));                                                                                      // 162
        } else if (msg.msg === 'removed') {                                                                     // 163
          if (!doc) throw new Error("Expected to find a document already present for removed");                 // 164
                                                                                                                //
          self._collection.remove(mongoId);                                                                     // 166
        } else if (msg.msg === 'changed') {                                                                     // 167
          if (!doc) throw new Error("Expected to find a document to change");                                   // 168
                                                                                                                //
          if (!_.isEmpty(msg.fields)) {                                                                         // 170
            var modifier = {};                                                                                  // 171
                                                                                                                //
            _.each(msg.fields, function (value, key) {                                                          // 172
              if (value === undefined) {                                                                        // 173
                if (!modifier.$unset) modifier.$unset = {};                                                     // 174
                modifier.$unset[key] = 1;                                                                       // 176
              } else {                                                                                          // 177
                if (!modifier.$set) modifier.$set = {};                                                         // 178
                modifier.$set[key] = value;                                                                     // 180
              }                                                                                                 // 181
            });                                                                                                 // 182
                                                                                                                //
            self._collection.update(mongoId, modifier);                                                         // 183
          }                                                                                                     // 184
        } else {                                                                                                // 185
          throw new Error("I don't know how to deal with this message");                                        // 186
        }                                                                                                       // 187
      },                                                                                                        // 189
      // Called at the end of a batch of updates.                                                               // 191
      endUpdate: function () {                                                                                  // 192
        self._collection.resumeObservers();                                                                     // 193
      },                                                                                                        // 194
      // Called around method stub invocations to capture the original versions                                 // 196
      // of modified documents.                                                                                 // 197
      saveOriginals: function () {                                                                              // 198
        self._collection.saveOriginals();                                                                       // 199
      },                                                                                                        // 200
      retrieveOriginals: function () {                                                                          // 201
        return self._collection.retrieveOriginals();                                                            // 202
      },                                                                                                        // 203
      // Used to preserve current versions of documents across a store reset.                                   // 205
      getDoc: function (id) {                                                                                   // 206
        return self.findOne(id);                                                                                // 207
      },                                                                                                        // 208
      // To be able to get back to the collection from the store.                                               // 210
      _getCollection: function () {                                                                             // 211
        return self;                                                                                            // 212
      }                                                                                                         // 213
    });                                                                                                         // 113
                                                                                                                //
    if (!ok) {                                                                                                  // 216
      var message = "There is already a collection named \"" + name + "\"";                                     // 217
                                                                                                                //
      if (options._suppressSameNameError === true) {                                                            // 218
        // XXX In theory we do not have to throw when `ok` is falsy. The store is already defined               // 219
        // for this collection name, but this will simply be another reference to it and everything             // 220
        // should work. However, we have historically thrown an error here, so for now we will                  // 221
        // skip the error only when `_suppressSameNameError` is `true`, allowing people to opt in               // 222
        // and give this some real world testing.                                                               // 223
        console.warn ? console.warn(message) : console.log(message);                                            // 224
      } else {                                                                                                  // 225
        throw new Error(message);                                                                               // 226
      }                                                                                                         // 227
    }                                                                                                           // 228
  } // XXX don't define these until allow or deny is actually used for this                                     // 229
  // collection. Could be hard if the security rules are only defined on the                                    // 232
  // server.                                                                                                    // 233
                                                                                                                //
                                                                                                                //
  if (options.defineMutationMethods !== false) {                                                                // 234
    try {                                                                                                       // 235
      self._defineMutationMethods({                                                                             // 236
        useExisting: options._suppressSameNameError === true                                                    // 236
      });                                                                                                       // 236
    } catch (error) {                                                                                           // 237
      // Throw a more understandable error on the server for same collection name                               // 238
      if (error.message === "A method named '/" + name + "/insert' is already defined") throw new Error("There is already a collection named \"" + name + "\"");
      throw error;                                                                                              // 241
    }                                                                                                           // 242
  } // autopublish                                                                                              // 243
                                                                                                                //
                                                                                                                //
  if (Package.autopublish && !options._preventAutopublish && self._connection && self._connection.publish) {    // 246
    self._connection.publish(null, function () {                                                                // 247
      return self.find();                                                                                       // 248
    }, {                                                                                                        // 249
      is_auto: true                                                                                             // 249
    });                                                                                                         // 249
  }                                                                                                             // 250
}; ///                                                                                                          // 251
/// Main collection API                                                                                         // 254
///                                                                                                             // 255
                                                                                                                //
                                                                                                                //
_.extend(Mongo.Collection.prototype, {                                                                          // 258
  _getFindSelector: function (args) {                                                                           // 260
    if (args.length == 0) return {};else return args[0];                                                        // 261
  },                                                                                                            // 265
  _getFindOptions: function (args) {                                                                            // 267
    var self = this;                                                                                            // 268
                                                                                                                //
    if (args.length < 2) {                                                                                      // 269
      return {                                                                                                  // 270
        transform: self._transform                                                                              // 270
      };                                                                                                        // 270
    } else {                                                                                                    // 271
      check(args[1], Match.Optional(Match.ObjectIncluding({                                                     // 272
        fields: Match.Optional(Match.OneOf(Object, undefined)),                                                 // 273
        sort: Match.Optional(Match.OneOf(Object, Array, Function, undefined)),                                  // 274
        limit: Match.Optional(Match.OneOf(Number, undefined)),                                                  // 275
        skip: Match.Optional(Match.OneOf(Number, undefined))                                                    // 276
      })));                                                                                                     // 272
      return _.extend({                                                                                         // 279
        transform: self._transform                                                                              // 280
      }, args[1]);                                                                                              // 279
    }                                                                                                           // 282
  },                                                                                                            // 283
  /**                                                                                                           // 285
   * @summary Find the documents in a collection that match the selector.                                       //
   * @locus Anywhere                                                                                            //
   * @method find                                                                                               //
   * @memberOf Mongo.Collection                                                                                 //
   * @instance                                                                                                  //
   * @param {MongoSelector} [selector] A query describing the documents to find                                 //
   * @param {Object} [options]                                                                                  //
   * @param {MongoSortSpecifier} options.sort Sort order (default: natural order)                               //
   * @param {Number} options.skip Number of results to skip at the beginning                                    //
   * @param {Number} options.limit Maximum number of results to return                                          //
   * @param {MongoFieldSpecifier} options.fields Dictionary of fields to return or exclude.                     //
   * @param {Boolean} options.reactive (Client only) Default `true`; pass `false` to disable reactivity         //
   * @param {Function} options.transform Overrides `transform` on the  [`Collection`](#collections) for this cursor.  Pass `null` to disable transformation.
   * @param {Boolean} options.disableOplog (Server only) Pass true to disable oplog-tailing on this query. This affects the way server processes calls to `observe` on this query. Disabling the oplog can be useful when working with data that updates in large batches.
   * @param {Number} options.pollingIntervalMs (Server only) When oplog is disabled (through the use of `disableOplog` or when otherwise not available), the frequency (in milliseconds) of how often to poll this query when observing on the server. Defaults to 10000ms (10 seconds).
   * @param {Number} options.pollingThrottleMs (Server only) When oplog is disabled (through the use of `disableOplog` or when otherwise not available), the minimum time (in milliseconds) to allow between re-polling when observing on the server. Increasing this will save CPU and mongo load at the expense of slower updates to users. Decreasing this is not recommended. Defaults to 50ms.
   * @param {Number} options.maxTimeMs (Server only) If set, instructs MongoDB to set a time limit for this cursor's operations. If the operation reaches the specified time limit (in milliseconds) without the having been completed, an exception will be thrown. Useful to prevent an (accidental or malicious) unoptimized query from causing a full collection scan that would disrupt other database users, at the expense of needing to handle the resulting error.
   * @param {String|Object} options.hint (Server only) Overrides MongoDB's default index selection and query optimization process. Specify an index to force its use, either by its name or index specification. You can also specify `{ $natural : 1 }` to force a forwards collection scan, or `{ $natural : -1 }` for a reverse collection scan. Setting this is only recommended for advanced users.
   * @returns {Mongo.Cursor}                                                                                    //
   */find: function () /* selector, options */{                                                                 //
    // Collection.find() (return all docs) behaves differently                                                  // 307
    // from Collection.find(undefined) (return 0 docs).  so be                                                  // 308
    // careful about the length of arguments.                                                                   // 309
    var self = this;                                                                                            // 310
                                                                                                                //
    var argArray = _.toArray(arguments);                                                                        // 311
                                                                                                                //
    return self._collection.find(self._getFindSelector(argArray), self._getFindOptions(argArray));              // 312
  },                                                                                                            // 314
  /**                                                                                                           // 316
   * @summary Finds the first document that matches the selector, as ordered by sort and skip options. Returns `undefined` if no matching document is found.
   * @locus Anywhere                                                                                            //
   * @method findOne                                                                                            //
   * @memberOf Mongo.Collection                                                                                 //
   * @instance                                                                                                  //
   * @param {MongoSelector} [selector] A query describing the documents to find                                 //
   * @param {Object} [options]                                                                                  //
   * @param {MongoSortSpecifier} options.sort Sort order (default: natural order)                               //
   * @param {Number} options.skip Number of results to skip at the beginning                                    //
   * @param {MongoFieldSpecifier} options.fields Dictionary of fields to return or exclude.                     //
   * @param {Boolean} options.reactive (Client only) Default true; pass false to disable reactivity             //
   * @param {Function} options.transform Overrides `transform` on the [`Collection`](#collections) for this cursor.  Pass `null` to disable transformation.
   * @returns {Object}                                                                                          //
   */findOne: function () /* selector, options */{                                                              //
    var self = this;                                                                                            // 332
                                                                                                                //
    var argArray = _.toArray(arguments);                                                                        // 333
                                                                                                                //
    return self._collection.findOne(self._getFindSelector(argArray), self._getFindOptions(argArray));           // 334
  }                                                                                                             // 336
});                                                                                                             // 258
                                                                                                                //
Mongo.Collection._publishCursor = function (cursor, sub, collection) {                                          // 340
  var observeHandle = cursor.observeChanges({                                                                   // 341
    added: function (id, fields) {                                                                              // 342
      sub.added(collection, id, fields);                                                                        // 343
    },                                                                                                          // 344
    changed: function (id, fields) {                                                                            // 345
      sub.changed(collection, id, fields);                                                                      // 346
    },                                                                                                          // 347
    removed: function (id) {                                                                                    // 348
      sub.removed(collection, id);                                                                              // 349
    }                                                                                                           // 350
  }); // We don't call sub.ready() here: it gets called in livedata_server, after                               // 341
  // possibly calling _publishCursor on multiple returned cursors.                                              // 354
  // register stop callback (expects lambda w/ no args).                                                        // 356
                                                                                                                //
  sub.onStop(function () {                                                                                      // 357
    observeHandle.stop();                                                                                       // 357
  }); // return the observeHandle in case it needs to be stopped early                                          // 357
                                                                                                                //
  return observeHandle;                                                                                         // 360
}; // protect against dangerous selectors.  falsey and {_id: falsey} are both                                   // 361
// likely programmer error, and not what you want, particularly for destructive                                 // 364
// operations. If a falsey _id is sent in, a new string _id will be                                             // 365
// generated and returned; if a fallbackId is provided, it will be returned                                     // 366
// instead.                                                                                                     // 367
                                                                                                                //
                                                                                                                //
Mongo.Collection._rewriteSelector = function (selector) {                                                       // 368
  var _ref = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},                            // 368
      fallbackId = _ref.fallbackId;                                                                             // 368
                                                                                                                //
  // shorthand -- scalars match _id                                                                             // 369
  if (LocalCollection._selectorIsId(selector)) selector = {                                                     // 370
    _id: selector                                                                                               // 371
  };                                                                                                            // 371
                                                                                                                //
  if (_.isArray(selector)) {                                                                                    // 373
    // This is consistent with the Mongo console itself; if we don't do this                                    // 374
    // check passing an empty array ends up selecting all items                                                 // 375
    throw new Error("Mongo selector can't be an array.");                                                       // 376
  }                                                                                                             // 377
                                                                                                                //
  if (!selector || '_id' in selector && !selector._id) {                                                        // 379
    // can't match anything                                                                                     // 380
    return {                                                                                                    // 381
      _id: fallbackId || Random.id()                                                                            // 381
    };                                                                                                          // 381
  }                                                                                                             // 382
                                                                                                                //
  return selector;                                                                                              // 384
}; // 'insert' immediately returns the inserted document's new _id.                                             // 385
// The others return values immediately if you are in a stub, an in-memory                                      // 388
// unmanaged collection, or a mongo-backed collection and you don't pass a                                      // 389
// callback. 'update' and 'remove' return the number of affected                                                // 390
// documents. 'upsert' returns an object with keys 'numberAffected' and, if an                                  // 391
// insert happened, 'insertedId'.                                                                               // 392
//                                                                                                              // 393
// Otherwise, the semantics are exactly like other methods: they take                                           // 394
// a callback as an optional last argument; if no callback is                                                   // 395
// provided, they block until the operation is complete, and throw an                                           // 396
// exception if it fails; if a callback is provided, then they don't                                            // 397
// necessarily block, and they call the callback when they finish with error and                                // 398
// result arguments.  (The insert method provides the document ID as its result;                                // 399
// update and remove provide the number of affected docs as the result; upsert                                  // 400
// provides an object with numberAffected and maybe insertedId.)                                                // 401
//                                                                                                              // 402
// On the client, blocking is impossible, so if a callback                                                      // 403
// isn't provided, they just return immediately and any error                                                   // 404
// information is lost.                                                                                         // 405
//                                                                                                              // 406
// There's one more tweak. On the client, if you don't provide a                                                // 407
// callback, then if there is an error, a message will be logged with                                           // 408
// Meteor._debug.                                                                                               // 409
//                                                                                                              // 410
// The intent (though this is actually determined by the underlying                                             // 411
// drivers) is that the operations should be done synchronously, not                                            // 412
// generating their result until the database has acknowledged                                                  // 413
// them. In the future maybe we should provide a flag to turn this                                              // 414
// off.                                                                                                         // 415
/**                                                                                                             // 417
 * @summary Insert a document in the collection.  Returns its unique _id.                                       //
 * @locus Anywhere                                                                                              //
 * @method  insert                                                                                              //
 * @memberOf Mongo.Collection                                                                                   //
 * @instance                                                                                                    //
 * @param {Object} doc The document to insert. May not yet have an _id attribute, in which case Meteor will generate one for you.
 * @param {Function} [callback] Optional.  If present, called with an error object as the first argument and, if no error, the _id as the second.
 */                                                                                                             //
                                                                                                                //
Mongo.Collection.prototype.insert = function () {                                                               // 426
  function insert(doc, callback) {                                                                              // 426
    // Make sure we were passed a document to insert                                                            // 427
    if (!doc) {                                                                                                 // 428
      throw new Error("insert requires an argument");                                                           // 429
    } // Shallow-copy the document and possibly generate an ID                                                  // 430
                                                                                                                //
                                                                                                                //
    doc = _.extend({}, doc);                                                                                    // 433
                                                                                                                //
    if ('_id' in doc) {                                                                                         // 435
      if (!doc._id || !(typeof doc._id === 'string' || doc._id instanceof Mongo.ObjectID)) {                    // 436
        throw new Error("Meteor requires document _id fields to be non-empty strings or ObjectIDs");            // 437
      }                                                                                                         // 438
    } else {                                                                                                    // 439
      var generateId = true; // Don't generate the id if we're the client and the 'outermost' call              // 440
      // This optimization saves us passing both the randomSeed and the id                                      // 443
      // Passing both is redundant.                                                                             // 444
                                                                                                                //
      if (this._isRemoteCollection()) {                                                                         // 445
        var enclosing = DDP._CurrentMethodInvocation.get();                                                     // 446
                                                                                                                //
        if (!enclosing) {                                                                                       // 447
          generateId = false;                                                                                   // 448
        }                                                                                                       // 449
      }                                                                                                         // 450
                                                                                                                //
      if (generateId) {                                                                                         // 452
        doc._id = this._makeNewID();                                                                            // 453
      }                                                                                                         // 454
    } // On inserts, always return the id that we generated; on all other                                       // 455
    // operations, just return the result from the collection.                                                  // 458
                                                                                                                //
                                                                                                                //
    var chooseReturnValueFromCollectionResult = function (result) {                                             // 459
      if (doc._id) {                                                                                            // 460
        return doc._id;                                                                                         // 461
      } // XXX what is this for??                                                                               // 462
      // It's some iteraction between the callback to _callMutatorMethod and                                    // 465
      // the return value conversion                                                                            // 466
                                                                                                                //
                                                                                                                //
      doc._id = result;                                                                                         // 467
      return result;                                                                                            // 469
    };                                                                                                          // 470
                                                                                                                //
    var wrappedCallback = wrapCallback(callback, chooseReturnValueFromCollectionResult);                        // 472
                                                                                                                //
    if (this._isRemoteCollection()) {                                                                           // 474
      var result = this._callMutatorMethod("insert", [doc], wrappedCallback);                                   // 475
                                                                                                                //
      return chooseReturnValueFromCollectionResult(result);                                                     // 476
    } // it's my collection.  descend into the collection object                                                // 477
    // and propagate any exception.                                                                             // 480
                                                                                                                //
                                                                                                                //
    try {                                                                                                       // 481
      // If the user provided a callback and the collection implements this                                     // 482
      // operation asynchronously, then queryRet will be undefined, and the                                     // 483
      // result will be returned through the callback instead.                                                  // 484
      var _result = this._collection.insert(doc, wrappedCallback);                                              // 485
                                                                                                                //
      return chooseReturnValueFromCollectionResult(_result);                                                    // 486
    } catch (e) {                                                                                               // 487
      if (callback) {                                                                                           // 488
        callback(e);                                                                                            // 489
        return null;                                                                                            // 490
      }                                                                                                         // 491
                                                                                                                //
      throw e;                                                                                                  // 492
    }                                                                                                           // 493
  }                                                                                                             // 494
                                                                                                                //
  return insert;                                                                                                // 426
}(); /**                                                                                                        // 426
      * @summary Modify one or more documents in the collection. Returns the number of matched documents.       //
      * @locus Anywhere                                                                                         //
      * @method update                                                                                          //
      * @memberOf Mongo.Collection                                                                              //
      * @instance                                                                                               //
      * @param {MongoSelector} selector Specifies which documents to modify                                     //
      * @param {MongoModifier} modifier Specifies how to modify the documents                                   //
      * @param {Object} [options]                                                                               //
      * @param {Boolean} options.multi True to modify all matching documents; false to only modify one of the matching documents (the default).
      * @param {Boolean} options.upsert True to insert a document if no matching documents are found.           //
      * @param {Function} [callback] Optional.  If present, called with an error object as the first argument and, if no error, the number of affected documents as the second.
      */                                                                                                        //
                                                                                                                //
Mongo.Collection.prototype.update = function () {                                                               // 509
  function update(selector, modifier) {                                                                         // 509
    for (var _len = arguments.length, optionsAndCallback = Array(_len > 2 ? _len - 2 : 0), _key = 2; _key < _len; _key++) {
      optionsAndCallback[_key - 2] = arguments[_key];                                                           // 509
    }                                                                                                           // 509
                                                                                                                //
    var callback = popCallbackFromArgs(optionsAndCallback); // We've already popped off the callback, so we are left with an array
    // of one or zero items                                                                                     // 513
                                                                                                                //
    var options = _.clone(optionsAndCallback[0]) || {};                                                         // 514
    var insertedId = void 0;                                                                                    // 515
                                                                                                                //
    if (options && options.upsert) {                                                                            // 516
      // set `insertedId` if absent.  `insertedId` is a Meteor extension.                                       // 517
      if (options.insertedId) {                                                                                 // 518
        if (!(typeof options.insertedId === 'string' || options.insertedId instanceof Mongo.ObjectID)) throw new Error("insertedId must be string or ObjectID");
        insertedId = options.insertedId;                                                                        // 521
      } else if (!selector || !selector._id) {                                                                  // 522
        insertedId = this._makeNewID();                                                                         // 523
        options.generatedId = true;                                                                             // 524
        options.insertedId = insertedId;                                                                        // 525
      }                                                                                                         // 526
    }                                                                                                           // 527
                                                                                                                //
    selector = Mongo.Collection._rewriteSelector(selector, {                                                    // 529
      fallbackId: insertedId                                                                                    // 530
    });                                                                                                         // 530
    var wrappedCallback = wrapCallback(callback);                                                               // 532
                                                                                                                //
    if (this._isRemoteCollection()) {                                                                           // 534
      var args = [selector, modifier, options];                                                                 // 535
      return this._callMutatorMethod("update", args, wrappedCallback);                                          // 541
    } // it's my collection.  descend into the collection object                                                // 542
    // and propagate any exception.                                                                             // 545
                                                                                                                //
                                                                                                                //
    try {                                                                                                       // 546
      // If the user provided a callback and the collection implements this                                     // 547
      // operation asynchronously, then queryRet will be undefined, and the                                     // 548
      // result will be returned through the callback instead.                                                  // 549
      return this._collection.update(selector, modifier, options, wrappedCallback);                             // 550
    } catch (e) {                                                                                               // 552
      if (callback) {                                                                                           // 553
        callback(e);                                                                                            // 554
        return null;                                                                                            // 555
      }                                                                                                         // 556
                                                                                                                //
      throw e;                                                                                                  // 557
    }                                                                                                           // 558
  }                                                                                                             // 559
                                                                                                                //
  return update;                                                                                                // 509
}(); /**                                                                                                        // 509
      * @summary Remove documents from the collection                                                           //
      * @locus Anywhere                                                                                         //
      * @method remove                                                                                          //
      * @memberOf Mongo.Collection                                                                              //
      * @instance                                                                                               //
      * @param {MongoSelector} selector Specifies which documents to remove                                     //
      * @param {Function} [callback] Optional.  If present, called with an error object as its argument.        //
      */                                                                                                        //
                                                                                                                //
Mongo.Collection.prototype.remove = function () {                                                               // 570
  function remove(selector, callback) {                                                                         // 570
    selector = Mongo.Collection._rewriteSelector(selector);                                                     // 571
    var wrappedCallback = wrapCallback(callback);                                                               // 573
                                                                                                                //
    if (this._isRemoteCollection()) {                                                                           // 575
      return this._callMutatorMethod("remove", [selector], wrappedCallback);                                    // 576
    } // it's my collection.  descend into the collection object                                                // 577
    // and propagate any exception.                                                                             // 580
                                                                                                                //
                                                                                                                //
    try {                                                                                                       // 581
      // If the user provided a callback and the collection implements this                                     // 582
      // operation asynchronously, then queryRet will be undefined, and the                                     // 583
      // result will be returned through the callback instead.                                                  // 584
      return this._collection.remove(selector, wrappedCallback);                                                // 585
    } catch (e) {                                                                                               // 586
      if (callback) {                                                                                           // 587
        callback(e);                                                                                            // 588
        return null;                                                                                            // 589
      }                                                                                                         // 590
                                                                                                                //
      throw e;                                                                                                  // 591
    }                                                                                                           // 592
  }                                                                                                             // 593
                                                                                                                //
  return remove;                                                                                                // 570
}(); // Determine if this collection is simply a minimongo representation of a real                             // 570
// database on another server                                                                                   // 596
                                                                                                                //
                                                                                                                //
Mongo.Collection.prototype._isRemoteCollection = function () {                                                  // 597
  function _isRemoteCollection() {                                                                              // 597
    // XXX see #MeteorServerNull                                                                                // 598
    return this._connection && this._connection !== Meteor.server;                                              // 599
  }                                                                                                             // 600
                                                                                                                //
  return _isRemoteCollection;                                                                                   // 597
}(); // Convert the callback to not return a result if there is an error                                        // 597
                                                                                                                //
                                                                                                                //
function wrapCallback(callback, convertResult) {                                                                // 603
  if (!callback) {                                                                                              // 604
    return;                                                                                                     // 605
  } // If no convert function was passed in, just use a "blank function"                                        // 606
                                                                                                                //
                                                                                                                //
  convertResult = convertResult || _.identity;                                                                  // 609
  return function (error, result) {                                                                             // 611
    callback(error, !error && convertResult(result));                                                           // 612
  };                                                                                                            // 613
} /**                                                                                                           // 614
   * @summary Modify one or more documents in the collection, or insert one if no matching documents were found. Returns an object with keys `numberAffected` (the number of documents modified)  and `insertedId` (the unique _id of the document that was inserted, if any).
   * @locus Anywhere                                                                                            //
   * @param {MongoSelector} selector Specifies which documents to modify                                        //
   * @param {MongoModifier} modifier Specifies how to modify the documents                                      //
   * @param {Object} [options]                                                                                  //
   * @param {Boolean} options.multi True to modify all matching documents; false to only modify one of the matching documents (the default).
   * @param {Function} [callback] Optional.  If present, called with an error object as the first argument and, if no error, the number of affected documents as the second.
   */                                                                                                           //
                                                                                                                //
Mongo.Collection.prototype.upsert = function () {                                                               // 625
  function upsert(selector, modifier, options, callback) {                                                      // 625
    if (!callback && typeof options === "function") {                                                           // 627
      callback = options;                                                                                       // 628
      options = {};                                                                                             // 629
    }                                                                                                           // 630
                                                                                                                //
    var updateOptions = _.extend({}, options, {                                                                 // 632
      _returnObject: true,                                                                                      // 633
      upsert: true                                                                                              // 634
    });                                                                                                         // 632
                                                                                                                //
    return this.update(selector, modifier, updateOptions, callback);                                            // 637
  }                                                                                                             // 638
                                                                                                                //
  return upsert;                                                                                                // 625
}(); // We'll actually design an index API later. For now, we just pass through to                              // 625
// Mongo's, but make it synchronous.                                                                            // 641
                                                                                                                //
                                                                                                                //
Mongo.Collection.prototype._ensureIndex = function (index, options) {                                           // 642
  var self = this;                                                                                              // 643
  if (!self._collection._ensureIndex) throw new Error("Can only call _ensureIndex on server collections");      // 644
                                                                                                                //
  self._collection._ensureIndex(index, options);                                                                // 646
};                                                                                                              // 647
                                                                                                                //
Mongo.Collection.prototype._dropIndex = function (index) {                                                      // 648
  var self = this;                                                                                              // 649
  if (!self._collection._dropIndex) throw new Error("Can only call _dropIndex on server collections");          // 650
                                                                                                                //
  self._collection._dropIndex(index);                                                                           // 652
};                                                                                                              // 653
                                                                                                                //
Mongo.Collection.prototype._dropCollection = function () {                                                      // 654
  var self = this;                                                                                              // 655
  if (!self._collection.dropCollection) throw new Error("Can only call _dropCollection on server collections");
                                                                                                                //
  self._collection.dropCollection();                                                                            // 658
};                                                                                                              // 659
                                                                                                                //
Mongo.Collection.prototype._createCappedCollection = function (byteSize, maxDocuments) {                        // 660
  var self = this;                                                                                              // 661
  if (!self._collection._createCappedCollection) throw new Error("Can only call _createCappedCollection on server collections");
                                                                                                                //
  self._collection._createCappedCollection(byteSize, maxDocuments);                                             // 664
}; /**                                                                                                          // 665
    * @summary Returns the [`Collection`](http://mongodb.github.io/node-mongodb-native/2.2/api/Collection.html) object corresponding to this collection from the [npm `mongodb` driver module](https://www.npmjs.com/package/mongodb) which is wrapped by `Mongo.Collection`.
    * @locus Server                                                                                             //
    */                                                                                                          //
                                                                                                                //
Mongo.Collection.prototype.rawCollection = function () {                                                        // 671
  var self = this;                                                                                              // 672
                                                                                                                //
  if (!self._collection.rawCollection) {                                                                        // 673
    throw new Error("Can only call rawCollection on server collections");                                       // 674
  }                                                                                                             // 675
                                                                                                                //
  return self._collection.rawCollection();                                                                      // 676
}; /**                                                                                                          // 677
    * @summary Returns the [`Db`](http://mongodb.github.io/node-mongodb-native/2.2/api/Db.html) object corresponding to this collection's database connection from the [npm `mongodb` driver module](https://www.npmjs.com/package/mongodb) which is wrapped by `Mongo.Collection`.
    * @locus Server                                                                                             //
    */                                                                                                          //
                                                                                                                //
Mongo.Collection.prototype.rawDatabase = function () {                                                          // 683
  var self = this;                                                                                              // 684
                                                                                                                //
  if (!(self._driver.mongo && self._driver.mongo.db)) {                                                         // 685
    throw new Error("Can only call rawDatabase on server collections");                                         // 686
  }                                                                                                             // 687
                                                                                                                //
  return self._driver.mongo.db;                                                                                 // 688
}; /**                                                                                                          // 689
    * @summary Create a Mongo-style `ObjectID`.  If you don't specify a `hexString`, the `ObjectID` will generated randomly (not using MongoDB's ID construction rules).
    * @locus Anywhere                                                                                           //
    * @class                                                                                                    //
    * @param {String} [hexString] Optional.  The 24-character hexadecimal contents of the ObjectID to create    //
    */                                                                                                          //
                                                                                                                //
Mongo.ObjectID = MongoID.ObjectID; /**                                                                          // 698
                                    * @summary To create a cursor, use find. To access the documents in a cursor, use forEach, map, or fetch.
                                    * @class                                                                    //
                                    * @instanceName cursor                                                      //
                                    */                                                                          //
Mongo.Cursor = LocalCollection.Cursor; /**                                                                      // 705
                                        * @deprecated in 0.9.1                                                  //
                                        */                                                                      //
Mongo.Collection.Cursor = Mongo.Cursor; /**                                                                     // 710
                                         * @deprecated in 0.9.1                                                 //
                                         */                                                                     //
Mongo.Collection.ObjectID = Mongo.ObjectID; /**                                                                 // 715
                                             * @deprecated in 0.9.1                                             //
                                             */                                                                 //
Meteor.Collection = Mongo.Collection; // Allow deny stuff is now in the allow-deny package                      // 720
                                                                                                                //
_.extend(Meteor.Collection.prototype, AllowDeny.CollectionPrototype);                                           // 723
                                                                                                                //
function popCallbackFromArgs(args) {                                                                            // 725
  // Pull off any callback (or perhaps a 'callback' variable that was passed                                    // 726
  // in undefined, like how 'upsert' does it).                                                                  // 727
  if (args.length && (args[args.length - 1] === undefined || args[args.length - 1] instanceof Function)) {      // 728
    return args.pop();                                                                                          // 731
  }                                                                                                             // 732
}                                                                                                               // 733
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

}}}}},{
  "extensions": [
    ".js",
    ".json"
  ]
});
require("./node_modules/meteor/mongo/local_collection_driver.js");
require("./node_modules/meteor/mongo/collection.js");

/* Exports */
if (typeof Package === 'undefined') Package = {};
(function (pkg, symbols) {
  for (var s in symbols)
    (s in pkg) || (pkg[s] = symbols[s]);
})(Package.mongo = {}, {
  Mongo: Mongo
});

})();
