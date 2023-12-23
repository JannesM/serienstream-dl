
function iOS() {
  return ['iPad', 'iPhone', 'iPod'].includes(navigator.platform) || (navigator.userAgent.includes("Mac") && "ontouchend" in document)
}

function lookAwayFunction() {
  console.clear();
  var before = (new Date).getTime();
  debugger;
  var after = (new Date).getTime();
  if (after - before > 200) {
      document.write("");
      self.location.replace(window.location.protocol + window.location.href.substring(window.location.protocol.length))
  } else {
      before = null;
      after = null;
      delete before;
      delete after
  }
  setTimeout(lookAwayFunction, 100)
}

lookAwayFunction();

window.onload = function () {
  document.addEventListener("contextmenu", function (e) {
      e.preventDefault()
  }, false);
  document.addEventListener("keydown", function (e) {
      if (e.ctrlKey && e.shiftKey && e.keyCode == 73) {
          disabledEvent(e)
      }
      if (e.ctrlKey && e.shiftKey && e.keyCode == 74) {
          disabledEvent(e)
      }
      if (e.keyCode == 83 && (navigator.platform.match("Mac") ? e.metaKey : e.ctrlKey)) {
          disabledEvent(e)
      }
      if (e.ctrlKey && e.keyCode == 85) {
          disabledEvent(e)
      }
      if (event.keyCode == 123) {
          disabledEvent(e)
      }
  }, false);

  function disabledEvent(e) {
      if (e.stopPropagation) {
          e.stopPropagation()
      } else if (window.event) {
          window.event.cancelBubble = true
      }
      e.preventDefault();
      return false
  }
};

//if (!iOS()) {
  setTimeout(function () {
      try {
          var t = ["sandbox", "hasAttribute", "frameElement", "data", "indexOf", "href", "domain", "", "plugins", "undefined", "namedItem", "Chrome PDF Viewer", "object", "createElement", "onerror", "type", "application/pdf", "setAttribute", "style", "visibility:hidden;width:0;height:0;position:absolute;top:-99px;", "data:application/pdf;base64,JVBERi0xLg0KdHJhaWxlcjw8L1Jvb3Q8PC9QYWdlczw8L0tpZHNbPDwvTWVkaWFCb3hbMCAwIDMgM10+Pl0+Pj4+Pj4=", "appendChild", "body", "removeChild", "parentElement", "/blocked?referer=", "substring", "referrer"];

          function setLocationHrefToBlocked() {
              try {
                  if (0) {
                      var n = window.location.ancestorOrigins;
                      if (n[n.length - 1].endsWith("ampproject.org") || false) return
                  }
              } catch (e) {
              }
              setTimeout(function () {
                  // location["href"] = "/blocked"
                  location[t[5]] = "/blocked"
              }, 900)
          }

          // may call setLocationHrefToBlocked
          !function (e) {
              try {
                // window[frameElement][hasAttribute](sandbox)
                  if (window[t[2]][t[1]](t[0])) return void e()
              } catch (e) {
              }

              // location[href][indexOf](data) || document[domain] != ""
              if (0 == location[t[5]][t[4]](t[3]) || document[t[6]] != t[7]) {
              } else e()
          }(setLocationHrefToBlocked), 
          
          function () {
              try {
                  document.domain = document.domain
              } catch (e) {
                  try {
                      if (-1 != e.toString().toLowerCase().indexOf("sandbox")) return !0
                  } catch (e) {
                  }
              }
              return !1
          }() && setLocationHrefToBlocked(), function () {
              if (window.parent === window) return !1;
              try {
                  var e = window.frameElement
              } catch (t) {
                  e = null
              }
              return null === e ? "" === document.domain && "data:" !== location.protocol : e.hasAttribute("sandbox")
          }() && setLocationHrefToBlocked()
      } catch (e) {
      }
  }, 1e3);
//}
