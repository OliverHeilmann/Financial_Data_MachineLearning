/*! GUCE 1.0.20 Copyright 2018 Oath Holdings, Inc. */
!function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(o,r,function(t){return e[t]}.bind(null,r));return o},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/",n(n.s=10)}([function(e,t,n){"use strict";t.__esModule=!0,function(e){e.backgroundPost="backgroundPost",e.done="done",e.error="error",e.interaction="interaction",e.view="view"}(t.LogEventType||(t.LogEventType={})),function(e){e.setCookies="setCookies",e.dimensions="dimensions",e.done="done",e.log="log",e.navigate="navigate",e.redirect="redirect",e.resize="resize"}(t.MessageType||(t.MessageType={})),function(e){e.blank="blank",e.self="self"}(t.NavigationTarget||(t.NavigationTarget={}))},function(e,t,n){"use strict";t.__esModule=!0;var o=decodeURIComponent,r=/; */;function i(e,t){try{return t(e)}catch(t){return e}}t.default=function(e,t){if("string"!=typeof e)throw new TypeError("argument str must be a string");for(var n={},a=t||{},s=e.split(r),c=a.decode||o,u=0;u<s.length;u++){var f=s[u],d=f.indexOf("=");if(!(d<0)){var l=f.substr(0,d).trim(),h=f.substr(++d,f.length).trim();'"'===h[0]&&(h=h.slice(1,-1)),void 0===n[l]&&(n[l]=[]),n[l].push(i(h,c))}}return n}},function(e,t,n){"use strict";t.__esModule=!0,t.encodeUrlSafeBase64=function(e){return e.replace(/\+/g,"-").replace(/\//g,"_")},t.decodeUrlSafeBase64=function(e){return e.replace(/-/g,"+").replace(/_/g,"/")},t.parseCookieValue=function(e){for(var t={},n=e.split("&"),o=0,r=n.length;o<r;o++){var i=n[o].split("=");if(1===i.length){if("first"in t)return;t.first=i[0]}else t[i[0]]=i[1]}return t},t.composeCookieValue=function(e){var t=[];for(var n in e)if(e.hasOwnProperty(n)&&"string"==typeof e[n]){var o=e[n];t.push(n+"="+o)}return t.join("&")},t.serializeCookie=function(e,t,n){var o=/^[\u0009\u0020-\u007e\u0080-\u00ff]+$/;if(!o.test(e))throw new TypeError("Cookie name is invalid");if(t&&!o.test(t))throw new TypeError("Cookie val is invalid");var r=e+"="+t;if(null!=n.maxAge){var i=n.maxAge-0;if(isNaN(i))throw new Error("maxAge should be a Number");r+="; Max-Age="+Math.floor(i)}if(n.domain){if(!o.test(n.domain))throw new TypeError("option domain is invalid");r+="; Domain="+n.domain}if(n.path){if(!o.test(n.path))throw new TypeError("option path is invalid");r+="; Path="+n.path}return n.secure&&(r+="; Secure"),r}},function(e,t,n){"use strict";t.__esModule=!0;var o=window;function r(e){var t=+new Date,n=[];for(var o in e)o&&e.hasOwnProperty(o)&&null!=e[o]&&n.push(encodeURIComponent(o)+"="+encodeURIComponent(""+e[o]));return"https://ganon.yahoo.com/p?s=1197805870&t="+t+"&"+n.join("&")}function i(e,t){"function"==typeof o.dispatchEvent&&"function"==typeof o.CustomEvent&&o.dispatchEvent(new CustomEvent("guce-beacon",{detail:{eventType:e,params:t}}))}function a(e,t,n,o){e.addEventListener(t,n,{capture:!1,passive:o})}function s(e,t){var n,r,i=!1,s=function(){n=null,o.clearTimeout(r),t&&t()};if(o.navigator&&"function"==typeof o.navigator.sendBeacon)try{o.navigator.sendBeacon(e)?s():i=!0}catch(e){i=!0}else i=!0;i&&(a(n=new Image,"error",s),a(n,"load",s),a(n,"abort",s),n.src=e,r=o.setTimeout(s,1e3))}t.logEvent=function(e,t,n){var a=o.OathGUCE.lastDecision&&o.OathGUCE.lastDecision.normalizedOptions;if(null==e||null==t||null==a||a.reportOnly)n&&n();else{t._R=o.location.hostname,t._w=t._w?t._w:o.location.href,t.etrg=e,t.ver="gucejs",t.gm_vn="1.0.20",t.gm_beu=a.isProductEU?"1":"0",t.gm_inline=a.inlineConsent?"1":"0",t.gm_lang=a.locale;var c=a.consentHost,u=c&&c.substring(c.indexOf("guce.")+5);t.gm_np=u&&u.substring(0,u.indexOf("."));var f=t;s(r(f),n),i(e,f)}},t.buildBeaconUrl=r,t.fireCustomEvent=i,t.fireBeacon=s},function(e,t,n){"use strict";t.__esModule=!0;var o=n(12),r=n(13),i=n(1),a=n(2);function s(e,t){var n=null,i=[];if(e.GUC&&e.GUC[0])try{n=r.default(a.parseCookieValue(e.GUC[0]))}catch(e){}for(var s=(e.B||[]).concat(e.BX||[]),c=0;c<s.length;c++)i.push(a.parseCookieValue(s[c]));var u={GUC:n,B:i};return{determination:o.default({consentCookies:u,isProductEU:t}),consentCookies:u}}t.decideWithCookie=function(e,t){return s(i.default(e),t)},t.decideWithParsedCookies=s},function(e,t,n){!function(){var e=t,n="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";function o(e){this.message=e}o.prototype=new Error,o.prototype.name="InvalidCharacterError",e.btoa||(e.btoa=function(e){for(var t,r,i=String(e),a=0,s=n,c="";i.charAt(0|a)||(s="=",a%1);c+=s.charAt(63&t>>8-a%1*8)){if((r=i.charCodeAt(a+=.75))>255)throw new o("'btoa' failed: The string to be encoded contains characters outside of the Latin1 range.");t=t<<8|r}return c}),e.atob||(e.atob=function(e){var t=String(e).replace(/[=]+$/,"");if(t.length%4==1)throw new o("'atob' failed: The string to be decoded is not correctly encoded.");for(var r,i,a=0,s=0,c="";i=t.charAt(s++);~i&&(r=a%4?64*r+i:i,a++%4)?c+=String.fromCharCode(255&r>>(-2*a&6)):0)i=n.indexOf(i);return c})}()},function(e,t,n){"use strict";t.__esModule=!0;var o=n(1),r=n(16);t.default=function(e,t){for(var n=!0,i=o.default(document.cookie),a=0;a<e.length;a++){var s=e[a];if(!(n=r.default(s,t,i)))break}return n}},function(e,t,n){"use strict";t.__esModule=!0;var o,r=n(6),i=n(0),a=n(3),s=n(8),c=window;function u(e){if(e){var t=e.split("/");return t[0]+"//"+t[2]}return""}function f(e,t){return(e+"/").indexOf("/"+t+"/")>0||(e+"/").indexOf("."+t+"/")>0||(""+e).indexOf("/"+t+":")>0||(""+e).indexOf("."+t+":")>0}function d(e){var t=u(e);return 0===t.indexOf("https://")&&(f(t,"oath.com")||f(t,"yahoo.com"))}t.isInlineConsentSupported=function(e){var t=Element.prototype,n="MatchesSelector",o=t.matches||t["o"+n]||t["ms"+n]||t["moz"+n]||t["webkit"+n],r=c.postMessage,i=t.querySelector;return e?!!r:!!o&&!!r&&!!i},t.getUrlOrigin=u,t.isSafeUrl=d;var l=function(){function e(e,t,n,r){e&&t&&(this.redirectUri=t,this.initialCookies=n,this.authorizedMessageOrigin=function(e){var t=u(e),n=t;if(-1===t.indexOf("guce.")){var o=e.indexOf("?");if(-1!==o)for(var r=e.substr(o).split("&"),i=0;i<r.length;i++){var a=r[i].split("=");"redirect_uri"===a[0]&&(n=u(decodeURIComponent(a[1])))}}return n}(e),this.handlers=[],o=c.OathGUCE.perf,this.lastFocus=document.activeElement,this.lastFocus&&this.lastFocus.blur(),r&&(this.doneCallback=r),this.attachEventListeners(),this.insertConsentIFrame(e))}return e.prototype.attachEventListeners=function(){var e=this.handlePostMessage.bind(this),t=this.handleWindowResize.bind(this);c.addEventListener("message",e),this.handlers.push({eventType:"message",eventListener:e,target:c}),c.addEventListener("resize",t),this.handlers.push({eventType:"resize",eventListener:t,target:c})},e.prototype.detachEventListeners=function(){for(var e=0;e<this.handlers.length;e+=1)this.handlers[e].target.removeEventListener(this.handlers[e].eventType,this.handlers[e].eventListener),this.handlers[e]=null;this.handlers=[]},e.prototype.handlePostMessage=function(e){if(e.origin===this.authorizedMessageOrigin||"https://guce.oath.com"===e.origin){var t;if(this.frameInitTimeout>0&&(c.clearTimeout(this.frameInitTimeout),this.frameInitTimeout=null),void 0===o.frameLoaded&&(o.frameLoaded=+new Date),e.data)try{t=JSON.parse(e.data)}catch(e){return}switch(t.messageType){case i.MessageType.redirect:this.redirectToConsentUri();break;case i.MessageType.navigate:if(d(t.url))a.logEvent(i.LogEventType.backgroundPost,{outcm:"iframe navigate",_w:t.url},function(){s.default(t.url,t.target)});else{var n="unsafe url";t.url||(n="missing url"),a.logEvent(i.LogEventType.backgroundPost,{outcm:"iframe navigate",etag:n})}break;case i.MessageType.setCookies:this.setCookiesIfSafe(t.cookies);break;case i.MessageType.dimensions:this.resizeFrame({width:t.width,height:t.height});break;case i.MessageType.log:this.decorateTrackingParams(t.eventType,t.trackingParams),a.logEvent(t.eventType,t.trackingParams);break;case i.MessageType.done:this.decorateTrackingParams(i.LogEventType.done,t.trackingParams),a.logEvent(i.LogEventType.done,t.trackingParams),this.cleanConsentIframe();break;default:return}}},e.prototype.decorateTrackingParams=function(e,t){switch(e){case i.LogEventType.view:t.gm_pfd=o.frameLoaded-o.start,t.gm_pfl=o.frameLoaded-o.frameInserted;break;case i.LogEventType.interaction:case i.LogEventType.done:t.gm_pfv=+new Date-o.frameLoaded;break;default:return}},e.prototype.handleWindowResize=function(){var e={messageType:i.MessageType.resize};this.frame.contentWindow.postMessage(JSON.stringify(e),this.authorizedMessageOrigin)},e.prototype.resizeFrame=function(e){this.frame.style.width="100%",this.frame.style.height=e.height+"px"},e.prototype.insertConsentIFrame=function(e){var t=this;this.frame=document.createElement("iframe");var n=this.frame,r=n.style;n.id="guce-inline-consent-iframe",n.src=e,n.tabIndex=1,n.frameBorder="0",r.bottom="0",r.height="0",r.left="0",r.margin="0 auto",r.maxWidth="900px",r.position="fixed",r.right="0",r.width="100%",r.zIndex="99999",document.body.appendChild(n),void 0===o.frameInserted&&(o.frameInserted=+new Date),this.frameInitTimeout=c.setTimeout(function(){a.logEvent(i.LogEventType.error,{outcm:"frame init fail"}),t.cleanConsentIframe(!0)},6e4)},e.prototype.cleanConsentIframe=function(e){this.resizeFrame({width:"0",height:"0"}),this.detachEventListeners(),this.lastFocus&&this.lastFocus.focus(),e&&this.frame&&(document.getElementById(this.frame.id)&&document.body.removeChild(this.frame),this.frame=null),this.doneCallback&&this.doneCallback()},e.prototype.redirectToConsentUri=function(){this.redirectUri&&s.default(this.redirectUri)},e.prototype.setCookiesIfSafe=function(e){if(r.default(e,this.initialCookies)){for(var t=0;t<e.length;t++)this.setCookie(e[t]);a.logEvent(i.LogEventType.backgroundPost,{outcm:"iframe set cookies"})}else a.logEvent(i.LogEventType.backgroundPost,{outcm:"iframe set cookies",etag:"failed"})},e.prototype.setCookie=function(e){document.cookie=e},e}();t.default=l},function(e,t,n){"use strict";t.__esModule=!0;var o=n(0);t.default=function(e,t){t===o.NavigationTarget.blank?window.open(e,"_newtab"):window.location.href=e}},function(e,t,n){"use strict";t.__esModule=!0,t.yo="http://yo/guce-js",t.api="OathGUCE",t.version="1.0.20",t.warn=function(e,n){if(console){var o=n?"Unable to continue. Fix: "+t.yo+"-define":t.yo;console.warn(t.api+" "+t.version+": "+e+" "+o)}},t.log=function(e){console&&console.log(t.api+" "+t.version+": "+e+" "+t.yo+"-report-only")}},function(e,t,n){"use strict";var o=this&&this.__assign||Object.assign||function(e){for(var t,n=1,o=arguments.length;n<o;n++)for(var r in t=arguments[n])Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r]);return e};t.__esModule=!0;var r,i=n(11),a=n(4),s=n(15),c=n(0),u=n(7),f=n(3),d=n(9),l=n(8),h=window,p=document;function g(e,t,n,i){var a=o({},n),s=t.cookieResult,u=t.remoteResult,d=t.redirectUri,l=t.inlineUri,h=t.unsafeRejectedUri;t.normalizedOptions&&t.normalizedOptions.beacon&&(e&&e.message&&(a.message=e.message),s&&(a.gm_crsn=s.determination.reason),u?(a.gm_ra=u.outcome,void 0!==u.statusCode&&(a.gm_hc=u.statusCode)):void 0!==t.outcome&&(a.gm_ra=t.outcome),l&&"redirect fallback"!==a.etag?a._w=l:d?a._w=d:h&&(a._w=h),void 0!==r.decision&&void 0!==r.start&&(a.gm_pjs=r.decision-r.start),f.logEvent(c.LogEventType.backgroundPost,o({outcm:"decision"},a),i))}function m(e,t){if(t){r.decision=+new Date;try{var n=t.normalizedOptions.reportOnly;if(n&&(d.warn("Report only mode, will not redirect the page or display inline consent."),d.log('Cookies: "'+p.cookie+'"'),d.log("Decision: "+JSON.stringify(t))),t.remoteResult){for(var o=t.remoteResult.cookies,a=0;a<o.length;a++)n?d.log("Would set cookie: "+o[a]):p.cookie=o[a];if(n){var s=t.remoteResult.unsafeRejectedCookies;for(a=0;a<s.length;a++)d.log("Rejected cookie: "+s[a])}}if(t.inlineUri&&t.redirectUri){if(!n)return void i(function(){!function(e){try{var t,n=new u.default(e.inlineUri,e.redirectUri,e.initialCookies,function(){t>0&&window.clearTimeout(t)});e.sessionExpiry>0&&(t=window.setTimeout(function(){n.cleanConsentIframe(!0),f.logEvent(c.LogEventType.done,{outcm:"session expired"})},e.sessionExpiry)),g(null,e)}catch(t){e.redirectUri?g(t,e,{etag:"redirect fallback"},function(){l.default(e.redirectUri)}):g(t,e,{etag:"inline failed"}),d.warn("Error during run: "+(t.message?t.message:t))}}(t)});d.log("Would load inline consent iframe: "+t.inlineUri)}else if(t.redirectUri){if(!n)return void g(e,t,{},function(){l.default(t.redirectUri)});d.log("Would redirect: "+t.redirectUri)}e?(g(e,t,{etag:"failed"}),d.warn("Error during decision: "+(e.message?e.message:e))):g(e,t)}catch(e){g(e,t,{etag:"run failed"}),d.warn("Error during run: "+(e.message?e.message:e))}}}function v(e){r.start=+new Date,s.default(e,m)}h.location,h.OathGUCE||(h.OathGUCE={lastDecision:null,perf:{},run:function(e){if(s.isValidOptions(e))return d.warn(d.api+".run is deprecated. Load "+d.api+" async instead."),void v(e);d.warn("Invalid "+d.api+".run options.",!0)},$run:v,decideWithCookie:a.decideWithCookie,decide:s.default,report:function(){var e=o({},h.OathGUCE.lastDecision);e.normalizedOptions.reportOnly=!0,m(null,e)}}),r=h.OathGUCE.perf;var y=s.getOptionsFromMetaTags();y.autorun&&v(y)},function(e,t,n){
/*!
  * domready (c) Dustin Diaz 2014 - License MIT
  */
