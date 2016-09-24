importScripts( "./lib/Promise.min.js", "./lib/FunctionPromise.js", "./lib/pypyjs.js");
pypyjs.ready().then(function() {
    return pypyjs.execfile('mma-lib.py');
})
onmessage = function(e) {
  console.log('Message received from main script');
  console.log(e.data[0]);
  pypyjs.set('song', e.data[0])
  pypyjs.ready().then(function(e) {
    return pypyjs.execfile('mma.py')
  }).catch(function(e) {
      console.log(e);
      console.log(e.trace);
  }).then(function() {
      return pypyjs.get('midi');
  }).then(function(x) {
      console.log("midi is", x);
      postMessage(x);
  })
}