e.exports=function(){var e,t=[],n=document,o=(n.documentElement.doScroll?/^loaded|^c/:/^loaded|^i|^c/).test(n.readyState);return o||n.addEventListener("DOMContentLoaded",e=function(){for(n.removeEventListener("DOMContentLoaded",e),o=1;e=t.shift();)e()}),function(e){o?setTimeout(e,0):t.push(e)}}()},function(e,t,n){"use strict";t.__esModule=!0,t.default=function(e){var t=e.consentCookies,n=t.GUC;if(null===n)return{reason:1,action:1};var o=Date.now()/1e3|0,r=n.validityCheckTime<=o,i=n.expirationTime<=o,a=n.consented,s=n.tos,c=n.userType,u=0,f=0;return n.consentVersion<1?u=2:i?u=3:n.matchSubject(t)?1===s&&(0===c&&2!==a&&r?u=7:1===c&&(e.isProductEU?u=8:r&&(u=7))):u=4,0!==u&&(f=1),{reason:u,action:f}}},function(e,t,n){"use strict";t.__esModule=!0;var o=n(5),r=n(14),i=n(2),a=function(){function e(e){this.tos=e.tos,this.userType=e.userType,this.consentVersion=e.consentVersion,this.consented=e.consented,this.subjectType=e.subjectType,this.subject=e.subject,this.validityCheckTime=e.validityCheckTime,this.expirationTime=e.expirationTime,this.version=e.version,this.sessionExpirationTime=e.sessionExpirationTime}return e.prototype.matchSubject=function(e){if(1===this.subjectType&&null!==e.B){for(var t=this.subject,n=0;n<e.B.length;n++){var o=e.B[n].first;if(o&&t===r.default(o))return!0}return!1}return!1},e}();function s(e,t,n){var o=0,r=function(n){return 255&e.charCodeAt(t+n)};if(2===n)o=(r(0)<<8|r(1))<<16;else if(3===n)o=(r(0)<<16|r(1)<<8|r(2))<<8;else for(var i=0;i<n;i++)o=o<<8|r(i);return o}t.CookieConsent=a,t.default=function(e){if(function(e){return!!e.first}(e))return function(e,t){var n=function(t){return e.charCodeAt(t)},o=0,r=n(o++),i=n(o++),c=n(o++),u=n(o++),f=n(o++),d=s(e,o,3),l=s(e,o+=3,2);o+=2;var h=e.substr(o++,1),p=s(e,o,4),g=0;"b"!==h&&"B"!==h||(g=1);var m=s(t,0,4);return new a({tos:i,userType:c,consentVersion:u,consented:f,subjectType:g,subject:p,validityCheckTime:d,expirationTime:l,version:r,sessionExpirationTime:m})}(o.atob(i.decodeUrlSafeBase64(e.first)),e.g?o.atob(i.decodeUrlSafeBase64(e.g)):"");throw new TypeError("Missing required data field.")}},function(e,t,n){"use strict";t.__esModule=!0;t.default=function(e){for(var t=1,n=0,o=0,r=e.length;o<r;++o)n=(n+(t=(t+e.charCodeAt(o))%65521))%65521;return n<<16|t}},function(e,t,n){"use strict";t.__esModule=!0;var o=n(1),r=n(6),i=n(4),a=n(18),s=n(0),c=n(7),u=n(19),f=n(22),d=n(3),l=n(9),h=n(23),p=window,g=document;function m(e,t,n,i,a,s,u){var f=0;if(e)!function(e,t,n,o){var r=null,i=107;!function(e){return void 0!==e.cycles}(e)?function(e){return void 0!==e.status}(e)&&(i=e.status>0?113:107,r=e.status):i=112,n.remoteResult={outcome:i,statusCode:r,action:0,cookies:[],unsafeRejectedCookies:[]},l.warn("Consent check failure. Is "+t+" online?"),o(e,n)}(e,t,i,u);else{switch(s.action){case 2:return i.remoteResult=function(e,t){var n,i=[],a=[],s=e.unsafeCookies;return o.default(g.cookie),r.default(s,t)?(n=3,i=i.concat(s)):(n=106,a=a.concat(s)),{action:e.action,outcome:n,cookies:i,unsafeRejectedCookies:a}}(s,i.initialCookies),void u(e,i);case 4:f=110;case 3:var d=s.unsafeConsentUri,p=s.unsafeConsentInlineUri,m=c.isInlineConsentSupported(n.isProductEU),v=h.isValidConsentUri(d,t),y=h.isValidConsentUri(p,t);p&&(1==(f=n.isProductEU||n.inlineConsent?m?y?1:102:101:103)?(i.inlineUri=p,i.sessionExpiry=s.sessionExpiry):(i.unsafeRejectedUri=p,v||(f=114))),v?(0===f&&(f=2),i.redirectUri=d):d&&(f=105,i.unsafeRejectedUri=d);break;case 0:f=100;break;default:f=109}i.remoteResult={outcome:f,action:s.action,cookies:[],unsafeRejectedCookies:[]},u(e,i)}}function v(e,t,n){l.warn(t,!0),d.logEvent(s.LogEventType.backgroundPost,{outcm:"decision",etag:e}),n(new Error(t))}function y(e){return e&&e.consentHost&&void 0!==e.isProductEU}function C(){for(var e=g.getElementsByTagName("meta"),t={autorun:!0,beacon:!0},n=0;n<e.length;n++){var o=e[n];"oath:guce:product-eu"===o.name?t.isProductEU="true"===o.content:"oath:guce:consent-host"===o.name?t.consentHost=o.content:"oath:guce:report-only"===o.name?t.reportOnly="true"===o.content:"oath:guce:autorun"===o.name?t.autorun="false"!==o.content:"oath:guce:inline-consent"===o.name?t.inlineConsent="true"===o.content:"oath:guce:locale"===o.name?t.locale=o.content:"oath:guce:experiment"===o.name&&(t.experiment=o.content)}return t}t.isValidOptions=y,t.getOptionsFromMetaTags=C,t.default=function(e,t){function n(e,n){p.OathGUCE.lastDecision=n,t(e,n)}var r=e||C(),s={normalizedOptions:r};try{if(p.OathGUCE.lastDecision=s,!y(r))return void v("invalid config","Required <meta> tags are not properly set.",t);if(!f.default())return void v("cookies disabled","Cookies are disabled.",t);var c=r.cookie;void 0===c&&(c=g.cookie),s.initialCookies=o.default(c);var d=i.decideWithParsedCookies(s.initialCookies,r.isProductEU);s.cookieResult=d;var h=s;if(1===d.determination.action){if(!function(e){if(!e)return!1;var t=Date.now()/1e3|0;return e.sessionExpirationTime>t}(d.consentCookies.GUC))return void function(e,t,n,o){var r="https://"+e.consentHost,i=a.default(e.consentHost);g.cookie=i.cookiePair;var s={callbackURI:p.location.href,consentBaseURI:r,experiment:e.experiment,gcrumb:i.gcrumb,isProductEU:e.isProductEU,locale:e.locale,jsVersion:l.version,referrer:document.referrer};u.default(s,function(t,i){try{m(t,r,e,n,0,i,o)}catch(e){o(e,n)}})}(r,0,h,n);h.outcome=111}n(null,h)}catch(e){n(e,s)}}},function(e,t,n){"use strict";t.__esModule=!0;var o=n(1),r=n(17);function i(e,t){return 0===e.indexOf(t)}t.default=function(e,t,n){if(!(i(e,"GUC=")||i(e,"B=")||i(e,"BX=")))return!1;var a=o.default(e);return!r.default(a,t,n)}},function(e,t,n){"use strict";t.__esModule=!0,t.default=function(e,t,n){var o=Object.keys(e).pop(),r=e[o][0],i=t[o],a=n[o];if(!i&&a)return!0;if(i&&a)for(var s=!0,c=0;c<i.length;c++){for(var u=0;u<a.length;u++)if(i[c]===a[u]){s=!1;break}if(s)return s}if(a&&("B"===o||"BX"===o)){for(u=0;u<a.length;u++)if(a[u]===r)return!1;return!0}return!1}},function(e,t,n){"use strict";t.__esModule=!0;var o=n(5),r=n(2);t.default=function(e){var t=function(e){var t,n=window.crypto,o="";if(n&&n.getRandomValues&&Uint8Array)t=new Uint8Array(5),n.getRandomValues(t);else{t=[];for(var r=0;r<5;r++)t.push(255*Math.random()|0)}for(r=0;r<5;r++)o+=String.fromCharCode(t[r]);return o}(),n=String.fromCharCode(1)+t,i=r.encodeUrlSafeBase64(o.btoa(n)),a=e,s=e.indexOf("guce.");return-1!==s&&(a=e.substring(s+5)),{cookiePair:r.serializeCookie("GUCS",i,{maxAge:1800,domain:a,path:"/",secure:!0}),gcrumb:r.encodeUrlSafeBase64(o.btoa(t))}}},function(e,t,n){"use strict";var o=this&&this.__extends||function(){var e=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var n in t)t.hasOwnProperty(n)&&(e[n]=t[n])};return function(t,n){function o(){this.constructor=t}e(t,n),t.prototype=null===n?Object.create(n):(o.prototype=n.prototype,new o)}}();t.__esModule=!0;var r=n(20),i=n(21),a=function(e){function t(t,n){var o=e.call(this,t)||this;return o.cycles=n,o}return o(t,e),t}(Error);t.CycleError=a,t.default=function(e,t){if(r.default()){var n=e.consentBaseURI,o=e.isProductEU,s=e.callbackURI,c=e.gcrumb,u=e.locale,f=e.jsVersion,d=e.experiment,l=e.referrer,h=n+"/v1/consentCheck?brandType="+(o?"eu":"nonEu")+"&done="+encodeURIComponent(s)+"&gcrumb="+c;u&&(h+="&lang="+u),f&&(h+="&jsVersion="+encodeURIComponent(f)),d&&(h+="&experiment="+encodeURIComponent(d)),l&&(h+="&referer="+encodeURIComponent(l)),i.default(h,function(e,t){var n=e.consentBaseURI,o=e.callbackURI,r=e.gcrumb,s=(e.locale,0);return function e(c,u){if(c)t(c,{action:3});else{var f=null,d=1,l=u.json();if("collectConsent"===l.action)!function(e,t){var n=l.collectConsent;t(null,{action:3,unsafeConsentUri:n.openUri,unsafeConsentInlineUri:n.inlineUri,sessionExpiry:"number"==typeof n.sessionExpiry?n.sessionExpiry:84e4})}(0,t);else{if("repeatConsentCheck"===l.action){if(!i.isCORSSupported()){var h=n+"/consent?done="+encodeURIComponent(o)+"&gcrumb="+r;return void t(f,{action:4,unsafeConsentUri:h})}if(s++<2)return void i.default(l.repeatConsentCheck.checkUri,e);f=new a("Too many rechecks.",s)}"setCookies"!==l.action?("noAction"===l.action&&(d=0),t(f,{action:d})):t(f,{action:2,unsafeCookies:l.setCookies})}}}}(e,t))}else t(null,{action:0})}},function(e,t,n){"use strict";t.__esModule=!0,t.default=function(){return!0}},function(e,t,n){"use strict";var o=this&&this.__extends||function(){var e=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var n in t)t.hasOwnProperty(n)&&(e[n]=t[n])};return function(t,n){function o(){this.constructor=t}e(t,n),t.prototype=null===n?Object.create(n):(o.prototype=n.prototype,new o)}}();t.__esModule=!0;var r="responseText";t.isCORSSupported=function(){return"withCredentials"in new XMLHttpRequest};var i=function(e){function t(t,n){var o=e.call(this,t)||this;return o.status=n,o}return o(t,e),t}(Error);t.XhrError=i;var a=function(){function e(e){this[r]=e}return e.prototype.json=function(){var e;try{e=JSON.parse(this[r])}catch(e){throw new Error("Bad JSON: "+this[r])}return e},e}();t.XhrBody=a,t.default=function(e,t){var n=new XMLHttpRequest;n.open("GET",e),n.withCredentials=!0,n.onreadystatechange=function(){4===n.readyState&&function(e,t,n){200===e?n(null,new a(t)):n(new i("Bad status",e))}(n.status,n[r],t)},n.send()}},function(e,t,n){"use strict";t.__esModule=!0;var o=document;t.default=function(){if(!1===navigator.cookieEnabled)return!1;o.cookie="_GFT=1;";var e=-1!==o.cookie.indexOf("_GFT=");return o.cookie="_GFT=;max-age=0",e}},function(e,t,n){"use strict";function o(e,t){return 0===e.indexOf(t)}t.__esModule=!0,t.isValidConsentUri=function(e,t){if(!e)return!1;for(var n=["guce.oath.com","stage.guce.oath.com","consent.yahoo.com","stage.consent.yahoo.com","accounts.huffingtonpost.com"],r=["aol","engadget","mapquest","moviefone","techcrunch","yahoo"],i=!1,a=0;a<r.length;a++)n.push("api.login."+r[a]+".com");for(var s=0;s<n.length;s++)if(o(e,"https://"+n[s]+"/")){i=!0;break}return o(e,t+"/")||o(e,"https://dev.guce.oath.com:")||o(e,"https://dev.consent.yahoo.com:")||i}}]);
//# sourceMappingURL=guce.js.map